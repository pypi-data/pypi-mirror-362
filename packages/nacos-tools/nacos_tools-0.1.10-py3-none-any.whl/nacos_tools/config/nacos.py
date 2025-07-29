"""
Nacos-specific implementation of configuration management.
"""
import asyncio
import os
import threading
import time
from typing import Optional, Callable, Any

from nacos import NacosClient
from .manager import ConfigManager
from ..lib.helper import retry_on_exception, calculate_md5


class NacosConfig(ConfigManager):
    def __init__(self, server_addr, namespace="public", group="DEFAULT_GROUP", username=None, password=None,
                 retry_times=3, retry_interval=1):
        """Initialize Nacos client with server address, namespace, and group."""
        # self.client = NacosClient(server_addr, namespace=namespace, username=username, password=password)
        # self.group = group
        self.server_addr = server_addr
        self.namespace = namespace
        self.group = group
        self.username = username
        self.password = password
        self.retry_times = retry_times
        self.retry_interval = retry_interval

        # 初始化客户端
        self.client = None
        self.initialize_client()

        # 配置监听相关
        self._running = False
        self._listener_thread = None
        self._loop = None
        self.listener_interval = 5  # 监听间隔（秒）

        # 心跳检测相关
        self._heartbeat_thread = None
        self._heartbeat_running = False
        self.heartbeat_interval = 5  # 心跳间隔（秒）

        # 连接状态
        self._connected = False
        self._reconnect_thread: Optional[threading.Thread] = None

    def check_server_health(self) -> bool:
        """检查服务器健康状态"""
        try:
            # 尝试获取一个不存在的配置来测试连接
            self.client._do_sync_req(
                '/nacos/v1/cs/configs',
                params={
                    'dataId': 'health_check',
                    'group': self.group,
                    'tenant': self.client.namespace
                }
            )
            return True
        except Exception as e:
            print(f"Health check failed: {e}")
            return False

    def initialize_client(self) -> bool:
        """初始化Nacos客户端并尝试连接"""
        for attempt in range(self.retry_times):
            try:
                self.client = NacosClient(
                    self.server_addr,
                    namespace=self.namespace,
                    username=self.username,
                    password=self.password
                )
                # 测试连接
                if self.check_server_health():
                    self._connected = True
                    print("Successfully connected to Nacos server")
                    return True
                else:
                    raise Exception("Server health check failed")
            except Exception as e:
                print(f"Connection attempt {attempt + 1} failed: {str(e)}")
                if attempt < self.retry_times - 1:
                    time.sleep(self.retry_interval)
                else:
                    print("Failed to connect to Nacos server after all attempts")
                    return False
        return False

    def check_connection(self) -> bool:
        """检查与Nacos服务器的连接状态"""
        try:
            return self.check_server_health()
        except Exception:
            self._connected = False
            return False

    def reconnect(self):
        """重新连接到Nacos服务器"""
        while not self._connected:
            if self.initialize_client():
                break
            time.sleep(self.retry_interval)

    def start_reconnect_thread(self):
        """启动重连线程"""
        if not self._reconnect_thread or not self._reconnect_thread.is_alive():
            self._reconnect_thread = threading.Thread(
                target=self.reconnect,
                daemon=True
            )
            self._reconnect_thread.start()

    @retry_on_exception(retries=3, delay=1)
    def _get_config_with_no_cache(self, data_id):
        """
        获取配置时添加时间戳避免缓存
        """
        if not self._connected:
            self.start_reconnect_thread()
            return None

        # 添加时间戳参数避免缓存
        timestamp = int(time.time() * 1000)
        params = {
            'dataId': data_id,
            'group': self.group,
            'tenant': self.client.namespace,
            'timestamp': timestamp  # 添加时间戳
        }

        # 直接调用 Nacos 的配置接口
        response = self.client._do_sync_req(
            '/nacos/v1/cs/configs',
            params=params
        )

        return response.read().decode("UTF-8")

    @retry_on_exception(retries=3, delay=1)
    def load_config(self, data_id: str) -> bool:
        """Load configuration from Nacos and set it as environment variables."""
        if not self._connected:
            self.start_reconnect_thread()
            return False

        try:
            config = self.client.get_config(data_id, self.group)
            if config:
                self._process_config(config)
                return True
            return False
        except Exception as e:
            print(f"Error loading config: {e}")
            self._connected = False
            self.start_reconnect_thread()
            return False

    def _process_config(self, config: str):
        """处理配置内容"""
        for line in config.splitlines():
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

    async def _run_callback(self, callback: Callable, args: Any):
        """异步执行回调"""
        try:
            await callback(args)
        except Exception as e:
            print(f"Error in callback: {e}")

    def _watch_config(self, data_id, callback):
        """监听配置变更的内部方法"""
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

        last_md5 = None
        while self._running:
            try:
                # 获取最新配置（无缓存）
                current_content = self._get_config_with_no_cache(data_id)
                current_md5 = calculate_md5(current_content)

                # 检查配置是否发生变化
                if current_md5 != last_md5:
                    if current_content is not None:  # 不是首次获取
                        # 异步执行回调
                        self._loop.run_until_complete(
                            self._run_callback(callback, {
                                "data_id": data_id,
                                "group": self.group,
                                "config": current_content
                            })
                        )
                    last_md5 = current_md5

                # 等待一段时间后再次检查
                time.sleep(self.listener_interval)

            except Exception as e:
                print(f"Error in config watcher: {e}")
                time.sleep(5)

        if self._loop:
            self._loop.close()

    def _send_heartbeat(self, service_name, ip, port):
        """发送心跳的内部方法"""
        while self._heartbeat_running:
            try:
                self.client.send_heartbeat(
                    service_name,
                    ip,
                    port,
                    group_name=self.group
                )
                time.sleep(self.heartbeat_interval)
            except Exception as e:
                # print(f"Error sending heartbeat: {e}")
                time.sleep(1)  # 出错后等待短暂时间再重试

    def update_config(self, args):
        """更新配置变更的内部方法"""
        config = args.get("config")
        if config:
            for line in config.splitlines():
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

    def start_listening(self, data_id, callback):
        """实现配置监听"""
        if self._listener_thread is None or not self._listener_thread.is_alive():
            self._running = True
            self._listener_thread = threading.Thread(
                target=self._watch_config,
                args=(data_id, callback),
                daemon=True
            )
            self._listener_thread.start()

    def stop_listening(self):
        """Stop listening for configuration changes."""
        self._running = False
        if hasattr(self, '_listener_thread') and self._listener_thread and self._listener_thread.is_alive():
            self._listener_thread.join(timeout=2)  # 等待线程结束，最多等待2秒
        if hasattr(self, '_loop') and self._loop:
            self._loop.stop()

    def start_heartbeat(self, service_name, ip, port):
        """启动心跳检测"""
        if self._heartbeat_thread is None or not self._heartbeat_thread.is_alive():
            self._heartbeat_running = True
            self._heartbeat_thread = threading.Thread(
                target=self._send_heartbeat,
                args=(service_name, ip, port),
                daemon=True
            )
            self._heartbeat_thread.start()

    def stop_heartbeat(self):
        """停止心跳检测"""
        self._heartbeat_running = False
        if hasattr(self, '_heartbeat_thread') and self._heartbeat_thread and self._heartbeat_thread.is_alive():
            self._heartbeat_thread.join(timeout=2)

    def __del__(self):
        """Cleanup when the object is destroyed."""
        self.stop_heartbeat()
        self.stop_listening()
