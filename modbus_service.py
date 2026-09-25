import json

from config import GE, LE, MODBUS_DEVICE_ID
from database import get_connection
from psycopg2.extras import RealDictCursor
from psycopg.rows import dict_row
import json

def getDevices():
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
        if not row:
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

        rows = cursor.fetchall()
        if not rows:
            return None

        columns = [desc[0] for desc in cursor.description]
        result= [dict(zip(columns, row)) for row in rows]

        return result

    finally:
        connection.close()

def add_device(name, host, port=502, unit_id=1):
    connection = get_connection()
    try:
        cursor = connection.cursor(row_factory=dict_row)

        cursor.execute(
            """
            INSERT INTO devices (name, host, port, unit_id)
            VALUES (%s, %s, %s, %s)
            RETURNING *
            """,
            (name, host, port, unit_id)
        )

        device_id = cursor.fetchall()

        connection.commit()

        return device_id

    finally:
        connection.close()


def up_device(
        id,
        name,
        host,
        port,
        unit_id
):
    connection = get_connection()
    try:
        cursor = connection.cursor(row_factory=dict_row)
        cursor.execute(
            """
            UPDATE devices
            SET name = %s, host = %s, port = %s, unit_id = %s
            WHERE id = %s
            RETURNING *
            """, (name, host, port, unit_id, id)
        )

        up_dev = cursor.fetchall()
        connection.commit()
        return up_dev
    finally:
        connection.close()

def del_device(id):
    connection = get_connection()
    try:
        cursor = connection.cursor(row_factory=dict_row)
        cursor.execute(
            """
            DELETE FROM devices WHERE id = %s RETURNING *
            """, (id,)
        )
        del_dev = cursor.fetchall()
        connection.commit()
        return del_dev
    finally:
        connection.close()

def patch_dev(id, name, host, port, unit_id):
    connection = get_connection()
    try:
        cursor = connection.cursor(row_factory=dict_row)
        sql = """UPDATE devices SET"""
        value = []
        where = """"""

        if name is not None:
            where += f""" , name = %s """
            value.append(name)

        if host is not None:
            where += f""" , host = %s """
            value.append(host)

        if port is not None:
            where += f""" , port = %s """
            value.append(port)
        if unit_id is not None:
            where += f""" , unit_id = %s """
            value.append(unit_id)

        sql += where[2:] + """ WHERE id = %s RETURNING *"""

        value.append(id)

        cursor.execute(sql, tuple(value))
        update_row = cursor.fetchone()

        return update_row
    finally:
        connection.close()
