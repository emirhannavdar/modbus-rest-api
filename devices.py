from calendar import error

from fastapi import APIRouter, HTTPException, Query
from modbus_service import get_devices, getIdDevice, add_device
from typing import Generic, TypeVar, Optional
from pydantic import BaseModel
import datetime

devices = APIRouter()

T = TypeVar("T")

class RestApiDevices(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    errorCode: Optional[int] = None
    errorMessage: Optional[str] = None

    @classmethod
    def ok(cls, data: T) -> T:
        return cls(success=True, data=data)

    @classmethod
    def error(cls, data: T, message: str, code: Optional[int] = None) -> T:
        return cls(success=False, data=None, errorCode=code, errorMessage=message)

@devices.get('')
def get_devices_endpoint():
    try:
        data = get_devices()
        return RestApiDevices.ok(data)

    except HTTPException:
        raise

    except Exception as e:
        error_res = RestApiDevices.error(None, f"Cihazlar listelenirken hata oluştu: {str(e)}", 500)
        raise HTTPException(
            status_code=500,
            detail=error_res.dict()
        )


@devices.get('/{id}')
def get_device_endpoint(id: int):
    try:
        data = getIdDevice(id=id)

        if data is None or data == {}:
            error_res = RestApiDevices.error(None, f"{id} numaralı cihaz veya verisi bulunamadı.", 404)
            raise HTTPException(
                status_code=404,
                detail=error_res.dict()
            )
        return RestApiDevices.ok(data)
    except HTTPException:
        raise

    except Exception as e:
        error_res = RestApiDevices.error(None, f"Cihaz hatası oluştu: {str(e)}", 500)
        raise HTTPException(
            status_code=500,
            detail=error_res.dict()
        )


@devices.post('')
def create_device(
    name: str,
    host: str
):
    try:
        device_id = add_device(
            name=name,
            host=host
        )

        return {
            "success": True,
            "data": device_id
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
