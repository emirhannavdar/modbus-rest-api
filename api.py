import logging
import time
from time import process_time
from urllib.request import Request
from venv import logger

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from devices import devices
from modbus import modbus


app = FastAPI(
    title="Modbus REST API",
    description="",
    version="1.0.0"
)

logging.basicConfig(
    filename="accsess.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S"
)
logger = logging.getLogger("Modbus REST API")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    dateTime = time.time()
    response = await call_next(request)
    duration = (time.time() - start_time) * 1000

    process_time_str = f"{duration:.2f}ms"
    process_time = datetime.fromtimestamp(dateTime).strftime('%Y-%m-%d %H:%M:%S')

    log_message = f"{response.status_code} - {process_time_str} - {process_time}"

    logger.info(log_message)

    if 200 <= response.status_code < 300:
        logger.info(log_message)
    else:
        logger.error(log_message)
    return response

app.include_router(
    devices,
    prefix="/api/v1/devices",
    tags=["Devices"]
)

app.include_router(
    modbus,
    prefix="/api/v1/modbus",
    tags=["Modbus"]
)
