import os
from file_util import forcedir

OP_1_MountPath = ""
config = {
    "OP_1_USB_ID": "*Teenage_OP-1*",
    "USB_VENDOR": 0x2367,
    "USB_PRODUCT": 0x0002,
    "USB_Mount_Path": "", # /media/pi/....
    "OP_1_Mounted_Dir": "", # sda/m
    "LocalBackupPath": os.path.dirname(os.path.realpath(__file__))+"/OP_1_Backup_Library/",

    "Max_Synth_Sampler_patches": 42, "Max_Synth_Synthesis_patches": 100, "Max_Drum_Patches": 42,
    "TargetOp1MountDir": "/media/op1",
    "TargetOpZMountDir": "/media/opz"
}

# For System Use
savePaths = {
    "OP_1_System_Path": config["OP_1_Mounted_Dir"],
    # Local OP1 Backup Paths
    "Local_Dir": config["LocalBackupPath"],
    "Local_Projects": config["LocalBackupPath"] + "projects",
    "Local_Patches": config["LocalBackupPath"] + "patches",
    "Local_Synth": config["LocalBackupPath"] + "patches/synth",
    "Local_Drum": config["LocalBackupPath"] + "patches/drum"
}


# print(savePaths["Local_Projects"])
if not os.path.exists(config["LocalBackupPath"]):
    forcedir(os.path.dirname(os.path.realpath(__file__))+"/OP_1_Backup_Library/projects")
    forcedir(os.path.dirname(os.path.realpath(__file__))+"/OP_1_Backup_Library/patches/synth")
    forcedir(os.path.dirname(os.path.realpath(__file__))+"/OP_1_Backup_Library/patches/drum")