from pymodbus.client import ModbusTcpClient

from config import GE, LE

from config import (
    MODBUS_HOST,
    MODBUS_PORT,
    MODBUS_DEVICE_ID
)

from database import save_measurement, get_connection


def get_modbus_client():
    client = ModbusTcpClient(
        MODBUS_HOST,
        port=MODBUS_PORT
    )

    if not client.connect():
        client.close()
        raise Exception(
            "Modbus cihazına bağlanılamadı."
        )

    return client


def read_modbus_data(start=None, end=None):

    client = get_modbus_client()

    try:

        if start is None:
            address = GE
            count = LE

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

    client = get_modbus_client()

    try:

        result = client.read_holding_registers(
            address=id,
            count=1
        )

        if result.isError():
            raise Exception(
                "register okuma hatası"
            )

        value = result.registers[0]

        # Şimdilik mevcut/default cihazı kullanıyoruz.
        # Çoklu cihaz endpointini yazarken burayı device_id
        # üzerinden değiştireceğiz.
        save_measurement(
            MODBUS_DEVICE_ID,
            id,
            value
        )

        return value

    finally:
        client.close()


def read_modbus_voltage():

    client = get_modbus_client()

    try:

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

    client = get_modbus_client()

    try:

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

    client = get_modbus_client()

    try:

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

    client = get_modbus_client()

    try:

        result = client.read_holding_registers(
            address=1,
            count=4
        )

        if result.isError():
            raise Exception(
                "FREKANS HATASI"
            )

        return result.registers[3]

    finally:
        client.close()


def read_modbus_enerji():

    client = get_modbus_client()

    try:

        result = client.read_holding_registers(
            address=1,
            count=5
        )

        if result.isError():
            raise Exception(
                "ENERGY HATASI"
            )

        return result.registers[4]

    finally:
        client.close()


def read_modbus_temp():

    client = get_modbus_client()

    try:

        result = client.read_holding_registers(
            address=1,
            count=6
        )

        if result.isError():
            raise Exception(
                "TEMP hatası"
            )

        fah = result.registers[5]

        temp = (fah - 32) * 5 / 9

        return "{:.2f}".format(temp)

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


def deleteId(id):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM measurements
            WHERE id = ?
            """,
            (id,)
        )

        if cursor.rowcount == 0:
            raise Exception(
                "Belirtilen id ile kayit bulunamadi"
            )

        connection.commit()

        return True

    finally:
        connection.close()


