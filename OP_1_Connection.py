import os
import sys
import time
import usb.util
import usb.core
from psutil import disk_partitions

from config import config, savePaths
from file_util import getDirFileList, get_visible_folders, analyzeAIF

__author__ = "Hsuan Han Lai (Edward Lai)"
__date__ = "2019-04-02"

currentStorageStatus = {
    "sampler": 0,
    "synth": 0,
    "drum": 0
}


# OP-1 connection
def ensure_connection():
    if not is_connected():
        wait_for_connection()


def is_connected():
    return usb.core.find(idVendor=config["USB_VENDOR"], idProduct=config["USB_PRODUCT"]) is not None


def wait_for_connection():
    try:
        while True:
            time.sleep(1)
            if is_connected():
                print("Connected!")
                break
    except KeyboardInterrupt:
        sys.exit(0)


# Mounting
def mountdevice(source, target, fs, options=''):
    ret = os.system('mount {} {}'.format(source, target))
    if ret not in (0, 8192):
        raise RuntimeError("Error mounting {} on {}: {}".format(source, target, ret))


def unmountdevice(target):
    ret = os.system('umount {}'.format(target))
    if ret != 0:
        raise RuntimeError("Error unmounting {}: {}".format(target, ret))


def getmountpath():
    o = os.popen('readlink -f /dev/disk/by-id/' + config["OP_1_USB_ID"]).read()
    return o.rstrip()


def getMountPath():
    mountpath = getmountpath()
    # mountPoint = ""
    for i, disk in enumerate(disk_partitions()):
        if disk.device == mountpath:
            mountPoint = disk.mountpoint
            config["OP_1_Mounted_Dir"] = mountPoint
            print(config["OP_1_Mounted_Dir"])
            return mountPoint


def start_OP_1_Connection():
    # Render Please Connect Screen
    wait_for_connection()
    mountpath = getmountpath()
    config["USB_Mount_Path"] = mountpath

    for i, disk in enumerate(disk_partitions()):
        if disk.device == mountpath:
            mountPoint = disk.mountpoint
            config["OP_1_Mounted_Dir"] = mountPoint
            print(config["OP_1_Mounted_Dir"])
            return mountPoint


def unmount_OP_1():
    unmountdevice(config["USB_Mount_Path"])


def list_files(startpath):
    patchType = ""
    sampleEngine = []
    synthEngine = []
    drum = []
    for root, dirs, files in os.walk(startpath):
        for f in files:
            currentFilePath = str(root) + "/" + f
            if f.endswith('.aif') and not f.startswith("."):
                try:
                    patchType, fx, lfo = analyzeAIF(currentFilePath)
                    print(patchType, fx, lfo)
                except:
                    pass
                # print(patchType, fx, lfo)
            if patchType == "Drum" or patchType == "Dbox" and "drum" in currentFilePath:
                drum.append(currentFilePath)
            elif patchType == "Sampler" and "synth" in currentFilePath:
                sampleEngine.append(currentFilePath)
            else:
                synthEngine.append(currentFilePath)
    return [sampleEngine, synthEngine, drum]


def get_OP1_Storage_Status():
    return currentStorageStatus


def update_Current_Storage_Status():
    sampler, synth, drum = list_files(savePaths["OP_1_Synth"])
    currentStorageStatus["sampler"] = len(sampler)
    currentStorageStatus["synth"] = len(synth)
    sampler, synth, drum = list_files(savePaths["OP_1_Drum"])
    currentStorageStatus["drum"] = len(drum)


