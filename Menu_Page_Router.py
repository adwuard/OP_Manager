import os
import subprocess
import time
from os.path import basename, isdir
from shutil import rmtree
from subprocess import call

from PIL import Image, ImageDraw
from smbus2 import smbus2
from FileBrowser import renderFolders, RenderOptionsMenu, renderRename
from GPIO_Init import getAnyKeyEvent, displayImage, getFont, getKeyStroke, getSmallFont, displayPng
from Midi import startMidi, usbMIDIOut
from OP_1_Connection import update_Current_Storage_Status, unmount_OP_1, check_OP_1_Connection, do_mount
from OP_1_Backup import OP1Backup
from UPS_Battery_Module import readCapacity, getBatteryImagePath
from file_util import getDirFileList, deleteHelper
from menu_structure import MainPage
from config import config, savePaths
from run import start

__author__ = "Hsuan Han Lai (Edward Lai)"
__date__ = "2019-04-02"

workDir = os.path.dirname(os.path.realpath(__file__))


class PageRouter:
    pageQue = [MainPage]
    currentDist = []
    font = getFont()
    smallFont = getSmallFont()

    def __init__(self):
        self.processState = False
        self.cursor = 1

    def getListSize(self):
        return len(self.pageQue[-1])

    def renderPage(self, action, cur):
        frameSize = (128, 64)
        image = Image.new('1', frameSize)
        # Battery Icon


        draw = ImageDraw.Draw(image)
        currentDist = self.pageQue[-1]
        # Stay on same page (Up Down) Render Standard Menu
        if action == 0:
            draw.rectangle([(-1, 0), (128, 64)], 'black', 'white')
            draw.rectangle([(0, 0), (128, 10)], 'white')
            draw.text((2, 0), str(currentDist[0][0]), fill='black', font=self.font)

            # Battery Level in percentage
            # draw.text((105, 0), readCapacity(), fill='black', font=self.smallFont)

            # Battery Level Icon
            icon = Image.open(os.path.join(workDir, getBatteryImagePath(readCapacity()))).convert("1")
            image.paste(icon, (117, 0))

            for i in range(1, len(currentDist)):
                draw.text((10, i * 10), str(currentDist[i][0]), fill='white', font=self.font)
            draw.text((2, cur * 10), ">", fill='white', font=self.font)

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

    def actionRouter(self, event):
        # =============Projects Actions ===========
        if event == "act_Backup_Project_From_OP_1":
            if check_OP_1_Connection() and config["OP_1_Mounted_Dir"] != "":
                displayPng(workDir + "/Assets/Img/BackupProject.png")
                time.sleep(0.1)
                try:

                    tape = OP1Backup()
                    tape.copyToLocal()
                    displayPng(workDir + "/Assets/Img/Done.png")
                    time.sleep(0.1)
                    getAnyKeyEvent()
                except:
                    print("File Transfer Error")
                    self.renderErrorMessagePage("File Transfer Error")
            self.renderPage(-1, 1)

        if event == "act_Load_Project_From_Local_only_tracks":
            if check_OP_1_Connection() and config["OP_1_Mounted_Dir"] != "":
                displayPng(workDir + "/Assets/Img/BackupProject.png")
                time.sleep(0.1)
                try:
                    tape = OP1Backup()
                    tape.copyOnlyTapesToLocal()
                    displayPng(workDir + "/Assets/Img/Done.png")
                    time.sleep(0.1)
                    getAnyKeyEvent()
                except:
                    print("File Transfer Error")
                    self.renderErrorMessagePage("File Transfer Error")
            self.renderPage(-1, 1)

        if event == "act_Load_Project_From_Local":
            # rtn = "RETURN"
            while True:
                temp = RenderOptionsMenu(getDirFileList(savePaths["Local_Projects"]), "Projects")
                if temp == "RETURN":
                    break
                else:
                    rtn = RenderOptionsMenu(["Upload", "Rename", "Delete"])
                    if rtn == "Upload":
                        if check_OP_1_Connection() and config["OP_1_Mounted_Dir"] != "":
                            displayPng(workDir + "/Assets/Img/UploadingProject.png")
                            time.sleep(0.1)
                            try:
                                tape = OP1Backup()
                                tape.loadProjectToOP1(os.path.join(savePaths["Local_Projects"], temp))
                            except:
                                print("File Transfer Error")
                                self.renderErrorMessagePage("File Transfer Error")

                    elif rtn == "Rename":
                        renderRename(os.path.join(savePaths["Local_Projects"], temp))
                    elif rtn == "Delete":
                        deleteHelper([os.path.join(savePaths["Local_Projects"], temp)])
                    elif rtn == "RETURN":
                        pass

            self.renderPage(-1, 1)

        # ===========Patches Actions===========
        if event == "OP1_Synth_Patches":
            if check_OP_1_Connection() and config["OP_1_Mounted_Dir"] != "":
                renderFolders(config["OP_1_Mounted_Dir"] + "/synth", "Backup", savePaths["Local_Synth"])
            self.renderPage(-1, 1)

        if event == "OP1_Drum_Patches":
            if check_OP_1_Connection() and config["OP_1_Mounted_Dir"] != "":
                renderFolders(config["OP_1_Mounted_Dir"] + "/drum", "Backup", savePaths["Local_Drum"])
            self.renderPage(-1, 1)

        if event == "UploadSynthPatches":
            renderFolders(savePaths["Local_Synth"], "Upload", config["OP_1_Mounted_Dir"] + "/synth")
            self.renderPage(-1, 1)

        if event == "UploadDrumPatches":
            renderFolders(savePaths["Local_Drum"], "Upload", config["OP_1_Mounted_Dir"] + "/drum")
            self.renderPage(-1, 1)

        if event == "act_5_Backup_All_Patches":
            if check_OP_1_Connection() and config["OP_1_Mounted_Dir"] != "":
                image = Image.new('1', (128, 64))
                image.paste(Image.open(workDir + "/Assets/Img/DownloadPatches.png").convert("1"))
                displayImage(image)
                time.sleep(0.1)
                try:
                    bk = OP1Backup()
                    bk.backupOP1Patches()

                    displayPng(workDir + "/Assets/Img/Done.png")
                    time.sleep(0.1)
                    getAnyKeyEvent()
                except:
                    print("File Transfer Error")
                    self.renderErrorMessagePage("File Transfer Error")
            self.renderPage(-1, 1)

        if event == "USB_MIDI_In_Test":
            startMidi()
            self.renderPage(-1, 1)

        if event == "USB_MIDI_Out_Test":
            usbMIDIOut()
            self.renderPage(-1, 1)

        # ===========Eject Actions===========
        if event == "act_ESC_Eject_OP_1":
            try:
                if unmount_OP_1():
                    print("Ejected")
            except:
                print("Error")
            self.renderPage(-1, 1)

        # ============= MOUNT OPTION ==============
        if event == "act_ESC_Mount_OP_1":
            try:
                if do_mount():
                    print("Mounted")
            except:
                print("Error")
            self.renderPage(-1, 1)
        # ========= POWER OFF ====================
        if event == "act_POWER_OFF":
            image = Image.new('1', (128, 64))
            image.paste(Image.open(workDir + "/Assets/Img/PowerOff.png").convert("1"))
            displayImage(image)
            time.sleep(1.0)
            call("sudo shutdown -h now", shell=True)

        if event == "checkStorage":
            if check_OP_1_Connection() and config["OP_1_Mounted_Dir"] != "":
                image = Image.new('1', (128, 64))
                image.paste(Image.open(workDir + "/Assets/Img/Storage_64.png").convert("1"))
                draw = ImageDraw.Draw(image)
                sampler, synth, drum = update_Current_Storage_Status()
                Disk = subprocess.check_output("df -h | awk '$NF==\"/\"{printf \"%d/%dGB %s\", $3,$2,$5}'", shell=True)
                draw.text((50, 13), Disk, font=getFont(), fill="white")  # Disk Storage Render
                draw.text((28, 48), str(config["Max_Synth_Sampler_patches"] - sampler), font=getFont(), fill="white")
                draw.text((70, 48), str(config["Max_Synth_Synthesis_patches"] - synth), font=getFont(), fill="white")
                draw.text((112, 48), str(config["Max_Drum_Patches"] - drum), font=getFont(), fill="white")
                displayImage(image)
                getAnyKeyEvent()  # Press any key to proceed
            else:
                print("Not Connected")
            self.renderPage(-1, 1)

    # Useful in "Are you sure to delete.", "Are you sure to rename"
    def renderConfirmation(self, message=""):
        """
        Renders The Message and ask for yes or no
        :return: Boolean
        """
        pass

    def renderErrorMessagePage(self, errorMessage=""):
        """
        Renders any given massage on to the screen, and wait for any key input to continue
        :param errorMessage: String message you want to display on the screen
        :return: N/A
        """
        pass
