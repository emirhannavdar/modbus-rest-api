from fastapi import FastAPI, HTTPException, APIRouter, Query, Path, Request, Depends, status
from modbus_service import read_modbus_data, read_modbus_id, read_modbus_voltage, read_modbus_current, read_modbus_power, read_modbus_frekans, read_modbus_enerji, read_modbus_temp, update_modbus_value, deleteId, AddUser
from pydantic import BaseModel, ConfigDict, Field
from config import GE, LE, ACCESS_TOKEN_EXPIRE_MINUTES
from database import add_device, get_devices, delete_device, get_device
from auth import get_current_active_user, Token, authenticate_user, create_access_token, fake_users_db
from typing import Annotated
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI(
    title="Modbus REST API",
    description="",
    version="1.0.0"
)

router = APIRouter(
    prefix="/api/v1/modbus",
    dependencies=[Depends(get_current_active_user)]
)

class ModbusRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    start: int = Field(ge=GE, le=LE)
    end: int = Field(ge=GE, le=LE)

class ModbusUpdate(BaseModel):
    model_config = ConfigDict()

    id: int
    voltage: float

class ModbusDevice(BaseModel):
    model_config = ConfigDict()
    name: str
    host: str

class ModbusDevices(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: int

class ModbusAddUser(BaseModel):
    model_config = ConfigDict(extra="forbid")
    username: str
    full_name: str
    email: str
    password: str

@app.post("/token")
async def login_for_accestoken(
    form_data: Annotated[
        OAuth2PasswordRequestForm,
        Depends()
    ]
) -> Token:
    user = authenticate_user(
        fake_users_db,
        form_data.username,
        form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="hatalı kullanıcı adı şifre",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )
    
    acces_token_expires = timedelta(
        minutes = ACCESS_TOKEN_EXPIRE_MINUTES
    )

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=acces_token_expires
    )

    return Token(
        access_token=access_token,
        token_type="bearer"
    )

@router.post("/add/user")
def add_User(request= ModbusAddUser):
    try:
        add_user = AddUser(request.username, request.full_name, request.email, request.password)
        return {
            "success": True,
            "data": add_user
        }
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="kullanici olusturulamadi"
        )

@router.post("/")
def getModbus(request: ModbusRequest):

    if request.end < request.start:
        raise HTTPException(
            status_code=400,
            detail="end, start değerinden küçük olamaz."
        )

    try:
        data = read_modbus_data(
            start=request.start,
            end=request.end
        )

        return {
            "success": True,
            "data": data
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/voltage")
def get_voltage():
    try:
        data = read_modbus_voltage()

        return {
            "success": True,
            "voltage": data,
            "unit": "V"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/current")
def get_current():
    try:
        data = read_modbus_current()

        return {
            "success": True,
            "current": data,
            "unit": "A"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/power")
def getByPower():
    try:
        data = read_modbus_power()

        return {
            "success": True,
            "current": data,
            "unit": "W"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/frequency")
def getByFrekans():
    try:
        data = read_modbus_frekans()

        return {
            "success": True,
            "frekans": data,
            "unit": "Hz"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/energy")
def getByEnergy():
    try:
        data = read_modbus_enerji()

        return {
            "success": True,
            "energy": data,
            "unit": "kWh"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/temp")
def getByTemp():
    try:
        data = read_modbus_temp()

        return {
            "success": True,
            "temp": data,
            "unit": "C"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/devices")
def devices():
    try:
        devices = get_devices()
        return {
            "success": True,
            "devices": devices
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/devices/{id}")
def getDevices(request: ModbusDevices):
    try:
        getDevice = get_device(device_id=request.id)
        return {
            "success": True,
            "data": getDevice
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/{id}")
def getBeyIdModbus(id: int):

    if id < GE or id > LE:
        raise HTTPException(
            status_code=400,
            detail=f"id {GE} ile {LE} arasında olmalıdır."
        )

    try:
        data = read_modbus_id(id)

        return {
            "success": True,
            "data": data
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.delete("/Devices/Delete/{id}")
def DeleteDevices(request: ModbusDevices):
    try:
        deletedevice = delete_device(device_id = request.id)
        return {
            "success": True,
            "id": request.id
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )        

@router.post("/addDevices")
def AddDevice(request: ModbusDevice):
    try:
        device_id = add_device(name=request.name, host=request.host)
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

@router.delete("/{id}")
def delete_id(request: ModbusDevices):
    try:
        deleteId(request.id)
        return {
            "succes": True,
            "id": request.id,
            "detail": "silindi"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.put("/{id}/voltage")
def update_modbus(request: ModbusUpdate):

    if request.id < GE or request.id > LE:
        raise HTTPException(
            status_code=400,
            detail=f"id {GE} ile {LE} arasinda olmalidir."
        )

    try:
        update_modbus_value(request.id, request.voltage)
        return {
            "success": True,
            "id": request.id,
            "voltage": request.voltage,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


app.include_router(router)