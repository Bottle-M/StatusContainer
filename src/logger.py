"""
日志记录器
"""

import traceback
import os
import logging
from logging.handlers import RotatingFileHandler
from configs import APP_LOG_DIR


class __CustomLogger(logging.Logger):
    # 魔改logger，针对logger.error方法加入traceback输出
    def error(self, msg, *args, **kwargs):
        # 调用父类的 error 方法
        super().error(f"{msg} \n {traceback.format_exc()}", *args, **kwargs)


logging.setLoggerClass(__CustomLogger)


class Logger:
    """
    日志记录模块
    """

    def __init__(self, name: str):
        """
        :param name: 要记录日志的模块名称，用于分模块记录日志
        """
        self._logger = logging.getLogger(f"logger_{name}")
        self._logger.setLevel(logging.DEBUG)
        # 日志目录不存在则建立, 全可读写权限
        if not os.path.exists(APP_LOG_DIR):
            os.makedirs(APP_LOG_DIR, mode=0o777)
        # 文件输出器
        self._file_handler = RotatingFileHandler(
            os.path.join(APP_LOG_DIR, f"{name}.log"),
            maxBytes=1024 * 1024 * 10,  # 10 MB
            backupCount=10,  # 保留 10 个备份
        )
        self._file_handler.setLevel(logging.INFO)
        # 控制台输出器
        self._console_handler = logging.StreamHandler()
        self._console_handler.setLevel(logging.DEBUG)
        # 定义打印格式
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s"
        )
        self._file_handler.setFormatter(formatter)
        self._console_handler.setFormatter(formatter)
        self._logger.addHandler(self._file_handler)
        self._logger.addHandler(self._console_handler)
        self._logger.debug("Logger initialized.")

    @property
    def logger(self) -> logging.Logger:
        return self._logger
