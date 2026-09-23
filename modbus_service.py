from config import GE, LE, MODBUS_DEVICE_ID
from database import get_connection


def read_modbus_data(start=None, end=None):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        if start is None:
            start = GE
            end = LE
        elif end is None:
            end = start
        if end < start:
            raise Exception(
                "Bitiş registerı başlangıç registerından küçük olamaz."
            )
        cursor.execute(
            """
            SELECT DISTINCT ON (register_address)
                   register_address,
                   value
            FROM measurements
            WHERE device_id = %s
              AND register_address BETWEEN %s AND %s
            ORDER BY register_address, timestamp DESC, id DESC
            """,
            (
                MODBUS_DEVICE_ID,
                start,
                end
            )
        )
        rows = cursor.fetchall()
        if not rows:
            raise Exception(
                "Belirtilen register için veri bulunamadı."
            )
        values = {
            row[0]: row[1]
            for row in rows
        }
        return [
            values[address]
            for address in range(start, end + 1)
            if address in values
        ]
    finally:
        connection.close()


def read_modbus_id(id: int):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT value
            FROM measurements
            WHERE device_id = %s
              AND register_address = %s
            ORDER BY timestamp DESC
            LIMIT 1
            """,
            (
                MODBUS_DEVICE_ID,
                id
            )
        )
        row = cursor.fetchone()
        if row is None:
            raise Exception(
                "Belirtilen register bulunamadı."
            )
        return row[0]
    finally:
        connection.close()


def read_modbus_voltage():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT value
            FROM measurements
            WHERE device_id = %s
              AND register_address = 1
            ORDER BY timestamp DESC
            LIMIT 1
            """,
            (MODBUS_DEVICE_ID,)
        )

        row = cursor.fetchone()
        if row is None:
            raise Exception(
                "Voltage verisi bulunamadı."
            )

        return row[0]
    finally:
        connection.close()


def read_modbus_current():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT value
            FROM measurements
            WHERE device_id = %s
              AND register_address = 2
            ORDER BY timestamp DESC
            LIMIT 1
            """,
            (MODBUS_DEVICE_ID,)
        )

        row = cursor.fetchone()
        if row is None:
            raise Exception(
                "Current verisi bulunamadı."
            )
        return row[0]
    finally:
        connection.close()


def read_modbus_power():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT value
            FROM measurements
            WHERE device_id = %s
              AND register_address = 3
            ORDER BY timestamp DESC
            LIMIT 1
            """,
            (MODBUS_DEVICE_ID,)
        )

        row = cursor.fetchone()
        if row is None:
            raise Exception(
                "Power verisi bulunamadı."
            )
        return row[0]
    finally:
        connection.close()


def read_modbus_frekans():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT value
            FROM measurements
            WHERE device_id = %s
              AND register_address = 4
            ORDER BY timestamp DESC
            LIMIT 1
            """,
            (MODBUS_DEVICE_ID,)
        )

        row = cursor.fetchone()
        if row is None:

            raise Exception(
                "Frequency verisi bulunamadı."
            )
        return row[0]
    finally:
        connection.close()


def read_modbus_enerji():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT value
            FROM measurements
            WHERE device_id = %s
              AND register_address = 5
            ORDER BY timestamp DESC
            LIMIT 1
            """,
            (MODBUS_DEVICE_ID,)
        )

        row = cursor.fetchone()
        if row is None:
            raise Exception(
                "Energy verisi bulunamadı."
            )
        return row[0]
    finally:
        connection.close()


def read_modbus_temp():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT value
            FROM measurements
            WHERE device_id = %s
              AND register_address = 9
            ORDER BY timestamp DESC
            LIMIT 1
            """,
            (MODBUS_DEVICE_ID,)
        )

        row = cursor.fetchone()
        if row is None:
            raise Exception(
                "Temperature verisi bulunamadı."
            )
        temp = row[0] / 10
        return f"{temp:.2f}"
    finally:
        connection.close()

def AddUser():
    asd

def update_modbus_value(id, value):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE measurements
            SET value = %s
            WHERE id = %s
            """,
            (
                value,
                id
            )
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
            WHERE id = %s
            """,
            (id,)
        )

        if cursor.rowcount == 0:
            raise Exception(
                "Belirtilen id ile kayıt bulunamadı."
            )
        connection.commit()
        return True
    finally:
        connection.close()