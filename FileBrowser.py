# import math
import math
import os
import time
from os import listdir
from os.path import isdir, isfile, basename

from PIL import Image, ImageDraw
from GPIO_Init import getFont, getKeyStroke, displayImage, clearDisplay, getSmallFont, getLargeFont
from config import config, savePaths
from file_util import getDirFileList, analyzeAIF


class fileBrowser:
    def __init__(self, Dir):
        self.histQueue = [Dir]
        self.currentDirLst = sorted(getDirFileList(Dir))
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
        self.currentDirLst = sorted([f for f in listdir(self.structCurrentPath()) if not f.startswith(".")])
        return self.currentDirLst

    def addToCopyQueue(self, item):
        self.copyQueue.append(str(self.structCurrentPath()) + str(self.currentDirLst[item - 1]))

    def removeFromCopyQueue(self, item):
        removeTarget = self.currentDirLst[item - 1]
        idx = 0
        for i in self.copyQueue:
            fileName = i.split("/")
            fileName = fileName[-1]
            print("remove file name", fileName)
            if fileName in removeTarget:
                print(fileName)
                print(removeTarget)
                self.copyQueue.pop(idx)
            idx += 1

    def prevPage(self):
        if len(self.histQueue) > 1:
            self.histQueue = self.histQueue[:-1]
            self.currentDirLst = sorted([f for f in listdir(self.structCurrentPath()) if not f.startswith(".")])
            self.copyQueue = []
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


# =======================For UI Rendering=======================
def shiftArray(array, shortArray, shift):
    """
    Given full array of the file dir, and shotArray is subset of the full array.
    short array being the current page that is displayed on the screen
    buy shifting +1 or -1 to achieve scrolling capability

    :param self:
    :param array: Full array of given file Dir
    :param shortArray: current page display array subset of full array
    :param shift : [1, -1]
    :return: the shifted array either by increment or decrement
    """
    # global currentIndex
    # Max Number of lines can be displayed on the screen
    PageSize = config["DisplayLines"]
    # if the list dir can fit in the page, then there's nothing to scroll
    if len(array) == 0 or len(array) < PageSize:
        return array
    # If the short array pass in nothing, adding an element for correctness of the algorithm
    if len(shortArray) == 0:
        if len(array) < PageSize:
            return array
        else:
            return array[:5]
    current = 0
    if shortArray[0] in array:
        current = array.index(shortArray[0])
    # Scroll Down
    if shift == 1:
        if current + 1 + PageSize <= len(array):
            current += 1
    # Scroll Up
    elif shift == -1:
        if current - 1 >= 0:
            current -= 1
    shortArray = []
    # Constructing the return short array
    for i in range(current, current + PageSize):
        shortArray.append(array[i])
    return shortArray


def displayLine(line, indent):
    return indent, line * 10


def scale(val, src, dst):
    return math.floor((float(val - src[0]) / float(src[1] - src[0])) * (dst[1] - dst[0]) + dst[0])
    # return int(((val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0])


def getOffset(lstFull, currentPointer, scrollBarSize):
    scrollFullSize = 54
    availableScrolling = int(scrollFullSize - scrollBarSize)
    return scale(currentPointer, (0, len(lstFull) - 1), (0, availableScrolling))


def getScrollBarSize(lst):
    scrollFullSize = 54
    lstSize = len(lst) - 1
    if lstSize > 5:
        if 10 >= lstSize > 5:
            return scrollFullSize * 0.5
        elif 15 >= lstSize > 10:
            return scrollFullSize * 0.45
        elif 20 >= lstSize > 15:
            return scrollFullSize * 0.40
        elif 25 >= lstSize > 20:
            return scrollFullSize * 0.35
        elif 30 >= lstSize > 25:
            return scrollFullSize * 0.30
        elif 35 >= lstSize > 30:
            return scrollFullSize * 0.25
        elif 40 >= lstSize > 35:
            return scrollFullSize * 0.20
        elif 45 >= lstSize > 40:
            return scrollFullSize * 0.15
        elif 50 >= lstSize > 45:
            return scrollFullSize * 0.10
        else:
            return scrollFullSize * 0.05


# RenderOptionsMenu(["Upload", "Rename", "Delete"]_
def RenderOptionsMenu(lst):
    userChoice = ""
    cursor = 1

    # Animation of right slide in
    while True:
        image = Image.new('1', (128, 64))
        draw = ImageDraw.Draw(image)
        draw.rectangle([(0, 0), (128, 10)], 'white')
        draw.text(displayLine(0, 2), "Actions", fill='black', font=getFont())

        iterCount = 1
        for i in lst:
            draw.text(displayLine(iterCount, 10), str(i), fill='white', font=getFont())
            iterCount += 1
        draw.text(displayLine(cursor, 2), ">", fill='white', font=getFont())
        displayImage(image)

        time.sleep(0.1)
        key = getKeyStroke()
        if key == "UP":
            if not cursor - 1 < 1:
                cursor -= 1
        if key == "DOWN":
            if not cursor + 1 > len(lst):
                cursor += 1
        if key == "A":
            return "RETURN"
        if key == "B":
            return lst[cursor - 1]


