import sqlcipher3
from config import DATABASE_NAME, DATABASE_PASSWORD

def get_connection():
    connection = sqlcipher3.connect(DATABASE_NAME)

    connection.execute(
        f"PRAGMA key = '{DATABASE_PASSWORD}'"
    )

    return connection


def create_database():
    connection = get_connection()
    cursor = connection.cursor()

    # Cihazlar
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS devices (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            host TEXT NOT NULL,

            port INTEGER NOT NULL DEFAULT 502,

            unit_id INTEGER NOT NULL DEFAULT 1

        )
    """)

    # Register bilgileri
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registers (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            device_id INTEGER NOT NULL,

            register_address INTEGER NOT NULL,

            name TEXT NOT NULL,

            unit TEXT,

            scale INTEGER NOT NULL DEFAULT 1,

            FOREIGN KEY (device_id)
                REFERENCES devices(id),

            UNIQUE(device_id, register_address)

        )
    """)

    # Ölçümler
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS measurements (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            device_id INTEGER NOT NULL,

            register_address INTEGER NOT NULL,

            value INTEGER NOT NULL,

            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (device_id)
                REFERENCES devices(id)

        )
    """)

    connection.commit()
    connection.close()


def add_device(name, host, port=502, unit_id=1):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO devices
            (name, host, port, unit_id)
            VALUES (?, ?, ?, ?)
        """, (
            name,
            host,
            port,
            unit_id
        ))

        connection.commit()

        return cursor.lastrowid

    finally:
        connection.close()


def get_device(device_id):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, name, host, port, unit_id
            FROM devices
            WHERE id = ?
        """, (device_id,))

        return cursor.fetchone()

    finally:
        connection.close()


def get_devices():

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, name, host, port, unit_id
            FROM devices
            ORDER BY id
        """)

        return cursor.fetchall()

    finally:
        connection.close()


def delete_device(device_id):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM devices
            WHERE id = ?
        """, (device_id,))

        if cursor.rowcount == 0:
            raise Exception(
                "Belirtilen cihaz bulunamadı."
            )

        connection.commit()

        return True

    finally:
        connection.close()


def save_measurement(device_id, register_address, value):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO measurements
            (device_id, register_address, value)
            VALUES (?, ?, ?)
        """, (
            device_id,
            register_address,
            value
        ))

        connection.commit()

    finally:
        connection.close()


if __name__ == "__main__":
    create_database()