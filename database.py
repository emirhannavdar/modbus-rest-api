import psycopg

from config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD
)


def get_connection():
    return psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


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


def get_device(device_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, name, host, port, unit_id
            FROM devices
            WHERE id = %s
            """,
            (device_id,)
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return {
            "id": row[0],
            "name": row[1],
            "host": row[2],
            "port": row[3],
            "unit_id": row[4]
        }

    finally:
        connection.close()


def delete_device(device_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM devices
            WHERE id = %s
            """,
            (device_id,)
        )

        deleted = cursor.rowcount

        connection.commit()

        return deleted > 0

    finally:
        connection.close()


def save_measurement(device_id, register_address, value):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO measurements
            (device_id, register_address, value)
            VALUES (%s, %s, %s)
            """,
            (device_id, register_address, value)
        )

        connection.commit()

    finally:
        connection.close()