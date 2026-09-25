import psycopg
from pwdlib import PasswordHash
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


def create_users_table():
    connection = get_connection()
    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                full_name VARCHAR(100),
                email VARCHAR(150) UNIQUE,
                hashed_password TEXT NOT NULL,
                disabled BOOLEAN DEFAULT FALSE
            )
            """
        )

        connection.commit()

    finally:
        connection.close()


password_hash = PasswordHash.recommended()
def add_user(
    username,
    full_name,
    email,
    password,
    disabled=False
):
    print("1")
    hashed_password = password_hash.hash(password)
    print("2")
    connection = get_connection()
    print("3")
    try:
        print("4")
        cursor = connection.cursor()
        print("5")
        cursor.execute(
            """
            INSERT INTO users
            (
                username,
                full_name,
                email,
                hashed_password,
                disabled
            )
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                username,
                full_name,
                email,
                hashed_password,
                disabled
            )
        )

        user_id = cursor.fetchone()[0]

        connection.commit()

        return user_id

    finally:
        connection.close()

def get_user(username):
    connection = get_connection()
    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                username,
                full_name,
                email,
                hashed_password,
                disabled
            FROM users
            WHERE username = %s
            """,
            (username,)
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return {
            "id": row[0],
            "username": row[1],
            "full_name": row[2],
            "email": row[3],
            "hashed_password": row[4],
            "disabled": row[5]
        }

    finally:
        connection.close()

def get_user_by_id(user_id):
    connection = get_connection()
    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                username,
                full_name,
                email,
                hashed_password,
                disabled
            FROM users
            WHERE id = %s
            """,
            (user_id,)
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return {
            "id": row[0],
            "username": row[1],
            "full_name": row[2],
            "email": row[3],
            "hashed_password": row[4],
            "disabled": row[5]
        }

    finally:
        connection.close()

def get_users():
    connection = get_connection()
    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                username,
                full_name,
                email,
                disabled
            FROM users
            ORDER BY id
            """
        )

        rows = cursor.fetchall()

        users = []

        for row in rows:
            users.append({
                "id": row[0],
                "username": row[1],
                "full_name": row[2],
                "email": row[3],
                "disabled": row[4]
            })

        return users

    finally:
        connection.close()

def update_user(
    user_id,
    full_name=None,
    email=None,
    disabled=None
):
    connection = get_connection()
    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE users
            SET
                full_name = COALESCE(%s, full_name),
                email = COALESCE(%s, email),
                disabled = COALESCE(%s, disabled)
            WHERE id = %s
            """,
            (
                full_name,
                email,
                disabled,
                user_id
            )
        )

        updated = cursor.rowcount

        connection.commit()

        return updated > 0

    finally:
        connection.close()

def update_user_password(user_id, hashed_password):
    connection = get_connection()
    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE users
            SET hashed_password = %s
            WHERE id = %s
            """,
            (
                hashed_password,
                user_id
            )
        )

        updated = cursor.rowcount

        connection.commit()

        return updated > 0

    finally:
        connection.close()

def delete_user(user_id):
    connection = get_connection()
    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM users
            WHERE id = %s
            """,
            (user_id,)
        )

        deleted = cursor.rowcount

        connection.commit()

        return deleted > 0

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
            (
                device_id,
                register_address,
                value
            )
        )

        connection.commit()

    finally:
        connection.close()