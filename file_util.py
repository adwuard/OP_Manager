import json
from os.path import abspath, join, pardir, basename, dirname
from time import sleep

from PIL import Image, ImageDraw

from GPIO_Init import displayImage, getAnyKeyEvent, getFont
from config import config
import os
import shutil
import ntpath

__author__ = "Hsuan Han Lai (Edward Lai)"
__date__ = "2019-04-02"

workDir = os.path.dirname(os.path.realpath(__file__))


# =================== Helper Tools===================
# Copy Entire Folder
def copytree(src, dst, symlinks=False, ignore=shutil.ignore_patterns('.*', '_*')):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


# This creat necessary folders to the path if not already exists
def forcedir(path):
    if not os.path.isdir(path):
        os.makedirs(path)


# ======================Copy Files ======================
def listOfPathsToDir(lst, target_Dir):
    for i in lst:
        parentfolder = ntpath.basename(os.path.dirname(i))
        filename = ntpath.basename(i)
        # Ensure the Dir is There
        forcedir(target_Dir + "/" + parentfolder)
        dstBuilder = target_Dir + "/" + parentfolder + filename
        shutil.copyfile(i, dstBuilder)


# [synth pack 1, synth pack 2, synth pack 3, synth pack 4... ], op1/synth
def copyListOfDirs(lst, target_Dir):
    for i in lst:
        foldername = ntpath.basename(i)
        forcedir(target_Dir + "/" + foldername)
        copytree(i, target_Dir + "/" + foldername)


def rename(src, dst):
    os.rename(src, dst)


def get_visible_folders(d):
    return list(filter(lambda x: os.path.isdir(os.path.join(d, x)), os.listdir(d)))


def getDirFileList(d):
    return list(filter(lambda x: x[0] != '.', os.listdir(d)))


def analyzeAIF(pathTOAIF):
    with open(pathTOAIF, 'rb') as reader:
        file = str(reader.read())
    strbuilder = ""
    startflag = False
    for i in file:
        if i == "}":
            strbuilder += "}"
            break
        if startflag:
            strbuilder += i
        if not startflag and i == "{":
            strbuilder += i
            startflag = True
    data = json.loads(strbuilder)
    # print(data)
    return data.get("type").capitalize(), data.get("fx_type").capitalize(), data.get("lfo_type").capitalize()


# Removes A File
# os.remove("")

# removes all files including the folder itself

def removeTree(path):
    shutil.rmtree(path)


# Remove files inside a dir
# d='/home/me/test'
# filesToRemove = [os.path.join(d,f) for f in os.listdir(d)]
# for f in filesToRemove:
#     os.remove(f)

# fileTransferHelper(["..../OP1_File_Organizer/NotUsed/..../patch.aif"], "/..../synth")
def fileTransferHelper(srclist, dest):
    for i in srclist:
        srcParentFolderName = abspath(join(i, pardir)).split("/")[-1:][0]
        srcBaseName = basename(i)
        distParentFolderName = dest + "/" + srcParentFolderName
        forcedir(distParentFolderName)

        image = Image.new('1', (128, 64))
        if config["LocalBackupPath"] in srclist[0]:
            # Local to OP1
            image.paste(Image.open(workDir + "/Assets/Img/UploadPatches.png").convert("1"))
        else:
            # OP1 to Local
            image.paste(Image.open(workDir + "/Assets/Img/DownloadPatches.png").convert("1"))
        draw = ImageDraw.Draw(image)
        draw.text((20, 63), srcBaseName, font=getFont(), fill="white")
        displayImage(image)
        print(i, distParentFolderName + "/" + srcBaseName)
        shutil.copy2(i, distParentFolderName + "/" + srcBaseName)

    image = Image.new('1', (128, 64))
    image.paste(Image.open(workDir + "/Assets/Img/Done.png").convert("1"))
    displayImage(image)
    getAnyKeyEvent()  # Press any key to proceed
    return


def deleteHelper(srclist):
    image = Image.new('1', (128, 64))
    image.paste(Image.open(workDir + "/Assets/Img/Deleting.png").convert("1"))
    displayImage(image)
    sleep(0.5)

    for i in srclist:
        folder = dirname(i)
        if os.path.exists(i):
            os.remove(i)

        if len(os.listdir(folder)) == 0:
            os.rmdir(folder)

    image = Image.new('1', (128, 64))
    image.paste(Image.open(workDir + "/Assets/Img/Done.png").convert("1"))
    displayImage(image)
    getAnyKeyEvent()  # Press any key to proceed
    return
