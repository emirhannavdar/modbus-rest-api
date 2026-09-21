import sqlcipher3 


DATABASE_NAME = "modbus.db"
DATABASE_PASSWORD = "aSdFgHjKlŞi."


def get_connection():

    connection = sqlcipher3.connect(DATABASE_NAME)

    connection.execute(
        f"PRAGMA key = '{DATABASE_PASSWORD}'"
    )

    return connection


def create_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            register_address INTEGER NOT NULL UNIQUE,
            name TEXT NOT NULL,
            unit TEXT,
            scale INTEGER NOT NULL DEFAULT 1
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            register_address INTEGER NOT NULL,
            value INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    registers = [
        (1, "Voltage", "V", 10),
        (2, "Current", "A", 100),
        (3, "Power", "W", 1),
        (4, "Frequency", "Hz", 100),
        (5, "Energy", "kWh", 1)
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO registers
        (register_address, name, unit, scale)
        VALUES (?, ?, ?, ?)
    """, registers)

    connection.commit()
    connection.close()

def save_measurement(register_address, value):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO measurements
        (register_address, value)
        VALUES (?, ?)
    """, (register_address, value))

    connection.commit()
    connection.close()

    
if __name__ == "__main__":

    create_database()

