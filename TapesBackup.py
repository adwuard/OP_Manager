import os
import shutil
from config import config, savePaths
from distutils.dir_util import copy_tree
from file_util import forcedir, removeTree,copyfile

__author__ = "Hsuan Han Lai (Edward Lai)"
__date__ = "2019-04-02"

workDir = os.path.dirname(os.path.realpath(__file__))

class TapeBackup:
    def getTime(self):
        import datetime
        currentDT = datetime.datetime.now()
        return str(currentDT.year) + "_" + str(currentDT.month) + "_" + str(currentDT.day) + "_" + str(
            currentDT.hour) + "_" + str(currentDT.minute) + "_" + str(currentDT.second)

    def copyToLocal(self):
        op1TapePath, op1AlbumPath = config["OP_1_Mounted_Dir"] + "/tape", config["OP_1_Mounted_Dir"] + "/album"
        newPath = savePaths["Local_Projects"] + "/" + self.getTime()
        forcedir(newPath + "/album")
        forcedir(newPath + "/tape")
        try:
            copy_tree(op1AlbumPath, newPath + "/album")
            copy_tree(op1TapePath, newPath + "/tape")
        except:
            shutil.rmtree(newPath)

    def loadProjectToOP1(self, localProjectPath):
        removeTree(config["OP_1_Mounted_Dir"] + "/tape")
        removeTree(config["OP_1_Mounted_Dir"] + "/album")
        # forcedir(config["OP_1_Mounted_Dir"] + "/tape")
        # forcedir(config["OP_1_Mounted_Dir"] + "/album")
        op1TapePath = config["OP_1_Mounted_Dir"] + "/tape"
        op1AlbumPath = config["OP_1_Mounted_Dir"] + "/album"
        copy_tree(localProjectPath + "/tape", op1TapePath)
        copy_tree(localProjectPath + "/album", op1AlbumPath)
        return True






