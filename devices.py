import calendar
from calendar import error

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.encoders import jsonable_encoder
from modbus_service import get_devices, getIdDevice, add_device, up_device, del_device, patch_dev
from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, ConfigDict, Field
from psycopg.rows import dict_row

from datetime import datetime
from typing_extensions import Self
import json

devices = APIRouter()

T = TypeVar("T")

class RestApiDevices(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    dateTime: datetime = Field(default_factory=datetime.now)
    errorCode: Optional[int] = None
    message: Optional[str] = None


    @classmethod
    def ok(cls, data: T, message: Optional[str]) -> T:
        return cls(success=True, data=data, message=message)

    @classmethod
    def error(cls, message: str, code: Optional[int] = None) -> T:
        return cls(success=False, data=None, errorCode=code, message=message)


class ModBusDevicesPost(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    host: str

class ModBusDevicesPut(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    unit_id: Optional[int] = None

class ModBusDevicesDel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: Optional[str] = None
    port: Optional[int] = None

class ModBusDevicesPatch(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    unit_id: Optional[int] = None

@devices.get('')
def get_devices_endpoint(request: Request):
    if request.query_params:
        error_res= RestApiDevices.error(f"geçersiz sayfa", code=404)
        raise HTTPException(
            status_code=404,
            detail=jsonable_encoder(error_res)
        )
    try:
        data = get_devices()
        return RestApiDevices.ok(data, f"BASARILI")

    except HTTPException:
        raise

    except Exception as e:
        error_res = RestApiDevices.error(f"Cihazlar listelenirken hata oluştu: {str(e)}", 500)
        raise HTTPException(
            status_code=500,
            detail=jsonable_encoder(error_res)
        )


@devices.get('/{id}')
def get_device_endpoint(id: int, request: Request):
    if  request.query_params:
        error_res = RestApiDevices.error(f"geçersiz sayfa", code=404)
        raise HTTPException(
            status_code=404,
            detail=jsonable_encoder(error_res)
        )

    try:
        data = getIdDevice(id=id)

        if isinstance(data, str):
            data = json.loads(data)
        else:
            data = data

        if data is None or data == {}:
            error_res = RestApiDevices.error(f"{id} numaralı cihaz veya verisi bulunamadı.", 404)
            raise HTTPException(
                status_code=404,
                detail=jsonable_encoder(error_res)
            )
        return RestApiDevices.ok(data, "BASARILI")
    except HTTPException:
        raise

    except Exception as e:
        error_res = RestApiDevices.error(f"Cihaz hata oluştu: {str(e)}", 500)
        raise HTTPException(
            status_code=500,
            detail=jsonable_encoder(error_res)
        )


@devices.post('')
def create_device(raw: ModBusDevicesPost, request: Request):
    try:
        device_id = add_device(
            name=raw.name,
            host=raw.host
        )

        return RestApiDevices.ok(device_id, "BASARILI")

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@devices.put('/{id}')
def update_device_endpoint(id: int, raw: ModBusDevicesPut, request: Request):
    try:
        device_up = up_device(
            id = id,
            name = raw.name,
            host = raw.host,
            port = raw.port,
            unit_id = raw.unit_id
        )
        return RestApiDevices.ok(device_up, "BASARILI")

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@devices.delete('/{id}')
def del_devicess_endpoint(id: int, raw: ModBusDevicesDel, request: Request):
    try:
        device_del = del_device(
            id = id,
            name = raw.name,
            port = raw.port
        )
        return RestApiDevices.ok(device_del, "BASARILI")
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@devices.patch('/{id}')
def patch_devices_endpoint(id: int, raw: ModBusDevicesPatch, request: Request):
    try:
        data = patch_dev(id=id, name=raw.name, host=raw.host, port=raw.port, unit_id=raw.unit_id)
        if isinstance(data, str):
            data = json.loads(data)
        else:
            data = data

        if data is None or data == {}:
            error_res = RestApiDevices.error(f"{id} numaralı cihaz veya verisi bulunamadı.", 404)
            raise HTTPException(
                status_code=404,
                detail=jsonable_encoder(error_res)
            )

        return RestApiDevices.ok(data, "BASARILI")
    except HTTPException:
        raise
