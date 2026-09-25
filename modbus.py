from errno import errorcode

from fastapi import APIRouter, HTTPException, Query
from typing import Generic, TypeVar, Optional
from pydantic import BaseModel
from modbus_service import read_modbus_temp, read_modbus_temp_id

modbus = APIRouter()

T = TypeVar("T")

class RestApiModbus(BaseModel, Generic[T]):
    success: bool
    data: T
    errorCode: Optional[int] = None
    errorMessage: Optional[T] = None

    @classmethod
    def ok(cls, data: T) -> T:
        return cls(success=True, data=data)
    @classmethod
    def error(cls, data: T, message: str, code: Optional[int] = None) -> T:
        return cls(success=False, data=None, errorCode=code, errorMessage=message)

@modbus.get('')
def Modbus_endpoint():
    try:
        data = read_modbus_temp()
        return RestApiModbus.ok(data)
    except HTTPException:
        raise
    except Exception as e:
        error_res = RestApiModbus.error(None, f"Modbus hatası oluştu: {str(e)}", 500)
        raise HTTPException(
            status_code=500,
            detail=error_res.dict()
        )

@modbus.get('/{id}')
def Modbus(id: int):
    try:
        data = read_modbus_temp_id(id=id)
        if not data:
            error_res = RestApiModbus.error(None, f"{id} numaralı Modbus cihazı veya verisi bulunamadı.", 404)
            raise HTTPException(
                status_code=404,
                detail=error_res.dict()
            )

        return RestApiModbus.ok(data)
    except HTTPException:
        raise
    except Exception as e:
        error_res = RestApiModbus.error(None, f"Modbus hatası oluştu: {str(e)}", 500)
        raise HTTPException(
            status_code=500,
            detail=error_res.dict()
        )