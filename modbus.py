from datetime import datetime
from errno import errorcode

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Generic, TypeVar, Optional, List
from pydantic import BaseModel, Field
from modbus_service import read_modbus_temp, read_modbus_temp_id

modbus = APIRouter()

T = TypeVar("T")

class ModbusDataModel(BaseModel):
    id: int
    device_id: int
    channel_id: int
    value: float
    timestamp: datetime

class RestApiModbus(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] =None
    dateTime: datetime = Field(default_factory=datetime.now)
    errorCode: Optional[int] = None
    errorMessage: Optional[str] = None

    @classmethod
    def ok(cls, data: T):
        return cls(success=True, data=data)

    @classmethod
    def error(cls, message: str, code: Optional[int] = None):
        return cls(success=False, data=None, errorCode=code, errorMessage=message)

@modbus.get('', response_model=RestApiModbus)
def Modbus_endpoint(request: Request):
    if request.query_params:
        error_res = RestApiModbus.error(f"Sayfa Bulunamadı.", 404)
        raise HTTPException(status_code=404, detail=jsonable_encoder(error_res))
    try:
        data = read_modbus_temp()
        formatted_data = [
            ModbusDataModel(
                id=row[0],
                device_id=row[1],
                channel_id=row[2],
                value=row[3],
                timestamp=row[4]
            ) for row in data
        ]
        return RestApiModbus.ok(formatted_data)
    except HTTPException:
        raise
    except Exception as e:
        error_res = RestApiModbus.error(f"Modbus hatası oluştu: {str(e)}", 500)
        return JSONResponse(status_code=500, content=jsonable_encoder(error_res))

@modbus.get('/{id}', response_model=RestApiModbus)
def Modbus(id: int, request: Request):
    if request.query_params:
        error_res = RestApiModbus.error(f"Sayfa Bulunamadı.", 404)
        raise HTTPException(status_code=404, detail=jsonable_encoder(error_res))
    try:
        data = read_modbus_temp_id(id=id)

        if not data:
            error_res = RestApiModbus.error(f"{id} numaralı Modbus cihazı veya verisi bulunamadı.", 404)
            return JSONResponse(status_code=404, content=jsonable_encoder(error_res))

        return RestApiModbus.ok(data)
    except HTTPException:
        raise
    except Exception as e:
        error_res = RestApiModbus.error(f"Modbus hatası oluştu: {str(e)}", 500)
        return JSONResponse(status_code=500, content=jsonable_encoder(error_res))