def renderFolders(path, avail, patchPage):
    folderSelected = False
    actualFilePointer = 1
    currentCursor = 1
    shortArray = []
    offset = 0

    fb = fileBrowser(path)
    scrollBarLength = getScrollBarSize(fb.getDirList())

    # RenderFolders
    while True:
        image = Image.new('1', (128, 64))

        if patchPage == 1:
            image.paste(Image.open("Assets/Img/FileBrowser.png").convert("1"))
            draw = ImageDraw.Draw(image)
        else:
            draw = ImageDraw.Draw(image)
            draw.rectangle([(0, 0), (128, 10)], 'white')

        # print(fb.structCurrentPath())
        draw.text(displayLine(0, 2), os.path.basename(fb.structCurrentPath()[:-1]), fill='black', font=getFont())
        if patchPage:
            draw.text((108, -2), str(avail), fill='white', font=getFont())
        shortArray = shiftArray(fb.getDirList(), shortArray, 0)
        clearDisplay()
        counter = 1
        for i in shortArray:
            itempath = fb.structCurrentPath() + i
            copyQue = fb.getCopyQueue()
            selected = False

            if itempath in copyQue:
                selected = True

            if "aif" in i and counter == currentCursor:
                try:
                    synType, FX, LFO = analyzeAIF(fb.structCurrentPath() + "/" + i)
                except:
                    synType, FX, LFO = "N/A", "N/A", "N/A"
                    pass
                draw.text((90, 16), str(synType), fill='white', font=getFont())
                draw.text((90, 35), str(FX), fill='white', font=getFont())
                draw.text((90, 53), str(LFO), fill='white', font=getFont())

            i = i.replace(".aif", "")
            if len(i) > 10:
                i = i[:10] + ".."
            if selected:
                draw.rectangle(((9, counter * 10), (84, counter * 10 + 10)), 'white')
                draw.text(displayLine(counter, 10), str(i), fill='black', font=getFont())
            else:
                # draw.rectangle(((5, counter * 10), (110, 10)), 'black')
                draw.text(displayLine(counter, 10), str(i), fill='white', font=getFont())

            counter += 1
        draw.text(displayLine(currentCursor, 0), ">", fill='white', font=getFont())
        # Render Scroll Bar
        scrollBarXLocation = 86
        # List Shorter than screen size, fill the whole scroll bar
        if len(fb.getDirList()) <= 5:
            draw.line((scrollBarXLocation, 10, scrollBarXLocation, 64), fill="white", width=1)
        # Render Scroll Bar
        else:
            scrollBarLength = int(getScrollBarSize(fb.getDirList()))
            offset = getOffset(fb.getDirList(), actualFilePointer - 1, scrollBarLength)
            draw.line((scrollBarXLocation, 10 + offset, scrollBarXLocation, 10 + scrollBarLength + offset),
                      fill="white", width=1)

        displayImage(image)

        key = getKeyStroke()
        if key == "UP":
            if currentCursor - 1 < 1:
                temp = shortArray
                shortArray = shiftArray(fb.getDirList(), shortArray, -1)
                if temp != shortArray:
                    actualFilePointer -= 1
            else:
                currentCursor -= 1
                actualFilePointer -= 1

        if key == "DOWN":
            if currentCursor + 1 > len(shortArray):
                temp = shortArray
                shortArray = shiftArray(fb.getDirList(), shortArray, 1)
                if temp != shortArray:
                    actualFilePointer += 1
            else:
                currentCursor += 1
                actualFilePointer += 1

        if key == "LEFT":
            if len(fb.histQueue) == 1:
                return
            else:
                currentCursor = 1
                actualFilePointer = 1
                offset = 0
                fb.prevPage()
                scrollBarLength = getScrollBarSize(fb.getDirList())

        if key == "RIGHT":
            if not folderSelected and "aif" not in fb.getDirList():
                currentCursor = 1
                try:
                    fb.selectNewPath(fb.getDirList()[actualFilePointer - 1])
                except:
                    RenderOptionsMenu(["Upload", "Rename", "Delete"])
                scrollBarLength = getScrollBarSize(fb.getDirList())
                offset = 0
                actualFilePointer = 1

        if key == "CENTER":

            # Start Multi-select

            currentCopyQueue = fb.getCopyQueue()

            print(fb.structCurrentPath() + fb.getDirList()[actualFilePointer - 1])
            if fb.structCurrentPath() + fb.getDirList()[actualFilePointer - 1] not in currentCopyQueue:
                fb.addToCopyQueue(actualFilePointer)
            else:
                fb.removeFromCopyQueue(actualFilePointer)

            if len(fb.getCopyQueue()) >= 1:
                folderSelected = True
            else:
                folderSelected = False

            print(fb.getCopyQueue(), folderSelected)

        if key == "A":
            print("")
        if key == "B":
            print(RenderOptionsMenu(["Upload", "Rename", "Delete"]))

# temp.addToCopyQueue(1)
# temp.addToCopyQueue(2)
# temp.addToCopyQueue(3)
# temp.removeFromCopyQueue(1)
# temp.removeFromCopyQueue(2)
# print(temp.getCopyQueue())
