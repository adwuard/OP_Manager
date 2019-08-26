import threading

import usb.util
import usb.core
import json
import os
import time
import usb.util
import usb.core
from PIL import ImageDraw, Image
from psutil import disk_partitions
from GPIO_Init import displayImage, getFont
from config import config, savePaths

__author__ = "Hsuan Han Lai (Edward Lai)"
__date__ = "2019-04-02"

workDir = os.path.dirname(os.path.realpath(__file__))

currentStorageStatus = {
    "sampler": 0,
    "synth": 0,
    "drum": 0
}


def is_connected():
    if usb.core.find(idVendor=config["USB_VENDOR"], idProduct=config["USB_PRODUCT"]) is not None:
        return True
    if usb.core.find(idVendor=config["USB_VENDOR"], idProduct=config["OP-Z_USB_PRODUCT"]) is not None:
        return True
    return False


# =========system shell calls to mount and unmount devices=========
def mountdevice(source, target):
    ret = os.system('sudo -E mount {} {}'.format(source, target))
    if ret not in (0, 8192):
        raise RuntimeError("Error mounting {} on {}: {}".format(source, target, ret))


def unmountdevice(target):
    if "op1" in target:
        ret = os.system('umount {}'.format(target))
        if ret != 0:
            raise RuntimeError("Error unmounting {}: {}".format(target, ret))
        os.system("sudo rm -R " + config["OP_1_Mounted_Dir"])
        config["OP_1_Mounted_Dir"] = ""
    else:
        ret = os.system('umount {}'.format(target))
        if ret != 0:
            raise RuntimeError("Error unmounting {}: {}".format(target, ret))
        os.system("sudo rm -R " + config["OP_Z_Mounted_Dir"])
        config["OP_Z_Mounted_Dir"] = ""


def getmountpath(device):
    """
    Search base on device's USB ID
    Then get the system mount path - EX: /dev/sda
    :param device:
    :return:
    """
    o = None
    if device == "OP1":
        o = os.popen('readlink -f /dev/disk/by-id/' + config["OP_1_USB_ID"]).read()
    elif device == "OPZ":
        o = os.popen('readlink -f /dev/disk/by-id/' + config["OP_Z_USB_ID"]).read()
    return o.rstrip()


def getMountPath(device):
    """
    Checks if the partition is mounted if not it return ""
    :param device: Target device being string "OP1" or "OPZ"
    :return: "" is not found
    """
    mountpath = getmountpath(device)
    # mountPoint = ""
    for i, disk in enumerate(disk_partitions()):
        print(disk)
        if disk.device == mountpath:
            mountPoint = disk.mountpoint
            if device == "OP1":
                config["OP_1_Mounted_Dir"] = mountPoint
                print(config["OP_1_Mounted_Dir"])
            elif device == "OPZ":
                config["OP_Z_Mounted_Dir"] = mountPoint
                print(config["OP_Z_Mounted_Dir"])
            return mountPoint
    return ""


def do_mount(device):
    if getMountPath(device) == "":
        try:
            print("-- device not mounted")
            mountpath = getmountpath(device)
            config["USB_Mount_Path"] = mountpath
            print (mountpath)
            if device == "OP1" and mountpath != "":
                print(config["TargetOp1MountDir"])
                # config["TargetOp1MountDir"] = mountpath
                os.system("sudo mkdir -p " + config["TargetOp1MountDir"])
                os.system("sudo chmod 0777 " + config["TargetOp1MountDir"])
                mountdevice(config["USB_Mount_Path"], config["TargetOp1MountDir"])

            elif device == "OPZ" and mountpath != "":
                print(config["TargetOpZMountDir"])
                # config["TargetOp1MountDir"] = mountpath
                os.system("sudo mkdir -p " + config["TargetOpZMountDir"])
                os.system("sudo chmod 0777 " + config["TargetOpZMountDir"])
                mountdevice(config["USB_Mount_Path"], config["TargetOpZMountDir"])
        except:
            return False
        return False
    else:
        return True


# ======== OP1 Mount/Unmount Helper Functions ===========
def check_OP_1_Connection_Silent():
    if is_connected():
        if do_mount("OP1"):
            return True
    else:
        return False


def check_OP_1_Connection():
    connected = Image.new('1', (128, 64))
    draw = ImageDraw.Draw(connected)
    draw.text((0, 25), "Connecting.....", font=getFont(), fill='white')
    displayImage(connected)

    # if is_connected():
    if do_mount("OP1"):
        connected = Image.new('1', (128, 64))
        draw = ImageDraw.Draw(connected)
        draw.text((0, 25), "Connected", font=getFont(), fill='white')
        displayImage(connected)
        return True
    else:
        connected = Image.new('1', (128, 64))
        draw = ImageDraw.Draw(connected)
        draw.text((0, 25), "No Connection!", font=getFont(), fill='white')
        displayImage(connected)
        config["USB_Mount_Path"] = ""
        config["OP_1_Mounted_Dir"] = ""
        time.sleep(1)
        return False


