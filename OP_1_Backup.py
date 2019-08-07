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
    def getLatestProjectName(self, path):
        """
        Search Project Names in a given folder path
        And return next eligible folder name

        :param path:
        :return: New Folder Name
        """
        projects = os.listdir(path)
        print(projects)
        maxProjectNum = 0
        for i in projects:
            if "Project_" in i:
                temp = i.split("_")
                try:
                    temp = int(temp[-1])
                    if temp > maxProjectNum:
                        maxProjectNum = temp
                except IndexError:
                    pass
        return "Project_" + str(maxProjectNum + 1)

    def getTime(self):
        import datetime
        currentDT = datetime.datetime.now()
        return str(currentDT.year) + str(currentDT.month) + str(currentDT.day) + "_" + str(
            currentDT.hour) + str(currentDT.minute) + str(currentDT.second)

    def copyToLocal(self):
        op1TapePath, op1AlbumPath = config["OP_1_Mounted_Dir"] + "/tape", config["OP_1_Mounted_Dir"] + "/album"
        # currentTimeFolder = savePaths["Local_Projects"] + "/" + self.getTime()
        currentTimeFolder = savePaths["Local_Projects"] + "/" + self.getLatestProjectName(savePaths["Local_Projects"])
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
        # currentTimeFolder = savePaths["Local_Projects"] + "/" + self.getTime()
        currentTimeFolder = savePaths["Local_Projects"] + "/" + self.getLatestProjectName(savePaths["Local_Projects"])
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

    def backupOPZState(self):
        OPZStatePath = config["OP_Z_Mounted_Dir"]
        # currentTimeFolder = savePaths["OP_Z_Local_Backup_States_Path"] + "/" + self.getTime()
        currentTimeFolder = savePaths["OP_Z_Local_Backup_States_Path"] + "/" + self.getLatestProjectName(
            savePaths["OP_Z_Local_Backup_States_Path"])
        print(OPZStatePath)
        print(currentTimeFolder)
        forcedir(currentTimeFolder)
        try:
            copy_tree(OPZStatePath, currentTimeFolder)
            print("Finished CPY")
        except:
            shutil.rmtree(currentTimeFolder)

    def loadStateToOPZ(self, localPath):
        OPZStatePath = savePaths["OP_Z_Local_Backup_States_Path"]
        print("Starting..")
        print(localPath)
        print(OPZStatePath)

        for root, dirs, files in os.walk(OPZStatePath):
            for f in files:
                print("remove", f)
                os.unlink(os.path.join(root, f))
            for d in dirs:
                print("remove Dir", d)
                shutil.rmtree(os.path.join(root, d))

        print("Cleared")
        copy_tree(localPath, OPZStatePath)
        print("Finished CPY")
