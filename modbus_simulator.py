import asyncio
import random

from pymodbus.simulator import SimData, SimDevice, DataType
from pymodbus.server import ModbusTcpServer


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

power_factor = 0.95
reactive_power = 600.0
apparent_power = 1936.0

temperature = 25.0

voltage_min = 225.0
voltage_max = 235.0

current_min = 5.0
current_max = 12.0

active_power = 1840.0

reactive_energy = 3500.0
apparent_energy = 4200.0

daily_energy = 125.0
monthly_energy = 3250.0

temperature_max = 30.0
temperature_min = 20.0


# ============================================================
# DEĞERLERİ GÜNCELLE
# ============================================================

def generate_values():

    global voltage
    global current
    global power
    global frequency
    global energy

    global power_factor
    global reactive_power
    global apparent_power

    global temperature

    global voltage_min
    global voltage_max

    global current_min
    global current_max

    global active_power

    global reactive_energy
    global apparent_energy

    global daily_energy
    global monthly_energy

    global temperature_max
    global temperature_min


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

    active_power = power


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

    daily_energy += power / 3600000

    monthly_energy += power / 3600000


    # --------------------------------------------------------
    # POWER FACTOR
    # --------------------------------------------------------

    power_factor += random.uniform(-0.01, 0.01)

    power_factor = max(
        0.80,
        min(power_factor, 1.00)
    )


    # --------------------------------------------------------
    # REACTIVE POWER
    # --------------------------------------------------------

    reactive_power = power * (
        (1 - power_factor ** 2) ** 0.5
        / power_factor
    )


    # --------------------------------------------------------
    # APPARENT POWER
    # --------------------------------------------------------

    apparent_power = power / power_factor


    # --------------------------------------------------------
    # TEMPERATURE
    # --------------------------------------------------------

    temperature += random.uniform(-0.2, 0.2)

    temperature = max(
        15.0,
        min(temperature, 40.0)
    )


    # --------------------------------------------------------
    # MIN / MAX DEĞERLER
    # --------------------------------------------------------

    voltage_min = min(
        voltage_min,
        voltage
    )

    voltage_max = max(
        voltage_max,
        voltage
    )


    current_min = min(
        current_min,
        current
    )

    current_max = max(
        current_max,
        current
    )


    temperature_min = min(
        temperature_min,
        temperature
    )

    temperature_max = max(
        temperature_max,
        temperature
    )


    # --------------------------------------------------------
    # ENERJİLER
    # --------------------------------------------------------

    reactive_energy += reactive_power / 3600000

    apparent_energy += apparent_power / 3600000


# ============================================================
# MODBUS REGISTERLARINI OLUŞTUR
# ============================================================

def create_registers():

    return [

        # Register 1
        int(voltage * 10),

        # Register 2
        int(current * 100),

        # Register 3
        int(power),

        # Register 4
        int(frequency * 100),

        # Register 5
        int(energy),

        # Register 6
        int(power_factor * 100),

        # Register 7
        int(reactive_power),

        # Register 8
        int(apparent_power),

        # Register 9
        int(temperature * 10),

        # Register 10
        int(voltage_min * 10),

        # Register 11
        int(voltage_max * 10),

        # Register 12
        int(current_min * 100),

        # Register 13
        int(current_max * 100),

        # Register 14
        int(active_power),

        # Register 15
        int(reactive_energy),

        # Register 16
        int(apparent_energy),

        # Register 17
        int(daily_energy),

        # Register 18
        int(monthly_energy),

        # Register 19
        int(temperature_max * 10),

        # Register 20
        int(temperature_min * 10)

    ]


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

    generate_values()

    new_registers = create_registers()


    for i in range(min(count, len(new_registers))):

        index = address - start_address + i

        if 0 <= index < len(current_registers):

            current_registers[index] = new_registers[i]


    print(
        f"Voltage={voltage:6.2f} V | "
        f"Current={current:6.2f} A | "
        f"Power={power:7.2f} W | "
        f"Frequency={frequency:5.2f} Hz | "
        f"Energy={energy:8.2f} kWh | "
        f"Temp={temperature:5.2f} C"
    )

    return None


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
    print("  6  -> Power Factor")
    print("  7  -> Reactive Power")
    print("  8  -> Apparent Power")
    print("  9  -> Temperature")
    print(" 10  -> Voltage Min")
    print(" 11  -> Voltage Max")
    print(" 12  -> Current Min")
    print(" 13  -> Current Max")
    print(" 14  -> Active Power")
    print(" 15  -> Reactive Energy")
    print(" 16  -> Apparent Energy")
    print(" 17  -> Daily Energy")
    print(" 18  -> Monthly Energy")
    print(" 19  -> Temperature Max")
    print(" 20  -> Temperature Min")

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

            count=20,

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

    print("20 adet register aktif.")

    print(
        "API üzerinden okuma yapıldığında "
        "register değerleri güncellenecek."
    )

    print()

    print("Simulator çalışıyor...")
    print("Durdurmak için CTRL+C")
    print()


    try:

        while True:

            await asyncio.sleep(1)


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