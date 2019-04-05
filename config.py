config = {
    "OP_1_USB_ID": "*Teenage_OP-1*",
    "USB_VENDOR": 0x2367,
    "USB_PRODUCT": 0x0002,

    "OP_1_Mounted_Dir": "",
    # "OP_1_Mounted_Dir": "/Users/edwardlai/Documents/Git Ripos/OP1_File_Organizer/SampleOP1Dir/",
    # "LocalBackupPath": "/Users/edwardlai/Documents/Git Ripos/OP1_File_Organizer/OP_1_Patches_Lib/",
    "LocalBackupPath": "/home/pi/Desktop/OP1_File_Organizer/SampleOP1Dir/",

    "Max_Synth_Sampler_patches": 42,
    "Max_Synth_Synthesis_patches": 100,
    "Max_Drum_Patches": 42,
    "DisplayLines": 5
}

# For System Use
savePaths = {
    "OP_1_System_Path": config["OP_1_Mounted_Dir"],
    "OP_1_Drum": config["OP_1_Mounted_Dir"] + "drum",
    "OP_1_Synth": config["OP_1_Mounted_Dir"] + "synth",
    # "OP_1_Synth": "/home/pi/Desktop/OP1_File_Organizer/SampleOP1Dir/SampleOP1Dir/synth",
    "OP_1_Tape": config["OP_1_Mounted_Dir"] + "tape",
    "OP_1_Album": config["OP_1_Mounted_Dir"] + "album",

    # Local Backup Paths
    "Local_Projects": config["LocalBackupPath"] + "project",
    "Local_Synth": config["LocalBackupPath"] + "synth",
    "Local_Drum": config["LocalBackupPath"] + "drum"
}