def unmount_OP_1():
    if getMountPath("OP1") != "":
        unmountDisplay = Image.new('1', (128, 64))
        draw = ImageDraw.Draw(unmountDisplay)
        draw.text((30, 25), "Ejecting!", font=getFont(), fill='white')
        displayImage(unmountDisplay)
        unmountdevice(config["OP_1_Mounted_Dir"])
        config["OP_1_Mounted_Dir"] = ""
        config["USB_Mount_Path"] = ""
        unmountDisplay = Image.new('1', (128, 64))
        draw = ImageDraw.Draw(unmountDisplay)
        draw.text((30, 25), "Ejected", font=getFont(), fill='white')
        displayImage(unmountDisplay)
        time.sleep(1)
        return True
    elif os.path.isdir(config["OP_Z_Mounted_Dir"]):
        unmountdevice(config["OP_Z_Mounted_Dir"])
        unmountDisplay = Image.new('1', (128, 64))
        draw = ImageDraw.Draw(unmountDisplay)
        draw.text((15, 25), "Ejected", font=getFont(), fill='white')
        displayImage(unmountDisplay)
        time.sleep(1)
        return True

    else:
        unmountDisplay = Image.new('1', (128, 64))
        draw = ImageDraw.Draw(unmountDisplay)
        draw.text((15, 25), "No Device to Eject", font=getFont(), fill='white')
        displayImage(unmountDisplay)
        time.sleep(1)
        return False


# ============= OP1 Helper tools =================
def get_abbreviation(text):
    """
    Rename texts to abbreviations in order to fit better to the screen
    """
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
    """
    For OP1 only
    Given path to dir, and return the counts of .aif files and all child directory
    :param startPath: path to folder
    :return: int: total count of aif files
    """
    filesCount = 0
    for root, dirs, files in os.walk(startPath):
        for f in files:
            if f.endswith('.aif') and not f.startswith("."):
                filesCount += 1
    return filesCount


def analyzeAIF(pathTOAIF):
    """
    For OP1 only
    path to the op1 AIF file extracting json format from the meta data and analyze patch type
    :param pathTOAIF: path to OP1 aif file
    :return: tuple of three strings (type, fx,lfo)
    """
    with open(pathTOAIF, 'rb') as reader:
        file = str(reader.read())
    strBuilder = ""
    startflag = False
    for i in file:
        if i == "}":
            strBuilder += "}"
            break
        if startflag:
            strBuilder += str(i)
        if not startflag and i == "{":
            strBuilder += str(i)
            startflag = True
    data = json.loads(strBuilder)
    return data.get("type").capitalize(), data.get("fx_type").capitalize(), data.get("lfo_type").capitalize()


def update_Current_Storage_Status():
    currentStorageStatus["sampler"] = getFileCount(config["OP_1_Mounted_Dir"] + "/synth")
    currentStorageStatus["synth"] = getFileCount(config["OP_1_Mounted_Dir"] + "/drum")
    currentStorageStatus["drum"] = getFileCount(config["OP_1_Mounted_Dir"] + "/drum")
    return currentStorageStatus["sampler"], currentStorageStatus["synth"], currentStorageStatus["drum"]


# ======== OPZ Mount/Unmount Helper Functions ===========
def check_OP_Z_Connection():
    connected = Image.new('1', (128, 64))
    draw = ImageDraw.Draw(connected)
    draw.text((0, 25), "Connecting.....", font=getFont(), fill='white')
    displayImage(connected)
    if do_mount("OPZ"):
        connected = Image.new('1', (128, 64))
        draw = ImageDraw.Draw(connected)
        draw.text((0, 25), "Connected", font=getFont(), fill='white')
        displayImage(connected)
        time.sleep(1)
        return True
    else:
        connected = Image.new('1', (128, 64))
        draw = ImageDraw.Draw(connected)
        draw.text((0, 25), "No Connection!", font=getFont(), fill='white')
        displayImage(connected)
        config["USB_Mount_Path"] = ""
        time.sleep(1)
        return False


def unmount_OP_Z():
    if getMountPath("OPZ") != "":
        unmountDisplay = Image.new('1', (128, 64))
        draw = ImageDraw.Draw(unmountDisplay)
        draw.text((30, 25), "Ejecting!", font=getFont(), fill='white')
        displayImage(unmountDisplay)
        unmountdevice(config["OP_Z_Mounted_Dir"])
        config["USB_Mount_Path"] = ""
        unmountDisplay = Image.new('1', (128, 64))
        draw = ImageDraw.Draw(unmountDisplay)
        draw.text((30, 25), "Ejected!", font=getFont(), fill='white')
        displayImage(unmountDisplay)
        time.sleep(1)
        return True
    else:
        unmountDisplay = Image.new('1', (128, 64))
        draw = ImageDraw.Draw(unmountDisplay)
        draw.text((15, 25), "No Device to Eject", font=getFont(), fill='white')
        displayImage(unmountDisplay)
        time.sleep(1)
        return False


def autoMountUnmontThread():
    while 1:
        print("Unmount Checking Thread")
        # if config["OP_1_Mounted_Dir"] == "":
        #     if do_mount("OP1"):
        #         print("============ Thread OP1 Mounted ==============")
        #     else:
        #         print("============ Thread Waiting OP1 ==============")
        # if config["OP_Z_Mounted_Dir"] == "":
        #     if do_mount("OPZ"):
        #         print("============ Thread OPZ Mounted ==============")
        #     else:
        #         print("============ Thread Waiting OPZ ==============")
        # Device Mounted check for unmount
        if config["OP_1_Mounted_Dir"] != "":
            if not os.listdir(config["OP_1_Mounted_Dir"]):
                unmountdevice(config["OP_1_Mounted_Dir"])
                config["OP_1_Mounted_Dir"] = ""
                print("============ Thread OP1 Auto Unmount==============")
        if config["OP_Z_Mounted_Dir"] != "":
            if not os.listdir(config["TargetOpZMountDir"]):
                unmountdevice(config["OP_Z_Mounted_Dir"])
                config["OP_z_Mounted_Dir"] = ""
                print("============ Thread OPZ Auto Unmount==============")
        time.sleep(3)


