"""
MySQL connector for VDB using SQLAlchemy ORM with async/sync support.
"""
import contextlib
from contextlib import contextmanager
import threading
import warnings

from sqlalchemy import create_engine, MetaData, Column, Integer, String, TIMESTAMP, func, PrimaryKeyConstraint, text, \
    select
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import asyncio
from ..base import DatabaseTool

# Import common SQLAlchemy types to make available
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
    ForeignKeyConstraint,
    UniqueConstraint,
    CheckConstraint,
    Index
)


# 首先定义 classproperty 装饰器
class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


# 向后兼容的 Model 基类
class CompatModel:
    """向后兼容的 Model 基类，提供 query 属性"""
    
    @classproperty
    def query(cls):
        """向后兼容的 query 属性"""
        warnings.warn(
            "Model.query is deprecated. Use db.session_scope() instead:\n"
            "  with db.session_scope() as session:\n"
            "      users = session.query(User).all()",
            DeprecationWarning,
            stacklevel=2
        )
        # 尝试从 __table__ 获取 bind_key
        bind_key = 'default'
        if hasattr(cls, '__table__') and hasattr(cls.__table__, 'info'):
            bind_key = cls.__table__.info.get('bind_key', 'default')
        
        # 需要访问 connector 实例，这里抛出异常提示用户
        raise RuntimeError(
            "Model.query is no longer supported. Please use session_scope():\n"
            "  with db.session_scope() as session:\n"
            "      result = session.query(Model).all()"
        )


class MySQLConnector(DatabaseTool):
    def __init__(self, config, async_mode=True):
        """Initialize MySQL connector with configuration and mode (async/sync)."""
        self.config = config
        self.async_mode = async_mode
        self.engines = {}  # 存储多个数据库引擎
        self.session_factories = {}  # 存储多个会话工厂
        self.scoped_sessions = {}  # 存储线程安全的会话
        self._engine_lock = threading.RLock()  # 引擎创建锁
        self._factory_lock = threading.RLock()  # 工厂创建锁

        # 直接使用 MetaData
        # 修改 MetaData 的配置
        self.metadata = MetaData(
            # 设置命名约定，使用原始的表名，不转义
            naming_convention={
                "ix": "ix_%(column_0_label)s",
                "uq": "uq_%(table_name)s_%(column_0_name)s",
                "ck": "ck_%(table_name)s_%(constraint_name)s",
                "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
                "pk": "pk_%(table_name)s"
            }
        )
        self.metadata.bind_keys = {}  # 添加 bind_keys 属性

        # 创建基础模型类，不再包含 query 属性
        class BaseModel:
            @classmethod
            def set_bind_key(cls, bind_key):
                if hasattr(cls, '__table__'):
                    cls.__table__.info['bind_key'] = bind_key

            # Add Column as a class attribute
            Column = staticmethod(Column)
            PrimaryKeyConstraint = staticmethod(PrimaryKeyConstraint)
            ForeignKeyConstraint = staticmethod(ForeignKeyConstraint)
            UniqueConstraint = staticmethod(UniqueConstraint)
            CheckConstraint = staticmethod(CheckConstraint)
            Index = staticmethod(Index)
            text = staticmethod(text)  # Add text function for SQL expressions

            # Add common SQLAlchemy types
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
            TIMESTAMP = TIMESTAMP
            func = func  # For SQL functions like current_timestamp()

        # 创建标准的 declarative base，不绑定 connector
        self.Model = declarative_base(cls=BaseModel, metadata=self.metadata)

        # Make Column and types accessible through the connector instance
        self.Column = Column
        self.PrimaryKeyConstraint = PrimaryKeyConstraint
        self.ForeignKeyConstraint = ForeignKeyConstraint
        self.UniqueConstraint = UniqueConstraint
        self.CheckConstraint = CheckConstraint
        self.Index = Index
        self.text = text  # Add text function to connector instance
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
        self.TIMESTAMP = TIMESTAMP
        self.func = func

    def _create_engine(self, db_config, bind_key=None):
        """创建数据库引擎，支持配置化的连接池参数"""
        # 获取连接池配置，支持自定义
        pool_config = {
            'pool_size': db_config.get('pool_size', 5),
            'max_overflow': db_config.get('max_overflow', 10),
            'pool_timeout': db_config.get('pool_timeout', 30),
            'pool_recycle': db_config.get('pool_recycle', 3600),
            'pool_pre_ping': db_config.get('pool_pre_ping', True),
            'pool_use_lifo': db_config.get('pool_use_lifo', True),
            'echo': db_config.get('echo', False),
        }
        
        if self.async_mode:
            url = f"mysql+aiomysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config.get('port', 3306)}/{db_config['database']}"
            engine = create_async_engine(
                url,
                **pool_config,
                connect_args={'charset': 'utf8mb4'}
            )
        else:
            url = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config.get('port', 3306)}/{db_config['database']}"
            engine = create_engine(
                url,
                **pool_config,
                connect_args={'charset': 'utf8mb4'}
            )

        if bind_key:
            self.metadata.bind_keys[bind_key] = engine
        return engine

    async def connect(self, bind_key=None):
        """Asynchronously create SQLAlchemy ORM connections to MySQL databases."""
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
    
    def get_compat_model(self):
        """获取向后兼容的 Model 类"""
        warnings.warn(
            "Using Model.query pattern is deprecated. Please migrate to session_scope().",
            DeprecationWarning,
            stacklevel=2
        )
        
        # 创建一个继承自 BaseModel 和 CompatModel 的类
        class CompatibleModel(self.Model.__class__, CompatModel):
            pass
        
        # 返回兼容的 declarative base
        return declarative_base(cls=CompatibleModel, metadata=self.metadata)
    
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
