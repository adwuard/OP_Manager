import math
import os
import shutil
import time
from os import listdir
from os.path import basename, join, dirname
from PIL import Image, ImageDraw

from FileBrowserDT import fileBrowserDT
from GPIO_Init import getFont, getKeyStroke, displayImage, getSmallFont, getAnyKeyEvent
from OP_1_Connection import get_abbreviation, update_Current_Storage_Status, check_OP_1_Connection, analyzeAIF, \
    check_OP_Z_Connection, check_OP_1_Connection_Silent
from config import config, savePaths
from file_util import fileTransferHelper, deleteHelper, clearUnderFolder, createEmptyFolder, moveFilesToFolder

__author__ = "Hsuan Han Lai (Edward Lai)"
__date__ = "2019-04-02"

workDir = os.path.dirname(os.path.realpath(__file__))


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


def renderRename(file="", jsutName=False):
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

        if not os.path.exists(file):
            # The given path does not exist, means its creating a new folder
            draw.text((2, 0), str("New Folder"), fill='black', font=getFont())

        elif os.path.isdir(file):
            draw.text((2, 0), str("Rename Folder"), fill='black', font=getFont())
            draw.text((1, 15), str(originalName.split(".")[0]), font=getFont(), fill="white")
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
            return ""

        if key == "B":
            if jsutName:
                name = ''.join(newName).replace("_", " ").strip()
                if len(name) != 0:
                    rtn = RenderOptionsMenu(["Yes", "Cancel"], "Confirm")
                    if rtn == "Yes":
                        return name
                    else:
                        return ""

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


def RenderOptionsMenu(lst, title="action", sort=True):
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
        draw.text((0, 0), title, fill='black', font=getFont())

        if sort:
            lst = sorted(lst)
        shortArray = shiftArray(lst, shortArray, 0)

        for i in range(0, len(shortArray)):
            draw.text((10, (i + 1) * 10), str(shortArray[i]), fill='white', font=getFont())

        # Render Scroll Bar
        if len(lst) > 5:
            scrollBarLength = int(getScrollBarSize(lst))
            offset = getOffset(lst, actualFilePointer - 1, scrollBarLength)
            draw.line((127, 10 + offset, 127, 10 + scrollBarLength + offset),
                      fill="white", width=1)

        # Not items in the given lst
        if not len(lst):
            draw.text((2, currentCursor * 10), "[----Empty----]", fill='white', font=getFont())
        else:
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
            if len(lst):
                return lst[actualFilePointer - 1]

        if key == "A":
            return "RETURN"

        if key == "B":
            if len(lst):
                return lst[actualFilePointer - 1]


