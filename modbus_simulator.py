import asyncio
import random

from pymodbus.simulator import SimData, SimDevice, DataType
from pymodbus.server import ModbusTcpServer

from database import save_measurement


HOST = "127.0.0.1"
PORT = 5020
DEVICE_ID = 1


# ============================================================
# BAŞLANGIÇ DEĞERLERİ
# ============================================================

voltage = 230.0
current = 8.0
power = 1840.0
frequency = 50.0
energy = 12500.0
temperature = 25.0


# ============================================================
# DEĞERLERİ GÜNCELLE
# ============================================================

def generate_values():

    global voltage
    global current
    global power
    global frequency
    global energy
    global temperature

    # --------------------------------------------------------
    # VOLTAGE
    # --------------------------------------------------------

    voltage += random.uniform(-0.8, 0.8)

    voltage = max(
        210.0,
        min(voltage, 250.0)
    )

    # --------------------------------------------------------
    # CURRENT
    # --------------------------------------------------------

    current += random.uniform(-0.5, 0.5)

    current = max(
        0.0,
        min(current, 20.0)
    )

    # --------------------------------------------------------
    # POWER
    # --------------------------------------------------------

    power = voltage * current

    # --------------------------------------------------------
    # FREQUENCY
    # --------------------------------------------------------

    frequency += random.uniform(-0.03, 0.03)

    frequency = max(
        49.5,
        min(frequency, 50.5)
    )

    # --------------------------------------------------------
    # ENERGY
    # --------------------------------------------------------

    energy += power / 3600000

    # --------------------------------------------------------
    # TEMPERATURE
    # --------------------------------------------------------

    temperature += random.uniform(-0.2, 0.2)

    temperature = max(
        15.0,
        min(temperature, 40.0)
    )


# ============================================================
# MODBUS REGISTERLARINI OLUŞTUR
# ============================================================

def create_registers():

    return [

        # Register 1 - Voltage
        int(voltage * 10),

        # Register 2 - Current
        int(current * 100),

        # Register 3 - Power
        int(power),

        # Register 4 - Frequency
        int(frequency * 100),

        # Register 5 - Energy
        int(energy),

        # Register 6 - Temperature
        int(temperature * 10)

    ]


# ============================================================
# POSTGRESQL'E REGISTERLARI KAYDET
# ============================================================

def save_registers_to_database(registers):

    for address, value in enumerate(
        registers,
        start=1
    ):

        save_measurement(
            device_id=DEVICE_ID,
            register_address=address,
            value=value
        )


# ============================================================
# MODBUS REGISTER GÜNCELLEME
# ============================================================

async def update_registers(
    function_code,
    start_address,
    address,
    count,
    current_registers,
    set_values
):

    new_registers = create_registers()

    for i in range(
        min(
            count,
            len(new_registers)
        )
    ):

        index = address - start_address + i

        if 0 <= index < len(current_registers):

            current_registers[index] = new_registers[i]

    return None


# ============================================================
# 1 SANİYELİK VERİ ÜRETİM DÖNGÜSÜ
# ============================================================

async def generate_and_save_loop(
    current_registers
):

    while True:

        # Yeni değerleri üret
        generate_values()

        # Yeni register değerlerini oluştur
        new_registers = create_registers()

        # Modbus registerlarını güncelle
        for i, value in enumerate(new_registers):

            if i < len(current_registers):

                current_registers[i] = value

        # PostgreSQL'e kaydet
        save_registers_to_database(
            new_registers
        )

        # Terminale yazdır
        print(
            f"Voltage={voltage:6.2f} V | "
            f"Current={current:6.2f} A | "
            f"Power={power:7.2f} W | "
            f"Frequency={frequency:5.2f} Hz | "
            f"Energy={energy:8.2f} kWh | "
            f"Temp={temperature:5.2f} C"
        )

        # 1 saniye bekle
        await asyncio.sleep(1)


# ============================================================
# MAIN
# ============================================================

async def main():

    print("=" * 70)
    print(" MODBUS WATTMETRE SIMULATOR")
    print("=" * 70)
    print()

    print(f"IP          : {HOST}")
    print(f"PORT        : {PORT}")
    print(f"DEVICE ID   : {DEVICE_ID}")

    print()

    print("REGISTER HARITASI")
    print("-" * 70)

    print("  1  -> Voltage")
    print("  2  -> Current")
    print("  3  -> Power")
    print("  4  -> Frequency")
    print("  5  -> Energy")
    print("  6  -> Temperature")

    print("-" * 70)
    print()

    # ========================================================
    # İLK REGISTER DEĞERLERİ
    # ========================================================

    initial_registers = create_registers()

    # ========================================================
    # MODBUS DEVICE
    # ========================================================

    device = SimDevice(
        id=DEVICE_ID,

        simdata=SimData(
            address=1,
            count=6,
            values=initial_registers,
            datatype=DataType.UINT16
        ),

        action=update_registers
    )

    # ========================================================
    # MODBUS TCP SERVER
    # ========================================================

    server = ModbusTcpServer(
        device,
        address=(HOST, PORT)
    )

    print("Modbus server başlatılıyor...")
    print()

    await server.serve_forever(
        background=True
    )

    print("Modbus TCP server çalışıyor.")
    print()

    print(
        f"Adres: {HOST}:{PORT}"
    )

    print()

    print("6 adet register aktif.")

    print(
        "Simulator her 1 saniyede yeni değer üretip "
        "PostgreSQL'e kaydedecek."
    )

    print()

    print("Simulator çalışıyor...")
    print("Durdurmak için CTRL+C")
    print()

    # ========================================================
    # ARKA PLANDA VERİ ÜRET
    # ========================================================

    try:

        await generate_and_save_loop(
            device.simdata.values
        )

    except asyncio.CancelledError:

        pass

    finally:

        await server.shutdown()


# ============================================================
# PROGRAMI BAŞLAT
# ============================================================

if __name__ == "__main__":

    try:

        asyncio.run(main())

    except KeyboardInterrupt:

        print()
        print("Simulator durduruldu.")