import os
from file_util import forcedir

config = {
    "OP_1_USB_ID": "*OP-1*",
    "OP_Z_USB_ID": "*OP-Z*",
    "USB_VENDOR": 0x2367,
    "USB_PRODUCT": 0x0002,
    "OP-Z_USB_PRODUCT": 0x000c,

    "USB_Mount_Path": "",
    "OP_1_Mounted_Dir": "",
    "OP_Z_Mounted_Dir": "/media/pi/OP-Z",
    # Device Mount Point
    "TargetOp1MountDir": "/media/op1",

    # Local Backup folders
    "OP1BackupPath": os.path.dirname(os.path.realpath(__file__)) + "/files/OP_1_Backup_Library/",
    "OPZBackupPath": os.path.dirname(os.path.realpath(__file__)) + "/files/OP_Z_Backup_Library/",

    # Configs
    "Max_Synth_Sampler_patches": 42,
    "Max_Synth_Synthesis_patches": 100,
    "Max_Drum_Patches": 42,
}

# For System Use
savePaths = {
    "OP_1_System_Path": config["OP_1_Mounted_Dir"],
    # Local OP1 Backup Paths
    "Local_Dir": config["OP1BackupPath"],
    "Local_Projects": config["OP1BackupPath"] + "projects",
    "Local_Patches": config["OP1BackupPath"] + "patches",
    "Local_Synth": config["OP1BackupPath"] + "patches/synth",
    "Local_Drum": config["OP1BackupPath"] + "patches/drum",
    "OP_Z_System_Path": config["OP_Z_Mounted_Dir"],
    "OP_Z_Local_Backup_States_Path": os.path.join(config["OPZBackupPath"], "Backup_States")
}
displayConfig = {
    "DisplayType": "SH1106",  # SSD1306, SSD1309, SSD1322, SSD1325, SSD1327, SSD1331, SSD1351 and SH1106
    "Rotation": 2  # 0:0, 1:90, 2:180, 3:270
    # "Rotation": 0  # 0:0, 1:90, 2:180, 3:270
}

batteryConfig = {
    "enable": True,
    "UPS_Method": "RaspiUPS"  # RaspiUPS or ADS1115
}

# Ensuring important folders are created
if not os.path.exists(config["OP1BackupPath"]) or not os.path.exists(config["OPZBackupPath"]):
    forcedir(os.path.dirname(os.path.realpath(__file__)) + "/files/OP_1_Backup_Library/projects")
    forcedir(os.path.dirname(os.path.realpath(__file__)) + "/files/OP_1_Backup_Library/patches/synth")
    forcedir(os.path.dirname(os.path.realpath(__file__)) + "/files/OP_1_Backup_Library/patches/drum")
    forcedir(os.path.dirname(os.path.realpath(__file__)) + "/files/OP_Z_Backup_Library/Backup_States")
