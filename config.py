import os


OP_1_MountPath = ""
config = {
    "OP_1_USB_ID": "*Teenage_OP-1*",
    "USB_VENDOR": 0x2367,
    "USB_PRODUCT": 0x0002,
    "USB_Mount_Path": "",
    "OP_1_Mounted_Dir": "",
    "LocalBackupPath": os.path.dirname(os.path.realpath(__file__))+"/OP_1_Backup_Library/",
    "Max_Synth_Sampler_patches": 42,
    "Max_Synth_Synthesis_patches": 100,
    "Max_Drum_Patches": 42,
    "DisplayLines": 5,
    "TargetOp1MountDir":"/media/op1"

}

# For System Use
savePaths = {
    "OP_1_System_Path": config["OP_1_Mounted_Dir"],
    "OP_1_Drum": config["OP_1_Mounted_Dir"] + "/drum",
    "OP_1_Synth": config["OP_1_Mounted_Dir"] + "/synth",
    "OP_1_Tape": config["OP_1_Mounted_Dir"] + "/tape",
    "OP_1_Album": config["OP_1_Mounted_Dir"] + "/album",

    # Local Backup Paths
    "Local_Dir": config["LocalBackupPath"],
    "Local_Projects": config["LocalBackupPath"] + "projects",
    "Local_Patches": config["LocalBackupPath"] + "patches",
    "Local_Synth": config["LocalBackupPath"] + "patches/synth",
    "Local_Drum": config["LocalBackupPath"] + "patches/drum"
}

