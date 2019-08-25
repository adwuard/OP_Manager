import os
from os import listdir

class fileBrowserDT:
    def __init__(self, Dir):
        self.histQueue = [Dir]
        self.currentDirLst = sorted(os.listdir(Dir))
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
        self.currentDirLst = sorted(
            [f for f in listdir(self.structCurrentPath()) if not f.startswith(".") and not f.endswith("plz")])
        return self.currentDirLst

    def addToCopyQueue(self, item):
        # self.copyQueue.append(str(self.structCurrentPath()) + str(self.currentDirLst[item - 1]))
        self.copyQueue.append(str(self.structCurrentPath()) + str(item))

    def removeFromCopyQueue(self, item):
        self.copyQueue.remove(str(self.structCurrentPath() + str(item)))

    def clearCopyQueue(self):
        self.copyQueue = []

    def prevPage(self):
        if len(self.histQueue) > 1:
            self.histQueue = self.histQueue[:-1]
            self.currentDirLst = sorted([f for f in listdir(self.structCurrentPath()) if not f.startswith(".")])
            self.copyQueue = []
            return True
        else:
            # Exit Current Program
            return False

    def updatePage(self):
        self.currentDirLst = sorted([f for f in listdir(self.structCurrentPath()) if not f.startswith(".")])
        self.copyQueue = []

    def getCopyQueue(self):
        return self.copyQueue

    def setDirList(self, lst):
        self.currentDirLst = lst

    def getDirList(self):
        return self.currentDirLst
