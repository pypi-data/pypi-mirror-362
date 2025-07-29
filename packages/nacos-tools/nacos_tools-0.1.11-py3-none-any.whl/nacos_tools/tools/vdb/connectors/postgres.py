"""
PostgreSQL connector for VDB using SQLAlchemy ORM with async/sync support.
"""
import contextlib
from contextlib import contextmanager
import threading
import warnings

from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import asyncio
from ..base import DatabaseTool

# Import PostgreSQL specific types and features
from sqlalchemy.types import (
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    Float,
    BigInteger,
    Date,
    Time,
    JSON,
)

from sqlalchemy import (
    Column,
    ForeignKeyConstraint,
    UniqueConstraint,
    CheckConstraint,
    Index,
    PrimaryKeyConstraint,
    func,
    select,
    insert,
    update
)

from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncEngine
import psycopg2


class PostgresConnector(DatabaseTool):
    def __init__(self, config, async_mode=True):
        """Initialize PostgreSQL connector with configuration and mode (async/sync)."""
        self.config = config
        self.async_mode = async_mode
        self.engines = {}  # 存储多个数据库引擎
        self.session_factories = {}  # 存储多个会话工厂
        self.scoped_sessions = {}  # 存储线程安全的会话
        self._engine_lock = threading.RLock()  # 引擎创建锁
        self._factory_lock = threading.RLock()  # 工厂创建锁

        # 设置 MetaData 配置
        self.metadata = MetaData(
            naming_convention={
                "ix": "ix_%(column_0_label)s",
                "uq": "uq_%(table_name)s_%(column_0_name)s",
                "ck": "ck_%(table_name)s_%(constraint_name)s",
                "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
                "pk": "pk_%(table_name)s"
            }
        )
        self.metadata.bind_keys = {}

        # 创建基础模型类，不再包含 query 属性
        class BaseModel:
            @classmethod
            def set_bind_key(cls, bind_key):
                if hasattr(cls, '__table__'):
                    cls.__table__.info['bind_key'] = bind_key

            # Add common PostgreSQL types as class attributes
            Column = staticmethod(Column)
            PrimaryKeyConstraint = staticmethod(PrimaryKeyConstraint)
            ForeignKeyConstraint = staticmethod(ForeignKeyConstraint)
            UniqueConstraint = staticmethod(UniqueConstraint)
            CheckConstraint = staticmethod(CheckConstraint)
            Index = staticmethod(Index)
            text = staticmethod(text)
            
            # PostgreSQL types
            Integer = Integer
            String = String
            Text = Text
            Boolean = Boolean
            DateTime = DateTime
            Float = Float
            BigInteger = BigInteger
            Date = Date
            Time = Time
            JSON = JSON
            func = func

        # 创建标准的 declarative base，不绑定 connector
        self.Model = declarative_base(cls=BaseModel, metadata=self.metadata)
        
        # Make types accessible through the connector instance
        self.Column = Column
        self.PrimaryKeyConstraint = PrimaryKeyConstraint
        self.ForeignKeyConstraint = ForeignKeyConstraint
        self.UniqueConstraint = UniqueConstraint
        self.CheckConstraint = CheckConstraint
        self.Index = Index
        self.text = text
        self.Integer = Integer
        self.String = String
        self.Text = Text
        self.Boolean = Boolean
        self.DateTime = DateTime
        self.Float = Float
        self.BigInteger = BigInteger
        self.Date = Date
        self.Time = Time
        self.JSON = JSON
        self.func = func
        
        # PostgreSQL 特有功能
        self.notification_manager = PostgreSQLNotificationManager(self)
        self.query_builder = PostgreSQLQueryBuilder(self)

    def _create_engine(self, db_config, bind_key=None):
        """创建数据库引擎，支持配置化的连接池参数和 PostgreSQL 优化"""
        # PostgreSQL 优化的连接池配置
        pool_config = {
            'pool_size': db_config.get('pool_size', 10),       # PostgreSQL 默认更大
            'max_overflow': db_config.get('max_overflow', 20),  # 支持更多并发连接
            'pool_timeout': db_config.get('pool_timeout', 30),
            'pool_recycle': db_config.get('pool_recycle', 7200), # 2小时，PostgreSQL 建议
            'pool_pre_ping': db_config.get('pool_pre_ping', True),
            'echo': db_config.get('echo', False),  # 生产环境关闭日志
        }
        
        # PostgreSQL 特有的连接参数
        connect_args = {
            'application_name': db_config.get('application_name', 'nacos-tools'),
            'connect_timeout': db_config.get('connect_timeout', 10),
            'command_timeout': db_config.get('command_timeout', 30),
        }
        
        if self.async_mode:
            # 使用 asyncpg 驱动，明确指定
            url = f"postgresql+asyncpg://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config.get('port', 5432)}/{db_config['database']}"
            engine = create_async_engine(
                url,
                **pool_config,
                connect_args=connect_args
            )
        else:
            # 明确指定 psycopg2 驱动
            url = f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config.get('port', 5432)}/{db_config['database']}"
            # 添加 PostgreSQL 特有的连接参数
            connect_args.update({
                'options': f"-c statement_timeout={db_config.get('statement_timeout', 30000)}ms"
            })
            engine = create_engine(
                url,
                **pool_config,
                connect_args=connect_args
            )

        if bind_key:
            self.metadata.bind_keys[bind_key] = engine
        return engine

    async def connect(self):
        """Asynchronously create a SQLAlchemy ORM connection to PostgreSQL."""
        # 使用锁保护引擎创建
        with self._engine_lock:
            # 处理默认连接
            if 'default' not in self.engines:
                default_engine = self._create_engine(self.config)
                self.engines['default'] = default_engine

            # 处理其他绑定的数据库
            if 'binds' in self.config:
                for bind_key, bind_config in self.config['binds'].items():
                    if bind_key not in self.engines:
                        engine = self._create_engine(bind_config, bind_key)
                        self.engines[bind_key] = engine

        # 创建会话工厂
        with self._factory_lock:
            for bind_key, engine in self.engines.items():
                if bind_key not in self.session_factories:
                    if self.async_mode:
                        session_factory = sessionmaker(
                            engine,
                            class_=AsyncSession,
                            expire_on_commit=False,
                            autocommit=False,
                            autoflush=True
                        )
                    else:
                        session_factory = sessionmaker(
                            bind=engine,
                            expire_on_commit=False,
                            autocommit=False,
                            autoflush=True
                        )
                        # 对于同步模式，使用 scoped_session 实现线程安全
                        session_factory = scoped_session(session_factory)
                    
                    self.session_factories[bind_key] = session_factory
                    if not self.async_mode:
                        self.scoped_sessions[bind_key] = session_factory

    async def close(self):
        """Close all database connections."""
        # 对于同步模式，清理 scoped_session
        if not self.async_mode:
            for scoped_session in self.scoped_sessions.values():
                scoped_session.remove()
        
        # 关闭所有引擎
        for engine in self.engines.values():
            if self.async_mode:
                await engine.dispose()
            else:
                engine.dispose()
        
        # 清理所有引用
        self.engines.clear()
        self.session_factories.clear()
        self.scoped_sessions.clear()

    def get_engine(self, bind_key='default'):
        """获取指定绑定键的引擎"""
        return self.engines.get(bind_key)

    def create_session(self, bind_key='default'):
        """创建新的会话实例，不复用会话"""
        if bind_key not in self.session_factories:
            raise ValueError(f"No session factory for bind_key: {bind_key}")
        
        if self.async_mode:
            # 异步模式直接返回新会话
            return self.session_factories[bind_key]()
        else:
            # 同步模式使用 scoped_session，自动管理线程局部会话
            return self.scoped_sessions[bind_key]()

    @contextmanager
    def session_scope(self, bind_key='default'):
        """提供事务范围的会话上下文管理器（同步模式）"""
        if self.async_mode:
            raise RuntimeError("Use async_session_scope for async mode")
        
        session = self.create_session(bind_key)
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            if not self.async_mode:
                # scoped_session 不需要显式 close
                self.scoped_sessions[bind_key].remove()
            else:
                session.close()

    @contextlib.asynccontextmanager
    async def async_session_scope(self, bind_key='default'):
        """提供事务范围的会话上下文管理器（异步模式）"""
        if not self.async_mode:
            raise RuntimeError("Use session_scope for sync mode")
            
        session = self.create_session(bind_key)
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    def __del__(self):
        """确保在对象销毁时清理资源"""
        try:
            # 停止通知监听
            if hasattr(self, 'notification_manager'):
                self.notification_manager.stop_listening()
            
            # 对于同步模式，清理 scoped_session
            if hasattr(self, 'scoped_sessions'):
                for scoped_session in self.scoped_sessions.values():
                    try:
                        scoped_session.remove()
                    except:
                        pass
            
            # 清理引擎
            if hasattr(self, 'engines'):
                for engine in self.engines.values():
                    try:
                        engine.dispose()
                    except:
                        pass
        except:
            pass
    
    # 向后兼容的方法
    def get_session(self, bind_key='default'):
        """向后兼容的方法，建议使用 create_session 或 session_scope"""
        warnings.warn(
            "get_session is deprecated. Use create_session() or session_scope() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.create_session(bind_key)
    
    @property
    def session(self):
        """向后兼容的属性，返回默认会话"""
        warnings.warn(
            "Direct session access is deprecated. Use session_scope() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.create_session('default')
    
    @session.setter
    def session(self, value):
        """向后兼容的 setter"""
        warnings.warn(
            "Setting session directly is deprecated and has no effect.",
            DeprecationWarning,
            stacklevel=2
        )
    
    def connect_sync(self):
        """同步版本的 connect 方法"""
        if self.async_mode:
            raise RuntimeError("Cannot use connect_sync in async mode")
        
        # 直接调用异步版本，但在同步上下文中运行
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.connect())
        finally:
            loop.close()
    
    # PostgreSQL 特有功能的便捷方法
    async def listen_notify(self, channel: str, callback, bind_key='default'):
        """启动 LISTEN/NOTIFY 监听"""
        self.notification_manager.start_listening()
        await self.notification_manager.listen(channel, callback, bind_key)
    
    async def send_notify(self, channel: str, payload: str = '', bind_key='default'):
        """发送 NOTIFY 消息"""
        await self.notification_manager.notify(channel, payload, bind_key)
    
    def stop_notify_listening(self):
        """停止 NOTIFY 监听"""
        self.notification_manager.stop_listening()
    
    async def upsert(self, table, values, conflict_columns, update_columns=None, bind_key='default'):
        """执行 UPSERT 操作"""
        return await self.query_builder.execute_upsert(table, values, conflict_columns, update_columns, bind_key)
    
    def build_json_query(self, table, json_column, json_path, value, bind_key='default'):
        """构建 JSON 查询"""
        return self.query_builder.json_query(table, json_column, json_path, value, bind_key)
    
    def build_json_update(self, table, json_column, json_path, new_value, where_clause, bind_key='default'):
        """构建 JSON 更新"""
        return self.query_builder.json_update(table, json_column, json_path, new_value, where_clause, bind_key)
    
    # 连接池监控方法
    def get_pool_status(self, bind_key='default'):
        """获取连接池状态"""
        engine = self.get_engine(bind_key)
        if engine:
            pool = engine.pool
            return {
                'size': pool.size(),
                'checked_in': pool.checkedin(),
                'checked_out': pool.checkedout(),
                'overflow': pool.overflow(),
                'invalid': pool.invalid()
            }
        return None
    
    def log_pool_status(self, bind_key='default'):
        """记录连接池状态"""
        status = self.get_pool_status(bind_key)
        if status:
            print(f"PostgreSQL Pool Status [{bind_key}]: {status}")


class PostgreSQLNotificationManager:
    """PostgreSQL LISTEN/NOTIFY 管理器"""
    
    def __init__(self, connector: 'PostgresConnector'):
        self.connector = connector
        self.listeners = {}
        self._notify_connections = {}
        self._listening = False
    
    async def listen(self, channel: str, callback, bind_key='default'):
        """监听 PostgreSQL NOTIFY 消息"""
        if self.connector.async_mode:
            await self._async_listen(channel, callback, bind_key)
        else:
            self._sync_listen(channel, callback, bind_key)
    
    async def _async_listen(self, channel: str, callback, bind_key='default'):
        """异步模式监听"""
        import asyncio
        engine = self.connector.get_engine(bind_key)
        if not isinstance(engine, AsyncEngine):
            raise RuntimeError("Async listen requires AsyncEngine")
        
        # 创建专用连接用于监听
        async with engine.connect() as conn:
            await conn.execute(text(f"LISTEN {channel}"))
            self.listeners[channel] = callback
            
            while self._listening:
                # 检查通知（需要 asyncpg 支持）
                try:
                    # 使用 asyncpg 的 connection 对象
                    raw_conn = await conn.get_raw_connection()
                    notifications = await raw_conn.connection.notifies()
                    
                    for notification in notifications:
                        if notification.channel == channel:
                            await callback(notification.payload)
                    
                    await asyncio.sleep(0.1)  # 短暂等待
                except Exception as e:
                    print(f"Error in async notification listener: {e}")
                    break
    
    def _sync_listen(self, channel: str, callback, bind_key='default'):
        """同步模式监听"""
        import select
        engine = self.connector.get_engine(bind_key)
        
        # 创建原始连接用于监听
        raw_conn = engine.raw_connection()
        raw_conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        
        cursor = raw_conn.cursor()
        cursor.execute(f"LISTEN {channel}")
        
        self.listeners[channel] = callback
        self._notify_connections[channel] = (raw_conn, cursor)
        
        def listen_loop():
            while self._listening:
                if select.select([raw_conn], [], [], 1) == ([], [], []):
                    continue
                
                raw_conn.poll()
                while raw_conn.notifies:
                    notify = raw_conn.notifies.pop(0)
                    if notify.channel == channel:
                        callback(notify.payload)
        
        import threading
        listener_thread = threading.Thread(target=listen_loop, daemon=True)
        listener_thread.start()
    
    async def notify(self, channel: str, payload: str = '', bind_key='default'):
        """发送 NOTIFY 消息"""
        if self.connector.async_mode:
            async with self.connector.async_session_scope(bind_key) as session:
                await session.execute(text(f"NOTIFY {channel}, '{payload}'"))
        else:
            with self.connector.session_scope(bind_key) as session:
                session.execute(text(f"NOTIFY {channel}, '{payload}'"))
    
    def start_listening(self):
        """开始监听"""
        self._listening = True
    
    def stop_listening(self):
        """停止监听"""
        self._listening = False
        
        # 清理连接
        for channel, (conn, cursor) in self._notify_connections.items():
            try:
                cursor.execute(f"UNLISTEN {channel}")
                cursor.close()
                conn.close()
            except:
                pass
        
        self._notify_connections.clear()
        self.listeners.clear()


class PostgreSQLQueryBuilder:
    """PostgreSQL 查询构建器，支持 UPSERT 和 JSON 操作"""
    
    def __init__(self, connector: 'PostgresConnector'):
        self.connector = connector
    
    def upsert(self, table, values, conflict_columns, update_columns=None, bind_key='default'):
        """构建 PostgreSQL UPSERT 查询 (INSERT ... ON CONFLICT)"""
        if update_columns is None:
            update_columns = [col for col in values.keys() if col not in conflict_columns]
        
        # 使用 PostgreSQL 特有的 insert
        stmt = pg_insert(table).values(values)
        
        # 设置冲突处理
        if isinstance(conflict_columns, str):
            conflict_columns = [conflict_columns]
        
        # 构建更新字典
        update_dict = {col: stmt.excluded[col] for col in update_columns}
        
        stmt = stmt.on_conflict_do_update(
            index_elements=conflict_columns,
            set_=update_dict
        )
        
        return stmt
    
    def json_query(self, table, json_column, json_path, value, bind_key='default'):
        """构建 JSON 路径查询"""
        # PostgreSQL JSON 路径查询
        return select(table).where(
            func.jsonb_extract_path_text(getattr(table.c, json_column), json_path) == value
        )
    
    def json_update(self, table, json_column, json_path, new_value, where_clause, bind_key='default'):
        """构建 JSON 字段更新"""
        # 使用 jsonb_set 函数更新 JSON 字段
        return update(table).where(where_clause).values({
            json_column: func.jsonb_set(
                getattr(table.c, json_column),
                f'{{{json_path}}}',
                f'"{new_value}"',
                True
            )
        })
    
    async def execute_upsert(self, table, values, conflict_columns, update_columns=None, bind_key='default'):
        """执行 UPSERT 操作"""
        stmt = self.upsert(table, values, conflict_columns, update_columns, bind_key)
        
        if self.connector.async_mode:
            async with self.connector.async_session_scope(bind_key) as session:
                result = await session.execute(stmt)
                return result
        else:
            with self.connector.session_scope(bind_key) as session:
                result = session.execute(stmt)
                return result
