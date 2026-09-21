from fastapi import FastAPI, HTTPException, APIRouter, Query, Path
from modbus_service import read_modbus_data, read_modbus_id, read_modbus_voltage, read_modbus_current, read_modbus_power, read_modbus_frekans, read_modbus_enerji, read_modbus_temp, update_modbus_value
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI(
    title="Modbus Wattmetre REST API",
    description="Modbus TCP üzerinden elektriksel değerleri okur.",
    version="1.0.0"
)

router = APIRouter(prefix="/api/v1/modbus")

class ModbusRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    start: int = Field(ge=1, le=6)
    end: int = Field(ge=1, le=6)

class ModbusUpdate(BaseModel):
    value: int


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
def getByPower():
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
def getByPower():
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
def getByPower():
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

@router.get("/{id}")
def getBeyIdModbus(id: int):

    if id < 1 or id > 6:
        raise HTTPException(
            status_code=400,
            detail="id 1 ile 6 arasında olmalıdır."
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

@router.put("/{id}/voltage")
def update_modbus(id: int, voltage: float,request: ModbusUpdate):

    if id < 1 or id > 6:
        raise HTTPException(
            status_code=400,
            detail="id 1 ile 6 arasında olmalıdır."
        )

    try:
        update_modbus_value(id, voltage)
        return {
            "success": True,
            "id": id,
            "voltage": voltage,
            "value": request.value
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


app.include_router(router)