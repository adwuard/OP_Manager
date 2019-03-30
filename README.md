# OP1_File_Organizer
Common issues from the OP-1 users is that OP-1 doesn't support projects and the unit only allow certain amount of patches.
I am currently developing a compact hardware tool that can easily swap and backup all the user patches and projects. This unit can benifet for users who don't want to connect their OP-1 to their computer. Or performers who wants to switch patches, and projects on the go. And allows the user to store all their OP-1 files in one place and store as much patches as whatever the SD card's capacity is available. The device will be low cost and compact.

## Features
- Quickly Upload/Backup Projects(tapes and album) form OP-1
- Load/Backup Snapshots patches
- Load Specfic Patches or Packs(Folder that contains multiple patches)
- Swap all patches: Since op-1 only accept limit amount of patches, user can preload different mega packs onto the raspberry pi, the loader will DELETE ALL the (drum, sample, and synth)patches on the OP-1 and load an entire different patch library
- Monitor remain available patch slots on the OP-1

## Hardware (Future Implement)
- Eventually can be deployed on to raspberry pi zero for maximum portability
- Uses 128x64 OLED Panel, a D pad, and two buttons for controll
- Uses OTG USB to Communicate with OP-1  
To-Do: Display Driver, OTG OP-1 Device Searcher, UI and menu design.

