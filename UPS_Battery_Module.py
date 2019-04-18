import struct
import smbus2
"""
Avg Draw
0.12 A @ Idele
0.19 A with LCD @ Idle
0.5 A  with OP-1 Connected (OTG)
====================== Estimate Battery Life =========================
1000 mAh 0.5 A  Draw - 2 Hours
1000 mAh 0.19 A  Draw - 5.2 Hours
800 mAh 0.5 A  Draw - 1.6 Hours  
800 mAh 0.19 A  Draw - 4.2 Hours  
600 mAh 0.5 A  Draw - 1.2 Hours  
600 mAh 0.19 A  Draw - 3.15 Hours
======================Actual Test========================
1000mAh 0.5A MAX Draw OP-1 Plugged at all time 1h/25m/28s


"""

def readVoltage(bus):
    # "This function returns as float the voltage from the Raspi UPS Hat via the provided SMBus object"
    address = 0x36
    read = bus.read_word_data(address, 2)
    swapped = struct.unpack("<H", struct.pack(">H", read))[0]
    voltage = swapped * 1.25 / 1000 / 16
    return voltage


def readCapacity():
    # "This function returns as a float the remaining capacity of the battery connected to the Raspi UPS Hat via the provided SMBus object"
    bus = smbus2.SMBus(1)
    address = 0x36
    read = bus.read_word_data(address, 4)
    bus.close()
    swapped = struct.unpack("<H", struct.pack(">H", read))[0]
    capacity = swapped / 256
    capacity = int(capacity * 1.1)

    if capacity >= 97:
        return "Full"
    elif capacity < 2:
        return "LOW"
    else:
        return str(capacity) + "%"
