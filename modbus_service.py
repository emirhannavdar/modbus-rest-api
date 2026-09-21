from pymodbus.client import ModbusTcpClient

from config import (
    MODBUS_HOST,
    MODBUS_PORT,
    MODBUS_DEVICE_ID
)

from database import save_measurement, get_connection

def read_modbus_data(start=None, end=None):

    client = ModbusTcpClient(
        MODBUS_HOST,
        port=MODBUS_PORT
    )
    try:
        if not client.connect():
            raise Exception(
                "Modbus cihazına bağlanılamadı."
            )

        if start is None:
            address = 1
            count = 5

        elif end is None:
            address = start
            count = 1

        else:
            address = start
            count = end - start + 1

        result = client.read_holding_registers(
            address=address,
            count=count,
        )

        if result.isError():
            raise Exception(
                "Modbus register okuma hatası."
            )

        registers = result.registers

        return registers

    finally:
        client.close()

def read_modbus_id(
    id: int
    ):
    client = ModbusTcpClient(
        MODBUS_HOST,
        port=MODBUS_PORT
    )
    try:
        if not client.connect():
            raise Exception(
                "Modbus cihazına bağlanılamadı."
            )
        result = client.read_holding_registers(
            address=id,
            count=1
        )
        if result.isError():
            raise Exception("register okuma hatası")
            
        save_measurement(id, result.registers[0])
        return result.registers[0]

    finally:
        client.close()

def read_modbus_voltage():
    client = ModbusTcpClient(
        MODBUS_HOST,
        port=MODBUS_PORT
    )
    try:
        if not client.connect():
            raise Exception(
                "modbus'a bağlanmadı"
            )

        result = client.read_holding_registers(
            address=1,
            count=1
        )

        if result.isError():
            raise Exception(
                "voltage hatası"
            )

        return result.registers[0]

    finally:
        client.close()

def read_modbus_current():
    client = ModbusTcpClient(
        MODBUS_HOST,
        port=MODBUS_PORT
    )
    try:
        if not client.connect():
            raise Exception(
                "modbus'a bağlanılamadı"
            )
        
        result = client.read_holding_registers(
            address=1,
            count=2
        )

        if result.isError():
            raise Exception(
                "current hatası"
            )
        return result.registers[1]

    finally:
        client.close()

def read_modbus_power():
    client = ModbusTcpClient(
        MODBUS_HOST,
        port=MODBUS_PORT
    )

    try:
        if not client.connect():
            raise Exception(
                "modbus'a bağlanılamadı"
            )
        
        result = client.read_holding_registers(
            address=1,
            count=3
        )

        if result.isError():
            raise Exception(
                "power hatası"
            )
        return result.registers[2]
    finally:
        client.close()

def read_modbus_frekans():
    client = ModbusTcpClient(
        MODBUS_HOST,
        port=MODBUS_PORT
    )

    try:
        if not client.connect():
            raise Exception(
                "modbus'a bağlanılamadı"
            )
        
        result = client.read_holding_registers(
            address=1,
            count=4
        )

        if result.isError():
            raise Exception(
                "power hatası"
            )
        return result.registers[3]
    finally:
        client.close()

def read_modbus_enerji():
    client = ModbusTcpClient(
        MODBUS_HOST,
        port=MODBUS_PORT
    )

    try:
        if not client.connect():
            raise Exception(
                "modbus'a bağlanılamadı"
            )
        
        result = client.read_holding_registers(
            address=1,
            count=5
        )

        if result.isError():
            raise Exception(
                "power hatası"
            )
        return result.registers[4]
    finally:
        client.close()

def read_modbus_temp():
    client = ModbusTcpClient(
        MODBUS_HOST,
        port=MODBUS_PORT
    )

    try:
        if not client.connect():
            raise Exception(
                "modbus'a bağlanılamadı"
            )
        
        result = client.read_holding_registers(
            address=1,
            count=6
        )

        if result.isError():
            raise Exception(
                "power hatası"
            )
        return result.registers[5]
    finally:
        client.close()

def update_modbus_value(id, value):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE measurements
            SET value = ?
            WHERE id = ?
            """,
            (value, id)
        )
        if cursor.rowcount == 0:
            raise Exception(
                "Belirtilen id ile kayıt bulunamadı."
            )
        connection.commit()

        return True
    finally:
        connection.close()