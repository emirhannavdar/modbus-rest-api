import sqlcipher3

DATABASE_NAME = "modbus.db"
DATABASE_PASSWORD = "aSdFgHjKlŞi."


connection = sqlcipher3.connect(DATABASE_NAME)

connection.execute(
    f"PRAGMA key = '{DATABASE_PASSWORD}'"
)

cursor = connection.cursor()

cursor.execute("""
    SELECT
        id,
        register_address,
        name,
        unit,
        scale
    FROM registers
    ORDER BY register_address
""")

rows = cursor.fetchall()

print()
print("========== MODBUS DATABASE ==========")
print()

print(
    f"{'ID':<5}"
    f"{'ADDRESS':<10}"
    f"{'NAME':<15}"
    f"{'UNIT':<10}"
    f"{'SCALE':<5}"
)

print("-" * 45)

for row in rows:
    print(
        f"{row[0]:<5}"
        f"{row[1]:<10}"
        f"{row[2]:<15}"
        f"{row[3]:<10}"
        f"{row[4]:<5}"
    )

print()
print("======================================")

connection.close()