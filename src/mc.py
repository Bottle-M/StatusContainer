"""
查询 Minecraft 服务器状态的模块
"""

import asyncio
from mcstatus import JavaServer
from logger import Logger
from asyncio.exceptions import TimeoutError

_mc_logger = Logger("mc").logger


class MCStatus:
    def __init__(self, address: str, timeout: float = 10, cache_max_age: float = 60):
        """
        初始化 MCStatus 实例
        :param address: Minecraft 服务器地址
        :param timeout: 查询超时时间
        :param cache_max_age: 缓存超时时间，单位为秒
        """
        self._address = address
        self._timeout = timeout
        self._cache_max_age = cache_max_age
        self._cached_dict: dict | None = None  # 缓存的返回结果
        self._cache_lock = asyncio.Lock()  # 缓存锁

    async def get(self):
        """
        获取 Minecraft 服务器状态
        :return: 服务器状态字典
        """
        async with self._cache_lock:
            if self._cached_dict is not None:
                return self._cached_dict
            # 如果缓存不存在，则查询服务器状态
            # 这里也写在 with 块内，防止这段时间挤入多个请求击穿缓存
            try:
                server = await JavaServer.async_lookup(self._address, timeout=self._timeout)
                status = await server.async_status()
                status_dict: dict = status.as_dict()
                resp_dict = {
                    "ok": True,
                    "version": status_dict["version"],
                    "players": status_dict["players"],
                    "icon": status_dict.get("icon", ""),
                    "motd": status_dict["motd"],
                }
            except TimeoutError:
                _mc_logger.error(
                    f"Query {self._address} timeout after {self._timeout} seconds."
                )
                resp_dict = {
                    "ok": False,
                    "error": f"Query timeout after {self._timeout} seconds.",
                }
            except ConnectionError:
                _mc_logger.error(f"Connection error when querying {self._address}.")
                resp_dict = {
                    "ok": False,
                    "error": "Connection error.",
                }
            # 设置缓存
            self._cached_dict = resp_dict

        _mc_logger.debug(
            f"Cache set for {self._address}, max age: {self._cache_max_age}."
        )
        self._set_timer()
        return resp_dict

    async def _set_and_clear_cache(self):
        """
        清除缓存的协程任务
        """
        await asyncio.sleep(self._cache_max_age)
        _mc_logger.debug(f"Cache cleared for {self._address}.")
        async with self._cache_lock:
            self._cached_dict = None

    def _set_timer(self):
        """
        设置缓存清除定时器
        """
        asyncio.create_task(self._set_and_clear_cache())
