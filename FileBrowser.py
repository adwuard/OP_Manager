import math
import os
import time
from os import listdir
from os.path import basename
from PIL import Image, ImageDraw
from GPIO_Init import getFont, getKeyStroke, displayImage, clearDisplay, getSmallFont, getAnyKeyEvent
from OP_1_Connection import get_abbreviation, update_Current_Storage_Status, check_OP_1_Connection, analyzeAIF
from config import config, savePaths
from file_util import getDirFileList, fileTransferHelper, deleteHelper

__author__ = "Hsuan Han Lai (Edward Lai)"
__date__ = "2019-04-02"

workDir = os.path.dirname(os.path.realpath(__file__))


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


# =======================For UI Rendering and page scrolling helper functions=======================
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
    PageSize = 5
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


def scale(val, src, dst):
    """
    :param val: Given input value for scaling
    :param src: Initial input value's Min Max Range pass in as tuple of two (Min, Max)
    :param dst: Target output value's Min Max Range pass in as tuple of two (Min, Max)
    :return: Return mapped scaling from target's Min Max range
    """
    return (float(val - src[0]) / float(src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]


def getOffset(lstFull, currentPointer, scrollBarSize):
    scrollFullSize = 54
    availableScrolling = int(scrollFullSize - scrollBarSize)
    return math.floor(scale(currentPointer, (0, len(lstFull) - 1), (0, availableScrolling)))


def getScrollBarSize(lst):
    scrollFullSize = 54
    lstSize = len(lst)
    if lstSize > 5:
        return scrollFullSize * scale(lstSize, (5, 50), (0.5, 0.05))


def renderRename(file=""):
    """
    Given a file path, renders for rename, with confirmation for rename or cancel,
    :param file:
    :return:
    """
    dirPath, originalName = os.path.dirname(file), basename(file)
    newName = list("__________")
    ascii_uppercase, digits, space = "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "0123456789", "_"
    curser, charPointer = 15, 0

    while True:
        image = Image.new('1', (128, 64))
        draw = ImageDraw.Draw(image)
        draw.rectangle([(-1, 0), (128, 64)], 'black', 'white')
        draw.rectangle([(0, 0), (128, 10)], 'white')
        if os.path.isdir(file):
            draw.text((2, 0), str("Rename Folder"), fill='black', font=getFont())
        else:
            draw.text((2, 0), str("Rename Patch"), fill='black', font=getFont())
        draw.text((1, 15), str(originalName.split(".")[0]), font=getFont(), fill="white")
        # Render Rename Edit Space
        offset, spacing = 15, 10
        for i in newName:
            draw.text((offset, 35), str(i), font=getFont(), fill="white")
            offset += spacing
        # Render cursor
        draw.text((curser, 45), str("^"), font=getFont(), fill="white")
        displayImage(image)

        key = getKeyStroke()
        if key == "LEFT":
            if curser - spacing >= 15:
                curser -= spacing
                charPointer -= 1
        if key == "RIGHT":
            if curser + spacing < 115:
                curser += spacing
                charPointer += 1
        if key == "UP":
            if newName[charPointer] == "_":
                newName[charPointer] = ascii_uppercase[0]
            elif newName[charPointer] in ascii_uppercase:
                current = ascii_uppercase.index(str(newName[charPointer]))
                if current - 1 >= 0:
                    newName[charPointer] = ascii_uppercase[current - 1]
            elif newName[charPointer] in digits:
                current = digits.index(str(newName[charPointer]))
                if current - 1 >= 0:
                    newName[charPointer] = digits[current - 1]
        if key == "DOWN":
            if newName[charPointer] == "_":
                newName[charPointer] = ascii_uppercase[0]
            elif newName[charPointer] in ascii_uppercase:
                current = ascii_uppercase.index(str(newName[charPointer]))
                if current + 1 < len(ascii_uppercase):
                    newName[charPointer] = ascii_uppercase[current + 1]
            elif newName[charPointer] in digits:
                current = digits.index(str(newName[charPointer]))
                if current + 1 < len(digits):
                    newName[charPointer] = digits[current + 1]
        if key == "CENTER":
            if newName[charPointer] == "_":
                newName[charPointer] = ascii_uppercase[0]
            elif newName[charPointer] in digits:
                newName[charPointer] = space
            elif newName[charPointer] in ascii_uppercase:
                newName[charPointer] = digits[0]
        if key == "A":
            return

        if key == "B":
            dirlst = os.listdir(dirPath)
            name = ''.join(newName).replace("_", " ").strip()
            if newName in dirlst:
                alreadyExist = Image.new('1', (128, 64))
                draw = ImageDraw.Draw(alreadyExist)
                draw.text((30, 25), "Name Already Exist!", font=getFont(), fill='white')
                displayImage(alreadyExist)
                pass

            if newName not in dirlst and len(name) != 0:
                rtn = RenderOptionsMenu(["Yes", "Cancel"], "Confirm")
                if rtn == "Yes":
                    # print(dirPath + "/" + originalName, dirPath + "/" + name + ".aif")
                    if not os.path.isdir(file):
                        os.rename(dirPath + "/" + originalName, dirPath + "/" + name + ".aif")
                    else:
                        os.rename(dirPath + "/" + originalName, dirPath + "/" + name)
                    image = Image.new('1', (128, 64))
                    image.paste(Image.open(workDir + "/Assets/Img/Done.png").convert("1"))
                    displayImage(image)
                    getAnyKeyEvent()
                    return

                elif rtn == "Cancel":
                    pass



def RenderOptionsMenu(lst, title="action"):
    """
    Renders items in given list, and return the string whatever user chooses
    :param title:
    :param lst: list of strings to render  Example: ["Upload", "Rename", "Delete"]
    :return: String the user choose
    """
    actualFilePointer = 1
    currentCursor = 1
    shortArray = []
    while True:
        image = Image.new('1', (128, 64))
        draw = ImageDraw.Draw(image)
        draw.rectangle([(0, 0), (128, 10)], 'white')
        draw.text((0, 2), title, fill='black', font=getFont())

        shortArray = shiftArray(lst, shortArray, 0)

        for i in range(0, len(shortArray)):
            draw.text((10, (i + 1) * 10), str(shortArray[i]), fill='white', font=getFont())

        # Render Scroll Bar
        if len(lst) > 5:
            scrollBarLength = int(getScrollBarSize(lst))
            offset = getOffset(lst, actualFilePointer - 1, scrollBarLength)
            draw.line((127, 10 + offset, 127, 10 + scrollBarLength + offset),
                      fill="white", width=1)

        draw.text((2, currentCursor * 10), ">", fill='white', font=getFont())
        displayImage(image)

        key = getKeyStroke()
        if key == "UP":
            if currentCursor - 1 < 1:
                temp = shortArray
                shortArray = shiftArray(lst, shortArray, -1)
                if temp != shortArray:
                    actualFilePointer -= 1
            else:
                currentCursor -= 1
                actualFilePointer -= 1

        if key == "DOWN":
            if currentCursor + 1 > len(shortArray):
                temp = shortArray
                shortArray = shiftArray(lst, shortArray, 1)
                if temp != shortArray:
                    actualFilePointer += 1
            else:
                currentCursor += 1
                actualFilePointer += 1
        if key == "LEFT":
            return "RETURN"
        if key == "RIGHT":
            return lst[actualFilePointer - 1]
        if key == "A":
            return "RETURN"
        if key == "B":
            return lst[actualFilePointer - 1]


def renderFolders(path, upload_download, dest):
    actualFilePointer = 1
    currentCursor = 1
    shortArray = []
    selectedDisplay = []

    fb = fileBrowser(path)

    sampler, synth, drum = update_Current_Storage_Status()

    if "synth" in fb.structCurrentPath() or "Synth" in fb.structCurrentPath():
        # Display synth and Sample Available
        availableSlots = config["Max_Synth_Synthesis_patches"] + config["Max_Synth_Sampler_patches"] - (synth + sampler)
    else:
        availableSlots = config["Max_Drum_Patches"] - drum

    # RenderFolders
    while True:
        image = Image.new('1', (128, 64))

        image.paste(Image.open(workDir + "/Assets/Img/FileBrowser.png").convert("1"))
        draw = ImageDraw.Draw(image)

        draw.text((2, -1), os.path.basename(fb.structCurrentPath()[:-1]), fill='black', font=getFont())

        if "synth" in fb.structCurrentPath().lower():
            # Display synth and Sample Available
            draw.text((108, -2), str(availableSlots), fill='white', font=getFont())
        else:
            # Display available drums
            draw.text((108, -2), str(availableSlots), fill='white', font=getFont())

        shortArray = shiftArray(fb.getDirList(), shortArray, 0)
        clearDisplay()

        # Empty Folder
        if not shortArray:
            draw.text((30, 40), "[Empty]", fill='white', font=getFont())
            displayImage(image)
            time.sleep(2)
            return

        counter = 1
        for i in shortArray:
            # Check if current item is selected
            selected = True if i in selectedDisplay else False
            # Render the AIF data from cursor landed item
            if "aif" in i and counter == currentCursor:
                try:
                    synType, FX, LFO = analyzeAIF(fb.structCurrentPath() + "/" + i)
                except:
                    # AIF meta data not retrievable
                    synType, FX, LFO = "N/A", "N/A", "N/A"
                    pass
                # Render Patch Type
                draw.text((90, 17), str(get_abbreviation(synType)), fill='white', font=getSmallFont())
                draw.text((90, 35), str(get_abbreviation(FX)), fill='white', font=getSmallFont())
                draw.text((90, 54), str(get_abbreviation(LFO)), fill='white', font=getSmallFont())

            # Remove extension for display and dash out long file names
            i = i.replace(".aif", "")
            if len(i) > 10:
                i = i[:10] + ".."
            # Iterate through selected queue and invert the color
            if selected:
                draw.rectangle(((9, counter * 10), (84, counter * 10 + 10)), 'white')
                draw.text((10, counter * 10), str(i), fill='black', font=getFont())
            else:
                draw.text((10, counter * 10), str(i), fill='white', font=getFont())
            # Render next item from current Directory
            counter += 1

        # Render cursor
        draw.text((0, currentCursor * 10), ">", fill='white', font=getFont())

        # Render Scroll Bar
        scrollBarXLocation = 86
        # List Shorter than screen size, fill the whole scroll bar
        if len(fb.getDirList()) <= 5:
            draw.line((scrollBarXLocation, 10, scrollBarXLocation, 64), fill="white", width=1)
        else:
            scrollBarLength = int(getScrollBarSize(fb.getDirList()))
            offset = getOffset(fb.getDirList(), actualFilePointer - 1, scrollBarLength)
            draw.line((scrollBarXLocation, 10 + offset, scrollBarXLocation, 10 + scrollBarLength + offset),
                      fill="white", width=1)

        # Update Image to the display
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
            if len(fb.histQueue) > 1:
                currentCursor = actualFilePointer = 1
                availableSlots += len(fb.getCopyQueue())
                fb.clearCopyQueue()
                fb.prevPage()
            else:
                return

        if key == "RIGHT":
            if len(fb.getCopyQueue()) == 0 and "aif" not in fb.getDirList()[actualFilePointer - 1]:
                fb.selectNewPath(fb.getDirList()[actualFilePointer - 1])
                currentCursor = 1
                actualFilePointer = 1

        if key == "CENTER":
            # Start Multi-select. (Select and deselect, and add the selected ones to copy queue)
            currentFile = fb.getDirList()[actualFilePointer - 1]
            selectedFolderPath = fb.structCurrentPath() + currentFile
            # Add to copy
            if currentFile not in selectedDisplay:
                # Decrement Available Patches
                if os.path.isdir(selectedFolderPath):
                    selectedDisplay.append(currentFile)
                    for i in listdir(selectedFolderPath):
                        fb.addToCopyQueue(currentFile + "/" + i)
                        if "media" not in fb.structCurrentPath():
                            availableSlots -= 1
                else:
                    fb.addToCopyQueue(currentFile)
                    selectedDisplay.append(currentFile)
                    if "media" not in fb.structCurrentPath():
                        availableSlots -= 1
            else:
                # Remove form copy
                if os.path.isdir(selectedFolderPath):
                    selectedDisplay.remove(currentFile)
                    for i in listdir(selectedFolderPath):
                        fb.removeFromCopyQueue(currentFile + "/" + i)
                        if "media" not in fb.structCurrentPath():
                            availableSlots += 1
                else:
                    fb.removeFromCopyQueue(currentFile)
                    selectedDisplay.remove(currentFile)
                    if "media" not in fb.structCurrentPath():
                        availableSlots += 1

        if key == "A":
            print("")
            # return
        if key == "B":
            currentFile = fb.getDirList()[actualFilePointer - 1]
            selectedFolderPath = fb.structCurrentPath() + currentFile
            fileCount = len(fb.getCopyQueue())
            if len(fb.getCopyQueue()) == 0 or len(selectedDisplay) == 1:
                # Takes case if non of the folder or file is selected
                if os.path.isdir(selectedFolderPath):
                    for i in listdir(selectedFolderPath):
                        fb.addToCopyQueue(currentFile + "/" + i)
                    fileCount = len(fb.getCopyQueue())
                    # availableSlots += len(fb.getCopyQueue())
                    rtn = RenderOptionsMenu(
                        [upload_download + " " + str(fileCount) + " Patches", "Delete " + str(fileCount) + "Patches"])
                else:
                    fb.addToCopyQueue(currentFile)
                    # availableSlots += 1
                    rtn = RenderOptionsMenu([upload_download, "Rename", "Delete"])

                if rtn == "RETURN":
                    availableSlots += fileCount
            else:
                if fileCount == 1:
                    rtn = RenderOptionsMenu([upload_download, "Rename", "Delete"])

                else:
                    rtn = RenderOptionsMenu(
                        [upload_download + " " + str(fileCount) + " Patches", "Delete " + str(fileCount) + "Patches"])
                if rtn == "RETURN":
                    availableSlots += fileCount

            if "Upload" in rtn or "Backup" in rtn:
                # List allowed
                if check_OP_1_Connection() and config["OP_1_Mounted_Dir"] != "":
                    try:
                        copyQueue = fb.getCopyQueue()

                        if dest == "":
                            dest = config["OP_1_Mounted_Dir"]
                        fileTransferHelper(copyQueue, dest)
                    except:
                        pass

            elif "Delete" in rtn:
                # List allowed
                if check_OP_1_Connection() and config["OP_1_Mounted_Dir"] != "":
                    try:
                        deleteHelper(fb.getCopyQueue())
                        fb.updatePage()
                    except:
                        pass

            elif "Rename" in rtn:
                # Only one item is allowed
                # Rename Page
                print(fb.getCopyQueue()[0])
                renderRename(str(fb.getCopyQueue()[0]))

            currentCursor = 1
            actualFilePointer = 1
            fb.clearCopyQueue()
            selectedDisplay = []

            # Update Remain Available Patches Here
        sampler, synth, drum = update_Current_Storage_Status()

# Python Bus Error can not open resource. Maybe For a rebuilt.
