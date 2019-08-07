import struct
from math import floor
from os.path import join

import smbus2

from FileBrowser import scale
from config import config, batteryConfig

# import Adafruit_ADS1x15
LIPO_MIN_VOLTAGE = 3.6
LIPO_MAX_VOLTAGE = 4.2

FULL_BATT_PERCENTAGE = 97
LOW_BATT_PERCENTAGE = 5

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


def readVoltage():
    # if(config["OP_1_Mounted_Dir"] == "RaspiUPS"):
    return readVoltageRaspiUPS()

    # if(config["OP_1_Mounted_Dir"] == "ADS1115"):
    #    return readVoltageADS1115()

    # return 4.2 #default max voltage


def readCapacity():
    # if (config["OP_1_Mounted_Dir"] == "RaspiUPS"):
    return readCapacityRaspiUPS()

    # if (config["OP_1_Mounted_Dir"] == "ADS1115"):
    #    return readCapacityADS1115()

    # return "100%"


# =============================For ADS1115 ADC voltage reading =============================
# Not supported yet

# read voltage from
# def readVoltageADS1115():
#    adc = Adafruit_ADS1x15.ADS1115()
# "This function reads the channel 0 voltage from the ADS1115"
#    GAIN = 2/3 # 0-6.14V
#    val = adc.read_adc(0, GAIN=1)
#    return val


# def readCapacityADS1115():
# "This function calculates the remaining batter capacity from the battery voltage read from the ADS1115"
#    voltage = readCapacityADS1115()
#    percentage = (voltage - LIPO_MIN_VOLTAGE) * (100 - 0) / (LIPO_MAX_VOLTAGE - LIPO_MIN_VOLTAGE) + 0 # MAPS THE VOLTAGE 4.2-3.6 to 0->100%
#    capacity = int(percentage)
#    if capacity >= FULL_BATT_PERCENTAGE:
#        return "FULL"
#    elif capacity < LOW_BATT_PERCENTAGE:
#        return "LOW"
#    else:
#        return str(capacity) + "%"

enable = batteryConfig["enable"]

def getBatteryImagePath(percentage):
    ImageFolder = "Assets/Img/battery/ST_1"
    return join(ImageFolder, str(int(floor(percentage * 0.1))) + ".png")


# ============================= For UPS-Lite Battery Module =============================
def readVoltageRaspiUPS():
    # "This function returns as float the voltage from the Raspi UPS Hat via the provided SMBus object"
    if enable:
        bus = smbus2.SMBus(1)
        address = 0x36
        read = bus.read_word_data(address, 2)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        voltage = swapped * 1.25 / 1000 / 16
        bus.close()
        return voltage
    else:
        return 0


def readCapacityRaspiUPS():
    # "This function returns as a float the remaining capacity of the battery connected to the Raspi UPS Hat via the provided SMBus object"
    if  enable:
        bus = smbus2.SMBus(1)
        address = 0x36
        read = bus.read_word_data(address, 4)
        bus.close()
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        capacity = swapped / 256
        capacity = int(capacity)
        return capacity
    else:
        return 0
    # if capacity >= FULL_BATT_PERCENTAGE:
    #     return "FULL"
    # elif capacity < LOW_BATT_PERCENTAGE:
    #     return "LOW"
    # else:
    #     return str(capacity) + "%"

