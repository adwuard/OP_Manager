import os
from file_util import forcedir

OP_1_MountPath = ""
config = {
    "OP_1_USB_ID": "*Teenage_OP-1*",
    "USB_VENDOR": 0x2367,
    "USB_PRODUCT": 0x0002,

    "USB_Mount_Path": "",  # /media/pi/....
    "OP_1_Mounted_Dir": "",  # sda/m
    "OP_Z_Mounted_Dir": "",  # sda/m

    # Local Backup folders
    "OP1BackupPath": os.path.dirname(os.path.realpath(__file__)) + "/OP_1_Backup_Library/",
    "OPZBackupPath": os.path.dirname(os.path.realpath(__file__)) + "/OP_Z_Backup_Library/",

    # Configs
    "Max_Synth_Sampler_patches": 42, "Max_Synth_Synthesis_patches": 100, "Max_Drum_Patches": 42,
    "UPSMETHOND": "RaspiUPS",  # RaspiUPS or ADS1115

    # Device Mount Point
    "TargetOp1MountDir": "/media/op1",
    "TargetOpZMountDir": "/media/opz"

}

# For System Use
savePaths = {
    "OP_1_System_Path": config["OP_1_Mounted_Dir"],
    "OP_Z_System_Path": config["OP_Z_Mounted_Dir"],
    # Local OP1 Backup Paths
    "Local_Dir": config["OP1BackupPath"],
    "Local_Projects": config["OP1BackupPath"] + "projects",
    "Local_Patches": config["OP1BackupPath"] + "patches",
    "Local_Synth": config["OP1BackupPath"] + "patches/synth",
    "Local_Drum": config["OP1BackupPath"] + "patches/drum",
}

# Ensuring important folders are created
if not os.path.exists(config["OP1BackupPath"]):
    forcedir(os.path.dirname(os.path.realpath(__file__)) + "/OP_1_Backup_Library/projects")
    forcedir(os.path.dirname(os.path.realpath(__file__)) + "/OP_1_Backup_Library/patches/synth")
    forcedir(os.path.dirname(os.path.realpath(__file__)) + "/OP_1_Backup_Library/patches/drum")
    forcedir(os.path.dirname(os.path.realpath(__file__)) + "/OP_Z_Backup_Library/Backups")
