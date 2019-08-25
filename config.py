import json
import os
from file_util import forcedir

workDir = os.path.dirname(os.path.realpath(__file__))

config = {
    # USB unique ID to help identify devices
    "OP_1_USB_ID": "*OP-1*",
    "OP_Z_USB_ID": "*OP-Z*",
    "USB_VENDOR": 0x2367,
    "USB_PRODUCT": 0x0002,
    "OP-Z_USB_PRODUCT": 0x000c,

    # Device path not yet mounted
    "USB_Mount_Path": "",

    # Updates once device successfully mounted
    "OP_1_Mounted_Dir": "",
    "OP_Z_Mounted_Dir": "",

    # Target device Mount Point
    "TargetOp1MountDir": "/media/op1",
    "TargetOpZMountDir": "/media/opz",

    # Local Backup folders
    # "OP1BackupPath": os.path.dirname(os.path.realpath(__file__)) + "/files/OP_1_Backup_Library/",
    # "OPZBackupPath": os.path.dirname(os.path.realpath(__file__)) + "/files/OP_Z_Backup_Library/",
    "OP1BackupPath": os.path.join("/home/pi/", "files/OP_1_Backup_Library/"),
    "OPZBackupPath": os.path.join("/home/pi/", "files/OP_Z_Backup_Library/"),

    # Max allowed patches for OP1
    "Max_Synth_Sampler_patches": 42,
    "Max_Synth_Synthesis_patches": 100,
    "Max_Drum_Patches": 42,
}

# For path referencing use. DO NOT change
savePaths = {
    "OP_1_System_Path": config["OP_1_Mounted_Dir"],
    # Local OP1 Backup Paths
    "Local_Dir": config["OP1BackupPath"],
    "Local_Projects": config["OP1BackupPath"] + "projects",
    "Local_Patches": config["OP1BackupPath"] + "patches",
    "Local_Synth": config["OP1BackupPath"] + "patches/synth",
    "Local_Drum": config["OP1BackupPath"] + "patches/drum",
    # Local OPZ Backup Paths
    "OP_Z_System_Path": config["OP_Z_Mounted_Dir"],
    "OP_Z_Local_Backup_States_Path": os.path.join(config["OPZBackupPath"], "Backup_States")
}

# OP1Fun Account Login Info
op1FunSetup = {
    "USER_ID": "",
    "Password": ""
}
# =========================== Display configuration ===========================
# Display driver luma oled lib
# Compatible displays: SSD1306, SSD1309, SSD1322, SSD1325, SSD1327, SSD1331, SSD1351 and SH1106
# Port: i2C port
# Address: Display i2c address
displayConfig = {
    "DisplayType": "SH1106",
    # "DisplayType": "SSD1306",
    "Rotation": 2,  # 0:0, 1:90, 2:180, 3:270
    "port": 1,
    "address": 0x3c
}

# =========================== Battery configuration ===========================
# RaspiUPS uses MAX17043 chip set
# ADS1115 not yet compatible
batteryConfig = {
    "enable": False,
    "UPS_Method": "RaspiUPS"  # RaspiUPS or ADS1115
}

# =================== DO NOT Modify ===================
# Ensuring important folders are created
if not os.path.exists(config["OP1BackupPath"]) or not os.path.exists(config["OPZBackupPath"]):
    forcedir(os.path.join(config["OP1BackupPath"], "projects"))
    forcedir(os.path.join(config["OP1BackupPath"], "patches/synth"))
    forcedir(os.path.join(config["OP1BackupPath"], "patches/drum"))
    forcedir(os.path.join(config["OPZBackupPath"], "Backup_States"))
    os.system("sudo chmod 0777 -R " + "/files")

if not os.path.exists(os.path.join(workDir, "op1funSetup.txt")):
    data = {
        "USER_ID": "",
        "USER_EMAIL": "",
        "API_TOKEN": ""
    }
    with open(os.path.join(workDir, 'op1funSetup.txt'), 'w') as outfile:
        json.dump(data, outfile, sort_keys=False, indent=4)
