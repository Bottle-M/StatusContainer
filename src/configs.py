"""
配置模块
"""

from os import environ

# 应用版本
APP_VERSION = environ.get("APP_VERSION", "UNKNOWN")

# 日志目录
APP_LOG_DIR = environ.get("LOG_DIR", "./logs")

# Minecraft 服务器地址
MC_SERVER_ADDR = environ.get("MC_SERVER_ADDR", "127.0.0.1")

# 查询超时时间
MC_QUERY_TIMEOUT = float(environ.get("MC_QUERY_TIMEOUT", 10.0))

# 缓存超时时间
MC_CACHE_MAX_AGE = float(environ.get("MC_CACHE_MAX_AGE", 60.0))
