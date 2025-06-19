from flask import Flask, jsonify
from logger import Logger
from configs import APP_VERSION, MC_SERVER_ADDR, MC_QUERY_TIMEOUT, MC_CACHE_MAX_AGE
from mc import MCStatus

# Logger
app_logger = Logger("app").logger

# MC Status
mc_status = MCStatus(
    MC_SERVER_ADDR, timeout=MC_QUERY_TIMEOUT, cache_max_age=MC_CACHE_MAX_AGE
)

# Flask App
app = Flask(__name__)

@app.route("/")
async def index():
    return jsonify({"message": f"Hello World, BottleM Status API Ver.{APP_VERSION}"})


@app.route("/mcstatus")
async def mcstatus():
    status_dict = await mc_status.get()
    return jsonify(status_dict)
