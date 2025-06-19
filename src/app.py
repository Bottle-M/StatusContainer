from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from logger import Logger
from configs import (
    APP_VERSION,
    MC_SERVER_ADDR,
    MC_QUERY_TIMEOUT,
    MC_CACHE_MAX_AGE,
    ALLOWED_CORS_ORIGINS,
)
from mc import MCStatus

# Logger
app_logger = Logger("app").logger

# MC Status
mc_status = MCStatus(
    MC_SERVER_ADDR, timeout=MC_QUERY_TIMEOUT, cache_max_age=MC_CACHE_MAX_AGE
)

# Flask App
app = FastAPI(title="Minecraft Status API", version=APP_VERSION)

# 根据 https://github.com/fastapi/fastapi/issues/1663 的讨论
# 下面两个必不可少，而且似乎不支持 Access-Control-Allow-Origin='*' 的情况

@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = ", ".join(ALLOWED_CORS_ORIGINS)
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app_logger.info(f"Allowed CORS origins: {ALLOWED_CORS_ORIGINS}")


@app.get("/")
async def index():
    return {"message": f"Hello World, BottleM Status API Ver.{APP_VERSION}"}


@app.get("/mcstatus")
async def mcstatus():
    status_dict = await mc_status.get()
    return status_dict