def renderFolders(path, upload_download, dest, singleFileSelection=False, localMode=False):
    actualFilePointer = 1
    currentCursor = 1
    shortArray = []
    selectedDisplay = []

    fb = fileBrowserDT(path)
    # RenderFolders
    while True:
        # sampler, synth, drum = update_Current_Storage_Status()
        if check_OP_1_Connection_Silent():
            sampler, synth, drum = update_Current_Storage_Status()
            if "synth" in fb.structCurrentPath() or "Synth" in fb.structCurrentPath():
                # Display synth and Sample Available
                availableSlots = config["Max_Synth_Synthesis_patches"] + config["Max_Synth_Sampler_patches"] - (
                        synth + sampler)
            else:
                availableSlots = config["Max_Drum_Patches"] - drum
        else:
            availableSlots = 0
        image = Image.new('1', (128, 64))

        image.paste(Image.open(workDir + "/Assets/Img/FileBrowser.png").convert("1"))
        draw = ImageDraw.Draw(image)

        draw.text((2, -1), os.path.basename(fb.structCurrentPath()[:-1]), fill='black', font=getFont())

        if config["OP_1_Mounted_Dir"] != "":
            if "synth" in fb.structCurrentPath().lower():
                # Display synth and Sample Available
                draw.text((108, -2), str(availableSlots - len(fb.getCopyQueue())), fill='white', font=getFont())
            else:
                # Display available drums
                draw.text((108, -2), str(availableSlots - len(fb.getCopyQueue())), fill='white', font=getFont())
        else:
            draw.text((108, -2), "--", fill='white', font=getFont())

        shortArray = shiftArray(fb.getDirList(), shortArray, 0)
        # Empty Folder
        if not shortArray:
            draw.text((5, 10), "[----Empty----]", fill='white', font=getFont())
            displayImage(image)

        counter = 1
        for i in shortArray:
            # Check if current item is selected
            selected = True if i in selectedDisplay else False
            # Render the AIF data from cursor landed item
            if "aif" in i and counter == currentCursor:
                try:
                    synType, FX, LFO = analyzeAIF(os.path.join(fb.structCurrentPath(), i))
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
                draw.rectangle(((9, counter * 10), (83, counter * 10 + 10)), 'white')
                draw.text((10, counter * 10), str(i), fill='black', font=getFont())
            else:
                draw.text((10, counter * 10), str(i), fill='white', font=getFont())
            # Render next item from current Directory
            counter += 1

        # Render cursor
        if shortArray:
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
                selectedDisplay = []
                fb.clearCopyQueue()
                fb.prevPage()
            else:
                return

        if key == "RIGHT":
            if len(fb.getDirList()):
                if len(fb.getCopyQueue()) == 0 and "aif" not in fb.getDirList()[actualFilePointer - 1]:
                    fb.selectNewPath(fb.getDirList()[actualFilePointer - 1])
                    currentCursor = 1
                    actualFilePointer = 1

        if key == "CENTER":
            # Start Multi-select. (Select and deselect, and add the selected ones to copy queue)
            if not singleFileSelection:
                currentFile = []
                selectedFolderPath = ""

                if len(fb.getDirList()):
                    currentFile = fb.getDirList()[actualFilePointer - 1]
                    selectedFolderPath = fb.structCurrentPath() + currentFile
                # Add to copy
                if currentFile not in selectedDisplay:
                    # Decrement Available Patches
                    if os.path.isdir(selectedFolderPath):
                        if availableSlots - len(listdir(selectedFolderPath)) >= 0 or config["OP_1_Mounted_Dir"] == "":
                            selectedDisplay.append(currentFile)
                            for i in listdir(selectedFolderPath):
                                fb.addToCopyQueue(currentFile + "/" + i)
                                if "media" not in fb.structCurrentPath():
                                    availableSlots -= 1
                        else:
                            print("Over Shoot")

                    else:
                        if availableSlots - 1 >= 0 or config["OP_1_Mounted_Dir"] == "":
                            fb.addToCopyQueue(currentFile)
                            selectedDisplay.append(currentFile)
                            if "media" not in fb.structCurrentPath():
                                availableSlots -= 1
                        else:
                            print("Over Shoot")

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
            if not singleFileSelection:
                if len(fb.getDirList()):
                    currentFile = fb.getDirList()[actualFilePointer - 1]
                    selectedFolderPath = fb.structCurrentPath() + currentFile
                    fileCount = len(fb.getCopyQueue())

                if len(selectedDisplay) == 0 and len(fb.getCopyQueue()) == 0:
                    rtn = RenderOptionsMenu(["New Folder"], sort=False)
                    if "New Folder" in rtn:
                        name = renderRename("/New Folder", jsutName=True)
                        if name != "":
                            print(join(fb.currentDirPath, name), "Folder Created")
                            try:
                                createEmptyFolder(fb.currentDirPath, name)
                                fb.updatePage()
                            except OSError:
                                print("Folder can not be created")
                            print ("Folder Created")
                        else:
                            print ("Create Folder Canceled")

                # if len(fb.getCopyQueue()) == 0 or len(selectedDisplay) == 1:
                #     # Takes case if non of the folder or file is selected
                #     if os.path.isdir(selectedFolderPath):
                #         for i in listdir(selectedFolderPath):
                #             fb.addToCopyQueue(currentFile + "/" + i)
                #         fileCount = len(fb.getCopyQueue())
                #         # availableSlots += len(fb.getCopyQueue())
                #         rtn = RenderOptionsMenu(
                #             [upload_download + " " + str(fileCount) + " Patches",
                #              "Delete " + str(fileCount) + "Patches", "New Folder"], sort=False)
                #     else:
                #         fb.addToCopyQueue(currentFile)
                #         # availableSlots += 1
                #         rtn = RenderOptionsMenu([upload_download, "Rename", "Delete"], sort=False)

                else:
                    if fileCount == 1:
                        rtn = RenderOptionsMenu([upload_download, "Rename", "Move", "Delete"], sort=False)

                    else:
                        rtn = RenderOptionsMenu(
                            [upload_download + " " + str(fileCount) + " Patches", "Move " + str(fileCount) + " Patches",
                             "Delete " + str(fileCount) + "Patches"], sort=False)

                    # if rtn == "RETURN":
                    #     availableSlots += fileCount
            else:
                currentFile = fb.getDirList()[actualFilePointer - 1]
                selectedFolderPath = fb.structCurrentPath() + currentFile
                if os.path.isdir(selectedFolderPath):
                    return selectedFolderPath
                    pass
                else:
                    rtn = RenderOptionsMenu(["Copy / Overwrite", "Cancel"], title="Upload to OP-Z", sort=False)

                if "Copy / Overwrite" in rtn:
                    currentFile = fb.getDirList()[actualFilePointer - 1]
                    selectedFolderPath = fb.structCurrentPath() + currentFile
                    return selectedFolderPath

                if "Cancel" in rtn:
                    print("Canceled")
                    return

            # Main File Actions
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

            elif "Move" in rtn:
                # Move files within folder
                if fb.getCopyQueue():
                    temp = fb.getCopyQueue()[0]
                    parentDir = dirname(dirname(temp))
                    parentDirLst = os.listdir(parentDir)
                    rtn = RenderOptionsMenu(parentDirLst, title="Move To ...", sort=False)
                    if "RETURN" not in rtn:
                        try:
                            moveFilesToFolder(fb.getCopyQueue(), os.path.join(parentDir, rtn))
                            fb.clearCopyQueue()
                            selectedDisplay = []
                            fb.updatePage()

                        except OSError:
                            print("File Moving Error")


            elif "Delete" in rtn:
                # List allowed
                # if check_OP_1_Connection() and config["OP_1_Mounted_Dir"] != "":
                try:
                    if len(fb.getCopyQueue()) == 0:
                        # Empty Folder Selected
                        currentFolder = fb.getDirList()[actualFilePointer - 1]
                        print(join(fb.structCurrentPath(), currentFolder))
                        shutil.rmtree(join(fb.structCurrentPath(), currentFolder))
                    else:
                        # Deleting folder that have patches
                        print("In!!")
                        deleteHelper(fb.getCopyQueue())
                        # Current Folder is empty and no longer existed go to Prev Page
                        if not os.path.exists(fb.structCurrentPath()):
                            fb.prevPage()
                            selectedDisplay = []
                            selected = []
                            fb.clearCopyQueue()
                    # Finished deleting, refresh the file list for display
                    fb.updatePage()

                except OSError:
                    pass

            elif "Rename" in rtn:
                # Only one item is allowed
                # Rename Page
                print(fb.getCopyQueue()[0])
                renderRename(str(fb.getCopyQueue()[0]))
                fb.updatePage()

            # currentCursor = 1
            # actualFilePointer = 1
            # fb.clearCopyQueue()
            # selectedDisplay = []

            # Update Remain Available Patches Here
        sampler, synth, drum = update_Current_Storage_Status()


