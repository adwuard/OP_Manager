import os
import shutil
from config import config, savePaths
from distutils.dir_util import copy_tree
from OP_1_Connect import OP_1_Connect
import datetime

__author__ = "Hsuan Han Lai (Edward Lai)"
__date__ = "2019-04-02"


class TapeBackup:
    def getTime(self):
        currentDT = datetime.datetime.now()
        return str(currentDT.year) + "_" + str(currentDT.month) + "_" + str(currentDT.day) + "_" + str(
            currentDT.hour) + "_" + str(currentDT.minute) + "_" + str(currentDT.second)

    def createNewFolder(self):
        savePath = savePaths["OP_1_Tape"]
        newPath = savePath + self.getTime()
        try:
            os.mkdir(newPath)
        except OSError:
            print("Creation of the directory %s failed" % newPath)
        else:
            print("Successfully created the directory %s " % newPath)
        return newPath

    def copyToLocal(self):
        newFolderPath = self.createNewFolder()
        op1TapePath = config["OP_1_System_Path"] + "tape"
        op1AlbumPath = config["OP_1_System_Path"] + "album"
        copy_tree(op1AlbumPath, newFolderPath + "/album")
        copy_tree(op1TapePath, newFolderPath + "/tape")
        return True

    def loadProjectToOP1(self, localProjectPath):
        op1TapePath = config["OP_1_System_Path"] + "tape"
        op1AlbumPath = config["OP_1_System_Path"] + "album"
        copy_tree(localProjectPath + "/tape", op1TapePath)
        copy_tree(localProjectPath + "/album", op1AlbumPath)
        return True


# temp = TapeBackup()
# status = temp.copyToLocal()
# status = temp.loadProjectToOP1(savePaths["TapeBackupPath"] + "2019_3_29_22_10_2")
# print(status)






