# checkStoragePage = {
#     "OP-1 Storage": -1,
#     "Synth": -1,
#     "Sampler": -1,
#     "Drum": -1,
#     "Local": "00/32.34GB"
# }
# SSHPage = {
#     "SSH": -1,
#     "Start SSH Transfer": "Open SSH"
#     # "Connect": -1
# }
#
# # Need to add action paths
# Utilities = {
#     "Utilities": -1,
#     "Check Storage": "checkStoragePage",
#     "Remove All User Data": "Remove all Data"
# }
#
# PresetPage = {
#     "Manage Presets": -1,
#     "Freeze State": "act_Freeze_State",
#     "Upload From Local": "act_Upload_Preset_From_Local",
#     "Del All User Data": "act_DANG_Delete_ALL_From_OP_1"
# }
#
# OP_1_Patches_Folder = {
#     "OP-1 Patches": -1,
#     "Synth": "OP-1 Synth Patches", #Start Browser
#     "Drum": "OP-1 Drum Patches" #Start Browser
# }
#
# Local_Patches ={
#     "Local Patches": -1,
#     "Synth": "Local Patches Synth", #Start Browser
#     "Drum": "Local Patches Synth" #Start Browser
# }
#
# PatchesPage = {
#     "Manage Patches": -1,
#     "Backup Patches": "act_5_Backup_All_Patches",
#     "Local Patches": Local_Patches
# }
#
# ProjectsPage = {
#     "Manage Projects": -1,
#     "Backup Project": "act_Backup_Project_From_OP_1",
#     "Local Projects": "Local Project"
# }



# checkStoragePage = [
#     ["OP-1 Storage", -1]
# ]
SSHPage = [
    ["SSH", -1],
    ["Start SSH Transfer", "Open SSH"]
    # "Connect", -1
]

# Need to add action paths
Utilities = [
    ["Utilities", -1],
    ["Check Storage", "checkStorage"],
    ["Remove All User Data", "Remove all Data"]
]

PresetPage = [
    ["Manage Presets", -1],
    ["Freeze State", "act_Freeze_State"],
    ["Upload From Local", "act_Upload_Preset_From_Local"],
    ["Del All User Data", "act_DANG_Delete_ALL_From_OP_1"]
]

OP_1_Patches_Folder = [
    ["OP-1 Patches", -1],
    ["Synth", "OP-1 Synth Patches"], #Start Browser
    ["Drum", "OP-1 Drum Patches"] #Start Browser
]

Local_Patches =[
    ["Local Patches", -1],
    ["Synth", "UploadSynthPatches"], #Start Browser
    ["Drum", "UploadDrumPatches"] #Start Browser
]

OP_1_Patches=[
    ["OP-1", -1],
    ["Synth", "OP1_Synth_Patches"], #Start Browser
    ["Drum", "OP1_Drum_Patches"] #Start Browser
]


PatchesPage = [
    ["Manage Patches", -1],
    ["Backup Patches", "act_5_Backup_All_Patches"],
    ["Local Patches", Local_Patches],
    ["Manage OP-1 Patches", OP_1_Patches]
]

ProjectsPage = [
    ["Manage Projects", -1],
    ["Backup Project", "act_Backup_Project_From_OP_1"],
    ["Local Projects", "act_Load_Project_From_Local"]
]


MainPage = [
    ["OP-1 File Manager", -1],
    ["Projects", ProjectsPage],
    ["Patches", PatchesPage],
    ["SSH Transfer", SSHPage],
    ["Utilities", Utilities],
    ["Eject OP-1", "act_ESC_Eject_OP_1"]
]


 # "Preset Packs", PresetPage,


