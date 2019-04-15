import os
import sys
import time
import usb.util
import usb.core
from PIL import ImageDraw, Image
from psutil import disk_partitions

from GPIO_Init import displayImage, getFont
from config import config, savePaths
from file_util import getDirFileList, get_visible_folders, analyzeAIF

__author__ = "Hsuan Han Lai (Edward Lai)"
__date__ = "2019-04-02"

workDir = os.path.dirname(os.path.realpath(__file__))

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


# def wait_for_connection():
#     try:
#         if is_connected():
#             print("Connected!")
#             break
#         else:
#             return
#     except KeyboardInterrupt:
#         sys.exit(0)


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
    print(mountpath)
    # mountPoint = ""
    for i, disk in enumerate(disk_partitions()):
        if disk.device == mountpath:
            mountPoint = disk.mountpoint
            config["OP_1_Mounted_Dir"] = mountPoint
            return mountPoint


def check_OP_1_Connection():
    if is_connected():
        mountpath = getMountPath()
        print("Mount Path", mountpath)
        config["USB_Mount_Path"] = mountpath
        print("Mount Path", mountpath)
        return True
    else:
        connected = Image.new('1', (128, 64))
        draw = ImageDraw.Draw(connected)
        draw.text((30, 25), "Please Check Connection!", font=getFont(), fill='white')
        displayImage(connected)
        config["USB_Mount_Path"] = ""
        config["OP_1_Mounted_Dir"] = ""
        time.sleep(1)
        return False



def unmount_OP_1():
    if config["OP_1_Mounted_Dir"] != "":
        unmountDisplay = Image.new('1', (128, 64))
        draw = ImageDraw.Draw(unmountDisplay)
        draw.text((30, 25), "Ejecting!", font=getFont(), fill='white')
        displayImage(unmountDisplay)

        cmd = "sudo umount " + config["OP_1_Mounted_Dir"]
        os.system(cmd)

        config["OP_1_Mounted_Dir"] = ""
        config["USB_Mount_Path"] = ""
        unmountDisplay = Image.new('1', (128, 64))
        draw = ImageDraw.Draw(unmountDisplay)
        draw.text((30, 25), "Ejected!", font=getFont(), fill='white')
        displayImage(unmountDisplay)
        time.sleep()
        return True
    else:
        unmountDisplay = Image.new('1', (128, 64))
        draw = ImageDraw.Draw(unmountDisplay)
        draw.text((15, 25), "No Device to Eject", font=getFont(), fill='white')
        displayImage(unmountDisplay)
        time.sleep(1)
        return False


def get_abbreviation(text):
    if text == "Element":
        return "Elem"
    elif text == "Tremolo":
        return "Tremo"
    elif text == "Random":
        return "Rand"
    elif text == "Sampler":
        return "Sample"
    else:
        return text


def getFileCount(startPath):
    filesCount = 0
    for root, dirs, files in os.walk(startPath):
        for f in files:
            if f.endswith('.aif') and not f.startswith("."):
                filesCount += 1
    return filesCount


def checkOccupiedSlots(startPath):
    patchType = ""
    sampleEngine = []
    synthEngine = []
    drum = []
    for root, dirs, files in os.walk(startPath):
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
            elif patchType == "Sampler":
                sampleEngine.append(currentFilePath)
            else:
                synthEngine.append(currentFilePath)
    return [sampleEngine, synthEngine, drum]


def update_Current_Storage_Status():
    # sampler, synth, none = checkOccupiedSlots(config["OP_1_Mounted_Dir"]+"/synth")
    # none, none, drum = checkOccupiedSlots(config["OP_1_Mounted_Dir"]+"/drum")
    sampler = getFileCount(config["OP_1_Mounted_Dir"] + "/synth")
    synth = getFileCount(config["OP_1_Mounted_Dir"] + "/drum")
    drum = getFileCount(config["OP_1_Mounted_Dir"] + "/drum")
    currentStorageStatus["sampler"] = sampler
    currentStorageStatus["synth"] = synth
    currentStorageStatus["drum"] = drum
    return sampler, synth, drum
