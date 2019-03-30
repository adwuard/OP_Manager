import os
from os import listdir
from os.path import isfile, join
from config import config


class fileBrowser:
    def __init__(self, Dir):
        self.histQueue = [Dir]
        self.currentDirLst = []
        self.currentDirPath = Dir
        self.prevDir = ""
        self.copyQueue = []

    def structCurrentPath(self):
        lst = self.histQueue
        str = ""
        for i in lst:
            str += i + "/"
        return str

    def selectNewPath(self, item):
        self.histQueue.append(item)
        self.currentDirLst = [f for f in listdir(self.structCurrentPath()) if not f.startswith(".")]
        return self.currentDirLst

    def addToCopyQueue(self, item):
        self.copyQueue.append(str(self.structCurrentPath()) + str(self.currentDirLst[item - 1]))

    def removeFromCopyQueue(self, item):
        removeTarget = self.currentDirLst[item - 1]
        idx = 0
        for i in self.copyQueue:
            fileName = i.split("/")
            fileName = fileName[-1]
            if fileName == removeTarget:
                print(fileName)
                print(removeTarget)
                self.copyQueue.pop(idx)
            idx += 1

    def prevPage(self):
        if len(self.histQueue) > 1:
            self.histQueue = self.histQueue[:-1]
            self.currentDirLst = [f for f in listdir(self.structCurrentPath()) if not f.startswith(".")]
            return True
        else:
            # Exit Current Program
            return False

    def getCopyQueue(self):
        return self.copyQueue

    # def setDirList(self):
    #     self.currentDirLst

    def getDirList(self):
        return self.currentDirLst


temp = fileBrowser(config["OP_1_System_Path"])
print(temp.selectNewPath("drum"))
temp.prevPage()
print(temp.getDirList())
# temp.addToCopyQueue(1)
# temp.addToCopyQueue(2)
# temp.addToCopyQueue(3)
# temp.removeFromCopyQueue(1)
# temp.removeFromCopyQueue(2)
# print(temp.getCopyQueue())
