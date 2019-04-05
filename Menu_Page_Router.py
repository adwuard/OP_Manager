import os
import subprocess
import time
from PIL import ImageFont, Image, ImageDraw
from FileBrowser import renderFolders
from GPIO_Init import getAnyKeyEvent, displayImage, getFont
from OP_1_Connection import update_Current_Storage_Status, get_OP1_Storage_Status, currentStorageStatus, getMountPath, \
    unmount_OP_1
from menu_structure import MainPage
from config import config, savePaths
from run import start

__author__ = "Hsuan Han Lai (Edward Lai)"
__date__ = "2019-04-02"


# This is for the local debugging, preview screen in Computer
# def rescale_frame(frame, percent=75):
#     width = int(frame.shape[1] * percent / 100)
#     height = int(frame.shape[0] * percent / 100)
#     dim = (width, height)
#     return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

def displayLine(line, indent):
    return indent, line * 10


class PageRouter:
    pageQue = [MainPage]
    currentDist = []

    fullPage = []
    currentPage = []
    realPointer = 1
    currentSelector = 1

    def __init__(self):
        self.processState = False
        self.cursor = 1
        self.cursorMax = 0

    def getListSize(self):
        return len(self.pageQue[-1])

    def renderPage(self, action, cur):
        frameSize = (128, 64)
        image = Image.new('1', frameSize)
        draw = ImageDraw.Draw(image)
        currentDist = self.pageQue[-1]
        # arr = currentDist[0]

        # Stay on same page (Up Down)
        if action == 0:
            self.renderStandardMenu(draw, currentDist, cur)

        # Action Events (RIGHT)
        if action == 1:
            if type(currentDist[cur][1]) is str:
                self.pageQue.append(["Action Page Route", -1])
                self.actionRouter(currentDist[cur][1])
            else:
                self.pageQue.append(currentDist[cur][1])
            self.renderPage(0, 1)
            return

        # Previous Page (Left)
        if action == -1:
            if len(self.pageQue) > 1:
                self.pageQue = self.pageQue[:-1]
            self.renderPage(0, 1)
            return

        displayImage(image)

        # npImage = np.asarray(image)
        # frameBGR = cv2.cvtColor(npImage, cv2.COLOR_RGB2BGR)
        # newFrame = rescale_frame(frameBGR, percent=300)
        # cv2.imshow('Test', newFrame)

    def actionRouter(self, event):
        # =============Projects Actions ===========
        if event == "act_Backup_Project_From_OP_1":
            image = Image.new('1', (128, 64))
            image.paste(Image.open("Assets/Img/BackupProject.png").convert("1"))
            displayImage(image)
            time.sleep(0.1)
            # try:
            #     tape = TapeBackup()
            #     tape.copyToLocal()
            # except:
            #     print("File Transfer Error")
            time.sleep(8)
            image = Image.new('1', (128, 64))
            image.paste(Image.open("Assets/Img/Done.png").convert("1"))
            displayImage(image)
            time.sleep(0.1)
            getAnyKeyEvent()
            self.renderPage(-1, 1)

        if event == "act_Load_Project_From_Local":
            renderFolders(savePaths["Local_Projects"], -9999, 0)
            self.renderPage(-1, 1)

        # ===========Patches Actions===========
        if event == "OP1_Synth_Patches":
            renderFolders(getMountPath() + "/synth", currentStorageStatus["synth"], 1)
            self.renderPage(-1, 1)

        if event == "OP1_Drum_Patches":
            renderFolders(getMountPath() + "/drum", currentStorageStatus["drum"], 1)
            self.renderPage(-1, 1)

        if event == "UploadSynthPatches":
            renderFolders(savePaths["Local_Synth"], currentStorageStatus["synth"], 1)
            self.renderPage(-1, 1)

        if event == "UploadDrumPatches":
            renderFolders(savePaths["Local_Drum"], currentStorageStatus["drum"], 1)
            self.renderPage(-1, 1)

        if event == "act_5_Backup_All_Patches":
            pass

        # ===========Eject Actions===========
        if event == "act_ESC_Eject_OP_1":
            # unmount_OP_1()
            cmd = "sudo umount " + config["OP_1_Mounted_Dir"]
            try:
                os.system(cmd)
            except:
                pass
            print("Ejected")
            time.sleep(5)
            start()
            # pass

        if event == "checkStorage":
            image = Image.new('1', (128, 64))
            image.paste(Image.open("Assets/Img/Storage_64.png").convert("1"))
            draw = ImageDraw.Draw(image)
            update_Current_Storage_Status()
            statusDist = get_OP1_Storage_Status()
            remainSynth = config["Max_Synth_Synthesis_patches"] - statusDist["synth"]
            remainSampler = config["Max_Synth_Sampler_patches"] - statusDist["sampler"]
            remainDrum = config["Max_Drum_Patches"] - statusDist["drum"]
            Disk = subprocess.check_output("df -h | awk '$NF==\"/\"{printf \"%d/%dGB %s\", $3,$2,$5}'", shell=True)
            draw.text((50, 13), Disk, font=getFont(), fill="white")
            draw.text((28, 48), str(remainSampler), font=getFont(), fill="white")
            draw.text((70, 48), str(remainSynth), font=getFont(), fill="white")
            draw.text((112, 48), str(remainDrum), font=getFont(), fill="white")
            displayImage(image)
            getAnyKeyEvent()
            self.renderPage(-1, 1)

    def renderStandardMenu(self, draw, currentDist, cursor):
        font = ImageFont.truetype("Fonts/Georgia Bold.ttf", 10)
        draw.rectangle([(-1, 0), (128, 64)], 'black', 'white')
        iterCount = 0
        for i in currentDist:
            if iterCount == 0:
                draw.rectangle([(0, 0), (128, 10)], 'white')
                draw.text(displayLine(iterCount, 2), str(i[0]), fill='black', font=font)
            else:
                draw.text(displayLine(iterCount, 10), str(i[0]), fill='white', font=font)
            iterCount += 1
        # if cursor != -1:
        draw.text(displayLine(cursor, 2), ">", fill='white', font=font)
