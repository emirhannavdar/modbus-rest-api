import json

from config import GE, LE, MODBUS_DEVICE_ID
from database import get_connection
from psycopg2.extras import RealDictCursor
import json

def get_devices():
    connection = get_connection()
    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, name, host, port, unit_id
            FROM devices
            ORDER BY id
            """
        )
        rows = cursor.fetchall()

        devices = []

        for row in rows:
            devices.append({
                "id": row[0],
                "name": row[1],
                "host": row[2],
                "port": row[3],
                "unit_id": row[4]
            })

        return devices

    finally:
        connection.close()

def getIdDevice(id):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id, name, host, port, unit_id
            FROM devices
            WHERE id = %s
            """, (id,)
        )
        row = cursor.fetchone()

        if row is None:
            return None

        device_dict = {
            "id": row[0],
            "name": row[1],
            "host": row[2],
            "port": row[3],
            "unit_id": row[4]
        }
        return json.dumps(device_dict)

    finally:
        connection.close()

def read_modbus_temp():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT *
            FROM measurements
            ORDER BY id DESC
            LIMIT 50
            """,
            
        )

        row = cursor.fetchall()
        if row is None:
            raise Exception(
                "Temperature verisi bulunamadı."
            )
        
        return row
    finally:
        connection.close()

def read_modbus_temp_id(id):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT *
            FROM measurements
            WHERE id = %s
            """, (id,)
            
        )

        row = cursor.fetchall()
        if not row:
            return None

        columns = [desc[0] for desc in cursor.description]
        result= [dict(zip(columns, row)) for row in row]

        return result

    finally:
        connection.close()

def add_device(name, host, port=502, unit_id=1):
    connection = get_connection()
    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO devices (name, host, port, unit_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,
            (name, host, port, unit_id)
        )

        device_id = cursor.fetchone()[0]

        connection.commit()

        return device_id

    finally:
        connection.close()


