import os
import shutil
from config import config, savePaths
from distutils.dir_util import copy_tree
from OP_1_Connect import OP_1_Connect
import datetime


class TapeBackup:

    def getAllOP1Tapes(self):
        print("get")

    def getTime(self):
        currentDT = datetime.datetime.now()
        return str(currentDT.year) + "_" + str(currentDT.month) + "_" + str(currentDT.day) + "_" + str(
            currentDT.hour) + "_" + str(currentDT.minute) + "_" + str(currentDT.second)

    def createNewFolder(self):
        savePath = savePaths["TapeBackupPath"]
        newPath = savePath + self.getTime()
        try:
            os.mkdir(newPath)
        except OSError:
            print("Creation of the directory %s failed" % newPath)
        else:
            print("Successfully created the directory %s " % newPath)
        return newPath

    def copytree(src, dst, symlinks=False, ignore=None):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)

    def copyToLocal(self):
        newFolderPath = self.createNewFolder()
        op1TapePath = config["OP_1_System_Path"] + "tape"
        op1AlbumPath = config["OP_1_System_Path"] + "album"
        copy_tree(op1AlbumPath, newFolderPath + "/album")
        copy_tree(op1TapePath, newFolderPath + "/tape")
        return "Done"

    def loadProjectToOP1(self, localProjectPath):
        op1TapePath = config["OP_1_System_Path"] + "tape"
        op1AlbumPath = config["OP_1_System_Path"] + "album"
        copy_tree(localProjectPath+"/tape", op1TapePath)
        copy_tree(localProjectPath+"/album", op1AlbumPath)
        return "Done"

temp = TapeBackup()
status = temp.copyToLocal()
# status = temp.loadProjectToOP1(savePaths["TapeBackupPath"] + "2019_3_29_22_10_2")
# print(status)
