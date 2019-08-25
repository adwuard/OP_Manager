WifiTransfer = [
    ["Wifi Transfer", -1],
    ["SSH Transfer", "Check_IP"],
    ["Wifi Server", "Server IP"]
    # "Connect", -1
]

MIDI = [
    ["MIDI", -1],
    ["USB MIDI IN Test", "MIDI_In_Test"],
    ["USB MIDI OUT Test", "MIDI_Out_Test"]
]
op1fun = [
    ["OP1.FUN", -1],
    ["Packs", "OP1FUN_BrowsePacks"],
    ["Download All Packs", "OP1FUN_DownloadAllPacks"]
]

Utilities = [
    ["Utilities", -1],
    ["Check Storage", "checkStorage"],
    ["MIDI Host", "MIDI_Host"],
    ["OP1.FUN", op1fun],
    ["SSH Transfer", "Check_IP"],
    ["Eject", "act_ESC_Eject"],
    # ["Power Off System", "act_POWER_OFF"],
]

# PresetPage = [
#     ["Manage Presets", -1],
#     ["Freeze State", "act_Freeze_State"],
#     ["Upload From Local", "act_Upload_Preset_From_Local"],
#     ["Del All User Data", "act_DANG_Delete_ALL_From_OP_1"]
# ]

OP_1_Patches_Folder = [
    ["OP-1 Patches", -1],
    ["Synth", "OP-1 Synth Patches"],  # Start Browser
    ["Drum", "OP-1 Drum Patches"]  # Start Browser
]

Local_Patches = [
    ["Local Patches", -1],
    ["Synth", "UploadSynthPatches"],  # Start Browser
    ["Drum", "UploadDrumPatches"]  # Start Browser
]

OP_1_Patches = [
    ["OP-1", -1],
    ["Synth", "OP1_Synth_Patches"],  # Start Browser
    ["Drum", "OP1_Drum_Patches"]  # Start Browser
]

PatchesPage = [
    ["Patches", -1],
    ["Backup", "act_5_Backup_All_Patches"],
    ["Manage Local", Local_Patches],
    ["Manage OP-1", OP_1_Patches]
]

BackupPage = [
    ["Backup", -1],
    ["Tracks + Album", "act_Backup_Project_From_OP_1"],
    ["Tracks", "act_Load_Project_From_Local_only_tracks"]
]

ProjectsPage = [
    ["Projects", -1],
    ["Backup", BackupPage],
    ["Manage Local", "act_Load_Project_From_Local"]
]

OP1 = [
    ["OP-1", -1],
    ["Projects", ProjectsPage],
    ["Patches", PatchesPage]
]

OPZ = [
    ["OP-Z", -1],
    ["Freeze State", "act_Freeze_State_OPZ"],
    ["Recall State", "act_Recall_State_To_OPZ"],
    ["Manage OP-Z", "OPZ_Patches"]
    # ["Local Projects", "act_Load_Project_From_Local"]
]

MainPage = [
    ["Main Menu", -1],
    ["OP-1", OP1],
    ["OP-Z", OPZ],
    # ["Wifi Transfer", WifiTransfer],
    ["Utilities", Utilities],
    ["Eject", "act_ESC_Eject"]
]
