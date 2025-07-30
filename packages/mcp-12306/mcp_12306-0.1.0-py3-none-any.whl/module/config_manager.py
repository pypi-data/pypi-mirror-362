import os
import time
import threading
import logging
import toml
from typing import Dict, Any, Optional

class ConfigManager:
    """配置管理器，支持从文件加载配置并定时刷新"""
    # 刷新时间，默认2小时
    def __init__(self, config_path: str, refresh_interval: int = 7200):
        """
        初始化配置管理器
        
        Args:
            config_path: 配置文件路径
            refresh_interval: 刷新间隔（秒），默认2小时
        """
        self._config_path = config_path
        self._refresh_interval = refresh_interval
        self._config = {}  # 存储配置的容器
        self._lock = threading.RLock()  # 读写锁，保证线程安全
        self._stop_event = threading.Event()
        self._refresh_thread = None
        
        # 初始化日志
        self._logger = logging.getLogger('ConfigManager')
        self._logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)
        
        # 首次加载配置
        self.reload_config()
        self.get_config()
        
        # 启动定时刷新线程
        if refresh_interval > 0:
            self._refresh_thread = threading.Thread(target=self._refresh_loop, daemon=True)
            self._refresh_thread.start()
    
    def _refresh_loop(self):
        """定时刷新配置的循环"""
        while not self._stop_event.wait(self._refresh_interval):
            try:
                self.reload_config()
            except Exception as e:
                self._logger.error(f"Failed to refresh config: {e}")
    
    def reload_config(self) -> None:
        try:
            # 打印绝对路径，方便排查
            abs_path = os.path.abspath(self._config_path)
            self._logger.info(f"Trying to load config from: {abs_path}")
            
            if not os.path.exists(abs_path):
                self._logger.warning(f"Config file not found: {abs_path}")
                return
               
            with open(self._config_path, 'r', encoding='utf-8') as f:
                new_config = toml.load(f)
            
            with self._lock:
                self._config = new_config
                self._logger.info(f"Config reloaded from {self._config_path}")
                
        except Exception as e:
            self._logger.error(f"Error loading config: {e}")
    
    def get_config(self) -> Dict[str, Any]:
        """获取当前配置的副本（线程安全）"""
        with self._lock:
            return self._config.copy()
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项的值（线程安全）"""
        with self._lock:
            return self._config.get(key, default)
    
    async def get_nested(self, keys: list, default: Any = None) -> Any:
        """获取嵌套配置项的值（线程安全）"""
        with self._lock:
            value = self._config
            for key in keys:
                if not isinstance(value, dict) or key not in value:
                    return default
                value = value[key]
            return value
    
    def stop_refresh(self) -> None:
        """停止定时刷新"""
        if self._refresh_thread and self._refresh_thread.is_alive():
            self._stop_event.set()
            self._refresh_thread.join(timeout=5)
            if self._refresh_thread.is_alive():
                self._logger.warning("Refresh thread did not stop gracefully")
    
    def __del__(self):
        """对象销毁时停止刷新线程"""
        self.stop_refresh()

# 使用示例
if __name__ == "__main__":
    # 初始化配置管理器，每2小时刷新一次
    config_manager = ConfigManager('pyproject.toml', refresh_interval=7200)
    
    # 获取完整配置
    all_config = config_manager.get_config()
    print("All config:", all_config)
    
    # 获取特定配置项
    port = config_manager.get_nested(['redis', 'server', 'port'])
    db_url = config_manager.get_nested(['redis', 'server', 'db'])
    print(f"Port: {port}, DB: {db_url}")
    
    # 程序退出时停止刷新线程
    config_manager.stop_refresh()