# Python Bus Error can not release resource. Rebuild needed.


def renderOPZFolder(path, upload_download):
    """
    Slight modification to the renderOP1Folder since it is in different folder layout

    :param path: Path the OPZ mounted dir
    :param upload_download: String: Selection menu type
    :return:
    """
    actualFilePointer = 1
    currentCursor = 1
    shortArray = []
    interFolder = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]

    fb = fileBrowserDT(path)
    # RenderFolders
    while True:
        image = Image.new('1', (128, 64))
        draw = ImageDraw.Draw(image)
        # draw.rectangle([(-1, 0), (128, 64)], 'black', 'white')
        draw.rectangle([(0, 0), (128, 10)], 'white')
        draw.text((2, -1), os.path.basename(fb.structCurrentPath()[:-1]), fill='black', font=getFont())
        shortArray = shiftArray(fb.getDirList(), shortArray, 0)
        # Render Sub-folder files
        if interFolder == fb.getDirList():
            counter = 1
            for i in shortArray:
                subFolderFileName = listdir(fb.currentDirPath + "/" + str(fb.histQueue[-1]) + "/" + str(i))
                if len(subFolderFileName) == 0:
                    subFolderFileName = "---Empty---"
                else:
                    subFolderFileName = subFolderFileName[0]
                    subFolderFileName = subFolderFileName.replace('.aif', '')
                    subFolderFileName = subFolderFileName.replace('.engine', '  [Engine]')
                    subFolderFileName = subFolderFileName.replace('~', '')
                draw.text((10, counter * 10), str(i) + " - " + str(subFolderFileName), fill='white', font=getFont())
                # Render next item from current Directory
                counter += 1
        else:
            counter = 1
            for i in shortArray:
                i = i.replace("-", " - ")
                draw.text((10, counter * 10), str(i), fill='white', font=getFont())
                # Render next item from current Directory
                counter += 1

        # Render cursor
        draw.text((0, currentCursor * 10), ">", fill='white', font=getFont())

        # Render Scroll Bar
        scrollBarXLocation = 127
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
                fb.clearCopyQueue()
                fb.prevPage()
            else:
                return

        if key == "RIGHT":
            if interFolder != fb.getDirList():
                fb.selectNewPath(fb.getDirList()[actualFilePointer - 1])
                currentCursor = 1
                actualFilePointer = 1

        if key == "CENTER":
            pass

        if key == "A":
            pass
            # return

        if key == "B":
            currentFile = fb.getDirList()[actualFilePointer - 1]
            rtn = RenderOptionsMenu([upload_download, "Delete"], sort=False)
            if "Choose From OP-1 Lib" in rtn:
                if check_OP_Z_Connection() and config["OP_Z_Mounted_Dir"] != "":
                    try:
                        # Single file path selected from the OP-1 patch lib
                        # Start a new file browser / selecter
                        singleFile = renderFolders(savePaths["Local_Patches"], "Upload to OPZ",
                                                   savePaths["OP_Z_System_Path"], singleFileSelection=True)

                        # User selected a dir but not a file.
                        if os.path.isdir(singleFile):
                            errorMessage = Image.new('1', (128, 64))
                            draw = ImageDraw.Draw(errorMessage)
                            draw.text((0, 25), "Folder is not allowed!", font=getFont(), fill='white')
                            displayImage(errorMessage)
                            time.sleep(1)

                        # Ensure the selected file is supported on OP-Z system
                        type, fx, lfo = analyzeAIF(singleFile)
                        # Correct File. Execute file transfer
                        if type == "Drum" or type == "Sampler":
                            destPath = join(path, fb.histQueue[-1])
                            # Clear Dir on OPZ
                            clearUnderFolder(join(destPath, fb.getDirList()[actualFilePointer - 1]))
                            target = join(destPath, join(fb.getDirList()[actualFilePointer - 1], basename(singleFile)))
                            print("Transfer Single Patch to OPZ", singleFile, target)
                            try:
                                shutil.copy2(singleFile, target)
                            except:
                                pass
                            print("Done")

                        # File not supported on OP-Z
                        else:
                            errorMessage = Image.new('1', (128, 64))
                            draw = ImageDraw.Draw(errorMessage)
                            draw.text((0, 15), "File not supported", font=getFont(), fill='white')
                            draw.text((0, 25), "on OP-Z", font=getFont(), fill='white')
                            displayImage(errorMessage)
                            time.sleep(1)
                    except:
                        pass

            elif "Delete" in rtn:
                if check_OP_Z_Connection() and config["OP_Z_Mounted_Dir"] != "":
                    try:
                        destPath = join(path, fb.histQueue[-1])
                        target = join(destPath, join(fb.getDirList()[actualFilePointer - 1]))
                        print("Deleting file under...", target)
                        # Clear Dir on OPZ
                        clearUnderFolder(target)
                        print("Deleted")
                    except:
                        pass
                    fb.updatePage()
