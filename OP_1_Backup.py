import os
import shutil
from os.path import isdir

from config import config, savePaths
from distutils.dir_util import copy_tree

from file_util import forcedir, copyfile, recursive_overwrite

__author__ = "Hsuan Han Lai (Edward Lai)"
__date__ = "2019-04-02"

workDir = os.path.dirname(os.path.realpath(__file__))


class OP1Backup:
    def getTime(self):
        import datetime
        currentDT = datetime.datetime.now()
        return str(currentDT.year) + str(currentDT.month) + str(currentDT.day) + "_" + str(
            currentDT.hour) + str(currentDT.minute) + str(currentDT.second)

    def copyToLocal(self):
        op1TapePath, op1AlbumPath = config["OP_1_Mounted_Dir"] + "/tape", config["OP_1_Mounted_Dir"] + "/album"
        currentTimeFolder = savePaths["Local_Projects"] + "/" + self.getTime()
        forcedir(currentTimeFolder + "/album")
        forcedir(currentTimeFolder + "/tape")
        try:
            copy_tree(op1AlbumPath, currentTimeFolder + "/album")
            copy_tree(op1TapePath, currentTimeFolder + "/tape")
        except:
            # Connection broken, remove created folder
            shutil.rmtree(currentTimeFolder)

    def copyOnlyTapesToLocal(self):
        op1TapePath, op1AlbumPath = config["OP_1_Mounted_Dir"] + "/tape", config["OP_1_Mounted_Dir"] + "/album"
        currentTimeFolder = savePaths["Local_Projects"] + "/" + self.getTime()
        forcedir(currentTimeFolder + "/tape")
        try:
            copy_tree(op1TapePath, currentTimeFolder + "/tape")
        except:
            shutil.rmtree(currentTimeFolder)

    def loadProjectToOP1(self, localProjectPath):
        shutil.rmtree(config["OP_1_Mounted_Dir"] + "/tape")
        forcedir(config["OP_1_Mounted_Dir"] + "/tape")
        op1TapePath = config["OP_1_Mounted_Dir"] + "/tape"
        copy_tree(localProjectPath + "/tape", op1TapePath)

        if isdir(localProjectPath + "/album"):
            shutil.rmtree(config["OP_1_Mounted_Dir"] + "/album")
            forcedir(config["OP_1_Mounted_Dir"] + "/album")
            op1AlbumPath = config["OP_1_Mounted_Dir"] + "/album"
            copy_tree(localProjectPath + "/album", op1AlbumPath)

    def backupOP1Patches(self):
        """
        OP-1 ------PATCHES------> LOCAL STORAGE
        Backing up all the patch files on the OP-1, and copy the file if the folder have already exist on the local drive.
        Overwrite when redundant file occurs
        """

        recursive_overwrite(config["OP_1_Mounted_Dir"] + "/synth", savePaths["Local_Synth"])
        recursive_overwrite(config["OP_1_Mounted_Dir"] + "/drum", savePaths["Local_Drum"])
