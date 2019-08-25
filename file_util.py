import os
from os.path import abspath, join, pardir, basename, dirname, isdir
import shutil
import ntpath
import GPIO_Init
import time
# from GPIO_Init import getAnyKeyEvent, displayImage, getFont, getKeyStroke, getSmallFont, displayPng
from PIL import Image, ImageDraw

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


def copyfile(src, dst, with_remove=False):
    print("copy " + src + " to " + dst)
    shutil.copy(src, dst)

    if (with_remove):
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
    Pass in list of paths to file, and copy to root destination
    It will create patch's parent folder if not already exist in the destination folder
    For example:
        fileTransferHelper(["..../OP1_File_Organizer/NotUsed/..../patch.aif"], dest = "/..../synth")

    :param srclist: ["pwd/1.aif", "pwd/2.aif", "pwd/3.aif",....., "pwd/n.aif"]
    :param dest: Root of the synth and drum destination folder
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
        draw.text((20, 63), srcBaseName, font=GPIO_Init.getFont(), fill="white")
        GPIO_Init.displayImage(image)
        print(i, distParentFolderName + "/" + srcBaseName)
        shutil.copy2(i, distParentFolderName + "/" + srcBaseName)

    GPIO_Init.displayPng(workDir + "/Assets/Img/Done.png")
    GPIO_Init.getAnyKeyEvent()  # Press any key to proceed
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
    GPIO_Init.displayPng(workDir + "/Assets/Img/Deleting.png")
    time.sleep(0.5)
    for f in srclist:
        if isdir(f):
            # If given element in a list is a directory
            shutil.rmtree(srclist[0])
        else:
            folder = dirname(f)
            if os.path.exists(f):
                # Check for file existence
                os.remove(f)
            if len(os.listdir(folder)) == 0:
                # If nothing is in the folder, remove the parent folder
                os.rmdir(folder)

    GPIO_Init.displayPng(workDir + "/Assets/Img/Done.png")
    GPIO_Init.getAnyKeyEvent()  # Press any key to proceed
    return


def recursive_overwrite(src, dest, ignore=None):
    print(src, dest)
    if os.path.isdir(src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        files = os.listdir(src)
        if ignore is not None:
            ignored = ignore(src, files)
        else:
            ignored = set()
        for f in files:
            if f not in ignored:
                recursive_overwrite(os.path.join(src, f),
                                    os.path.join(dest, f),
                                    ignore)
    else:
        shutil.copyfile(src, dest)


def moveFilesToFolder(lst, destFolderPath):
    for f in lst:
        base = basename(f)
        dest = os.path.join(destFolderPath, base)
        print("Moving: ", f, "      To: ", dest)
        shutil.move(f, dest)


def createEmptyFolder(path, foldername):
    newFolderPath = join(path, foldername)
    if not os.path.exists(newFolderPath):
        os.makedirs(newFolderPath)


def clearUnderFolder(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            print("remove", f)
            os.unlink(os.path.join(root, f))
        for d in dirs:
            print("remove Dir", d)
            shutil.rmtree(os.path.join(root, d))


def createImportantFolders():
    from config import savePaths
    forcedir(savePaths["Local_Dir"])
    forcedir(savePaths["Local_Projects"])
    forcedir(savePaths["Local_Patches"])
    forcedir(savePaths["Local_Synth"])
    forcedir(savePaths["Local_Drum"])
