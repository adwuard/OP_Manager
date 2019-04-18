import os
import subprocess
import time
from PIL import Image, ImageDraw
from FileBrowser import renderFolders, RenderOptionsMenu
from GPIO_Init import getAnyKeyEvent, displayImage, getFont
from OP_1_Connection import update_Current_Storage_Status, unmount_OP_1, check_OP_1_Connection, do_mount
from TapesBackup import TapeBackup
from file_util import getDirFileList
from menu_structure import MainPage
from config import config, savePaths
from run import start

__author__ = "Hsuan Han Lai (Edward Lai)"
__date__ = "2019-04-02"

workDir = os.path.dirname(os.path.realpath(__file__))


class PageRouter:
    pageQue = [MainPage]
    currentDist = []

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

    def actionRouter(self, event):
        # =============Projects Actions ===========
        if event == "act_Backup_Project_From_OP_1":
            if check_OP_1_Connection() and config["OP_1_Mounted_Dir"] != "":
                image = Image.new('1', (128, 64))
                image.paste(Image.open(workDir + "/Assets/Img/BackupProject.png").convert("1"))
                displayImage(image)
                time.sleep(0.1)
                try:
                    tape = TapeBackup()
                    tape.copyToLocal()
                    image = Image.new('1', (128, 64))
                    image.paste(Image.open(workDir + "/Assets/Img/Done.png").convert("1"))
                    displayImage(image)
                    time.sleep(0.1)
                    getAnyKeyEvent()
                except:
                    print("File Transfer Error")
                    self.renderErrorMessagePage("File Transfer Error")
            self.renderPage(-1, 1)

        if event == "act_Load_Project_From_Local":
            rtn = "RETURN"
            RenderOptionsMenu(getDirFileList(savePaths["Local_Projects"]), "Projects")
            while rtn == "RETURN":
                rtn = RenderOptionsMenu(["Upload", "Rename", "Delete"])
                temp = RenderOptionsMenu(getDirFileList(savePaths["Local_Projects"]), "Projects")
                if temp == "RETURN":
                    break
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
            image = Image.new('1', (128, 64))
            image.paste(Image.open(workDir + "/Assets/Img/BackupProject.png").convert("1"))
            displayImage(image)
            time.sleep(0.1)
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
            self.renderPage(-1, 1)

    def renderStandardMenu(self, draw, currentDist=None, cursor=1):
        font = getFont()
        draw.rectangle([(-1, 0), (128, 64)], 'black', 'white')
        draw.rectangle([(0, 0), (128, 10)], 'white')
        draw.text((2, 0), str(currentDist[0][0]), fill='black', font=font)
        for i in range(1, len(currentDist)):
            draw.text((10, i * 10), str(currentDist[i][0]), fill='white', font=font)
        draw.text((2, cursor * 10), ">", fill='white', font=font)

    def renderRename(self, file=""):
        """
        Given a file path, renders for rename, with confirmation for rename or cancel,
        :param file:
        :return:
        """

        pass

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
