import json
from os.path import abspath, join, pardir, basename, dirname
from time import sleep
from PIL import Image, ImageDraw
from GPIO_Init import displayImage, getAnyKeyEvent, getFont
import os
import time
from os.path import abspath, join, pardir, basename, dirname, isdir
import shutil
import ntpath
from PIL import Image, ImageDraw
from GPIO_Init import displayImage, getAnyKeyEvent, getFont, displayPng

__author__ = "Hsuan Han Lai (Edward Lai)"
__date__ = "2019-04-02"

workDir = os.path.dirname(os.path.realpath(__file__))


# =================== Helper Tools===================
def copytree(src, dst, symlinks=False, ignore=shutil.ignore_patterns('.*', '_*')):
    """
    Copy Entire Folder
    :param src: source path
    :param dst: destination path
    :param symlinks: optional
    :param ignore: pass shutil.ignore_patterns('.*', '_*')
    :return:
    """
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def copyfile(src,dst, with_remove = False):
    print("copy " + src + " to " + dst)
    shutil.copy(src,dst)

    if(with_remove):
        os.remove(src)


def forcedir(path):
    """
    This creat necessary folders to the path if not already exists
    :param path: path to folder existence check
    :return: NA
    """
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

# =======================List Files======================
def get_visible_folders(dirPath=""):
    """
    Get visible folder from given path
    :param dir: path to directory
    :return: list of directories found
    """
    lst = []
    try:
        lst = list(filter(lambda x: os.path.isdir(os.path.join(dirPath, x)), os.listdir(dirPath)))
    except:
        pass
    return lst


def getDirFileList(d):
    return list(filter(lambda x: x[0] != '.', os.listdir(d)))



def fileTransferHelper(srclist, dest):
    """
    Pass in list of paths to file, and a copy root destination
    It will create patch's parent folder if now already exist in the destination folder
    For example:
        fileTransferHelper(["..../OP1_File_Organizer/NotUsed/..../patch.aif"], dest = "/..../synth")

    :param srclist: ["pwd/1.aif", "pwd/2.aif", "pwd/3.aif",....., "pwd/n.aif"]
    :param dest: Root of the destination folder
    :return: NA
    """



    for i in srclist:
        srcParentFolderName = abspath(join(i, pardir)).split("/")[-1:][0]
        srcBaseName = basename(i)
        distParentFolderName = dest + "/" + str(srcParentFolderName)
        print(distParentFolderName)
        forcedir(distParentFolderName)
        image = Image.new('1', (128, 64))

        if workDir in srclist[0]:
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

    displayPng(workDir + "/Assets/Img/Done.png")
    getAnyKeyEvent()  # Press any key to proceed
    return


def deleteHelper(srclist):
    """
    Takes in a list of full walk path(str) for deletion.
    And render the delete on the display while deleting.
    For Example:
        [filePath1, filePath2, filePath3.......filePath n]
        or
        [DirPath1, DirPath2, DirPath3,...., DirPath n]

    :param srclist: list of paths to file or directory
    :return: NA
    """
    displayPng(workDir + "/Assets/Img/Deleting.png")
    time.sleep(0.2)
    for i in srclist:
        if isdir(i):
            # If given element in a list is a directory
            shutil.rmtree(srclist[0])
        else:
            folder = dirname(i)
            if os.path.exists(i):
                # Check for file existence
                os.remove(i)
            if len(os.listdir(folder)) == 0:
                # If nothing is in the folder, remove the parent folder
                os.rmdir(folder)
    displayPng(workDir + "/Assets/Img/Done.png")
    getAnyKeyEvent()  # Press any key to proceed
    return


def createImportantFolders():
    from config import savePaths
    forcedir(savePaths["Local_Dir"])
    forcedir(savePaths["Local_Projects"])
    forcedir(savePaths["Local_Patches"])
    forcedir(savePaths["Local_Synth"])
    forcedir(savePaths["Local_Drum"])

