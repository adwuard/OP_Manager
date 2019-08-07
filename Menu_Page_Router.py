import os
import subprocess
import time
from subprocess import call
from PIL import Image, ImageDraw

from Midi import MidiTool
from SSH_Service import SSH_Service
from FileBrowser import renderFolders, RenderOptionsMenu, renderRename, renderOPZFolder
from GPIO_Init import getAnyKeyEvent, displayImage, getFont, getKeyStroke, getSmallFont, displayPng
from OP_1_Connection import update_Current_Storage_Status, unmount_OP_1, check_OP_1_Connection, do_mount, \
    check_OP_Z_Connection
from OP_1_Backup import OP1Backup
from UPS_Battery_Module import readCapacity, getBatteryImagePath
from file_util import getDirFileList, deleteHelper
from menu_structure import MainPage
from config import config, savePaths, batteryConfig

__author__ = "Hsuan Han Lai (Edward Lai)"
__date__ = "2019-04-02"

workDir = os.path.dirname(os.path.realpath(__file__))


class PageRouter:
    pageQue = [MainPage]
    currentDist = []
    cursorHistory = []
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

            if batteryConfig["enable"]:
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
                self.cursorHistory.append(cur)
                self.actionRouter(currentDist[cur][1])
            else:
                self.pageQue.append(currentDist[cur][1])
                self.cursorHistory.append(cur)
            self.renderPage(0, 1)
            return

        # Previous Page (Left)
        if action == -1:
            if len(self.pageQue) > 1:
                self.pageQue = self.pageQue[:-1]
                # Previous Cursor History Recall
                cur = self.cursorHistory[len(self.cursorHistory) - 1]
                self.cursorHistory = self.cursorHistory[:-1]
            return cur
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

        # ===========Patches Actions===========
        if event == "OP1_Synth_Patches":
            if check_OP_1_Connection() and config["OP_1_Mounted_Dir"] != "":
                renderFolders(config["OP_1_Mounted_Dir"] + "/synth", "Backup", savePaths["Local_Synth"])

        if event == "OP1_Drum_Patches":
            if check_OP_1_Connection() and config["OP_1_Mounted_Dir"] != "":
                renderFolders(config["OP_1_Mounted_Dir"] + "/drum", "Backup", savePaths["Local_Drum"])

        if event == "UploadSynthPatches":
            renderFolders(savePaths["Local_Synth"], "Upload", config["OP_1_Mounted_Dir"] + "/synth")

        if event == "UploadDrumPatches":
            renderFolders(savePaths["Local_Drum"], "Upload", config["OP_1_Mounted_Dir"] + "/drum")

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

        # =================== OP-Z Action Routes ====================
        if event == "act_Freeze_State_OPZ":
            if check_OP_Z_Connection() and config["OP_Z_Mounted_Dir"] != "":
                displayPng(workDir + "/Assets/Img/BackupProject.png")
                time.sleep(0.1)
                try:
                    state = OP1Backup()
                    state.backupOPZState()
                    displayPng(workDir + "/Assets/Img/Done.png")
                    time.sleep(0.1)
                    getAnyKeyEvent()
                except:
                    print("File Transfer Error")
                    self.renderErrorMessagePage("File Transfer Error")
            # self.renderPage(-1, 1)

        if event == "act_Recall_State_To_OPZ":
            # rtn = "RETURN"
            while True:
                temp = RenderOptionsMenu(getDirFileList(savePaths["OP_Z_Local_Backup_States_Path"]), "Recall State")
                if temp == "RETURN":
                    break
                else:
                    rtn = RenderOptionsMenu(["Upload", "Rename", "Delete"])
                    if rtn == "Upload":
                        if check_OP_Z_Connection():
                            displayPng(workDir + "/Assets/Img/UploadingProject.png")
                            time.sleep(0.1)
                            try:
                                state = OP1Backup()
                                print("Recall File: ", os.path.join(savePaths["OP_Z_Local_Backup_States_Path"], temp))
                                state.loadStateToOPZ(os.path.join(savePaths["OP_Z_Local_Backup_States_Path"], temp))
                                displayPng(workDir + "/Assets/Img/Done.png")
                                time.sleep(0.1)
                                getAnyKeyEvent()
                            except:
                                print("File Transfer Error")
                                self.renderErrorMessagePage("File Transfer Error")

                    elif rtn == "Rename":
                        renderRename(os.path.join(savePaths["OP_Z_Local_Backup_States_Path"], temp))
                    elif rtn == "Delete":
                        deleteHelper([os.path.join(savePaths["OP_Z_Local_Backup_States_Path"], temp)])
                    elif rtn == "RETURN":
                        pass

            # self.renderPage(-1, 1)

        if event == "OPZ_Patches":
            if check_OP_Z_Connection() and config["OP_Z_Mounted_Dir"] != "":
                renderOPZFolder(config["OP_Z_Mounted_Dir"] + "/samplepacks", "Choose From OP-1 Lib")

        if event == "MIDI_Host":
            midi = MidiTool()
            midi.usbMIDIOut()

        # ===================== Server ==================
        if event == "Check_IP":
            SSH = SSH_Service()
            # print(SSH.get_ip_address())
            # print(SSH.get_current_connected())
            # SSH.start_SSH_Service()
            username = os.getlogin()
            IP = SSH.get_ip_address()
            IP = IP.replace(".", " . ")

            IPDisplay = Image.new('1', (128, 64))
            draw = ImageDraw.Draw(IPDisplay)
            draw.rectangle([(0, 0), (128, 10)], 'white')
            draw.text((50, 0), "SSH IP", font=getFont(), fill='black')
            draw.text((5, 15), "User : "+username , font=getFont(), fill='white')
            draw.text((5, 30), "IP : " + IP, font=getFont(), fill='white')
            draw.text((5, 50), "Password : sys paswd", font=getFont(), fill='white')
            displayImage(IPDisplay)
            getAnyKeyEvent()

        if event == "Server IP":
            SSH = SSH_Service()
            IP = SSH.get_ip_address()

            IPDisplay = Image.new('1', (128, 64))
            draw = ImageDraw.Draw(IPDisplay)
            draw.rectangle([(0, 0), (128, 10)], 'white')
            draw.text((30, 0), "Browser App", font=getFont(), fill='black')
            draw.text((0, 15), "Connect To Wifi", font=getFont(), fill='white')
            draw.text((0, 25), "Open Browser, Then", font=getFont(), fill='white')
            draw.text((0, 35), "-------------------------------------------------------", font=getSmallFont(), fill='white')
            draw.text((0, 40), "http://"+IP+":", font=getFont(), fill='white')
            draw.text((10, 53), "/5000/files", font=getFont(), fill='white')

            displayImage(IPDisplay)
            getAnyKeyEvent()

        # ===========Eject Actions===========
        if event == "act_ESC_Eject":
            try:
                unmounting = Image.new('1', (128, 64))
                draw = ImageDraw.Draw(unmounting)
                draw.text((0, 25), "Ejecting....", font=getFont(), fill='white')
                displayImage(unmounting)
                if unmount_OP_1():
                    time.sleep(1)
                    unmounted = Image.new('1', (128, 64))
                    draw = ImageDraw.Draw(unmounted)
                    draw.text((0, 25), "Ejected", font=getFont(), fill='white')
                    displayImage(unmounted)
                    time.sleep(1)
            except:
                pass

        # ========= POWER OFF ====================
        if event == "act_POWER_OFF":
            image = Image.new('1', (128, 64))
            image.paste(Image.open(workDir + "/Assets/Img/PowerOff.png").convert("1"))
            displayImage(image)
            time.sleep(1.0)
            # call("sudo shutdown -h now", shell=True)
            call("sudo poweroff", shell=True)


        if event == "checkStorage":
            image = Image.new('1', (128, 64))
            image.paste(Image.open(workDir + "/Assets/Img/Storage_64.png").convert("1"))
            draw = ImageDraw.Draw(image)

            if check_OP_1_Connection() and config["OP_1_Mounted_Dir"] != "":
                sampler, synth, drum = update_Current_Storage_Status()
            else:
                sampler, synth, drum = 42, 100, 42

            Disk = str(subprocess.check_output("df -h | awk '$NF==\"/\"{printf \"%d/%dGB %s\", $3,$2,$5}'", shell=True))
            Disk = Disk.replace("b\'", "")
            Disk = Disk.replace("\'", "")
            draw.text((50, 13), str(Disk), font=getFont(), fill="white")  # Disk Storage Render
            draw.text((28, 48), str(config["Max_Synth_Sampler_patches"] - sampler), font=getFont(), fill="white")
            draw.text((70, 48), str(config["Max_Synth_Synthesis_patches"] - synth), font=getFont(), fill="white")
            draw.text((112, 48), str(config["Max_Drum_Patches"] - drum), font=getFont(), fill="white")
            displayImage(image)
            getAnyKeyEvent()  # Press any key to proceed
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
