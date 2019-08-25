import os
import time
import RPi.GPIO as GPIO

from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1322, ssd1327, ssd1351, ssd1331, sh1106
from PIL import ImageFont, Image

# from config import displayConfig

__author__ = "Hsuan Han Lai (Edward Lai)"
__date__ = "2019-04-02"

workDir = os.path.dirname(os.path.realpath(__file__))

# Key Press Input Pins:
L_pin, R_pin, C_pin, U_pin, D_pin = 27, 23, 4, 17, 22
A_pin, B_pin = 5, 6

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(A_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(B_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(L_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(R_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(U_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(D_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(C_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Open i2c address port
# serial = i2c(port=displayConfig["port"], address=displayConfig["address"])
serial = i2c(port=1, address=0x3c)


# Get Config Setting and initialize the compatible OLED device
# Compatible devices -> SSD1306, SSD1309, SSD1322, SSD1325, SSD1327, SSD1331, SSD1351 and SH1106
# if config.displayConfig["DisplayType"] == "SSD1306":
#     disp = ssd1306(serial, rotate=config.displayConfig["Rotation"])
# elif config.displayConfig["DisplayType"] == "SSD1309":
#     disp = ssd1309(serial, rotate=config.displayConfig["Rotation"])
# elif config.displayConfig["DisplayType"] == "SSD1322":
#     disp = ssd1322(serial, rotate=config.displayConfig["Rotation"])
# elif config.displayConfig["DisplayType"] == "SSD1325":
#     disp = ssd1325(serial, rotate=config.displayConfig["Rotation"])
# elif config.displayConfig["DisplayType"] == "SSD1327":
#     disp = ssd1327(serial, rotate=config.displayConfig["Rotation"])
# elif config.displayConfig["DisplayType"] == "SSD1331":
#     disp = ssd1331(serial, rotate=config.displayConfig["Rotation"])
# elif config.displayConfig["DisplayType"] == "SSD1351":
#     disp = ssd1351(serial, rotate=config.displayConfig["Rotation"])
# elif config.displayConfig["DisplayType"] == "SH1106":
#     disp = sh1106(serial, rotate=config.displayConfig["Rotation"])
# elif config.displayConfig["DisplayType"] == "":
#     disp = ssd1306(serial, rotate=config.displayConfig["Rotation"])

# disp = sh1106(serial, rotate=2)
disp = ssd1306(serial, rotate=0)

def getLargeFont():
    return ImageFont.truetype(workDir + "/Fonts/Georgia Bold.ttf", 12)


def getFont():
    return ImageFont.truetype(workDir + "/Fonts/Georgia Bold.ttf", 10)


def getSmallFont():
    return ImageFont.truetype(workDir + "/Fonts/Georgia Bold.ttf", 9)


def clearDisplay():
    """
        Connector function to clear OLED Display
        :param img:
        :return: None
    """
    disp.clear()


def displayImage(img):
    """
    Connector function to send PIL images on to the OLED Display
    :param img:
    :return: None
    """
    disp.display(img)


def displayPng(pathToImage):
    """
    Given path to image. This function translate to PIL image and display on to the OLED display
    :param pathToImage:
    :return:
    """
    image = Image.new('1', (128, 64))
    image.paste(Image.open(pathToImage).convert("1"))
    displayImage(image)


def getKeyStroke():
    """
    Blocking version of getting a key
    :return: "UP" | "LEFT" | "RIGHT" | "DOWN" | "CENTER" | "A" | "B" | ""
    """
    time.sleep(0.05)
    while 1:
        if not GPIO.input(U_pin):
            return "UP"
        if not GPIO.input(L_pin):
            time.sleep(0.2)
            return "LEFT"
        if not GPIO.input(R_pin):
            return "RIGHT"
        if not GPIO.input(D_pin):
            return "DOWN"
        if not GPIO.input(C_pin):
            time.sleep(0.1)
            return "CENTER"
        if not GPIO.input(A_pin):
            # Return Key
            time.sleep(0.2)
            return "A"
        if not GPIO.input(B_pin):
            # Enter Key
            time.sleep(0.1)
            return "B"


def checkKeyInterrupt():
    """
    Non-Blocking get key
    :return: "UP" | "LEFT" | "RIGHT" | "DOWN" | "CENTER" | "A" | "B" | ""
    """
    # time.sleep(0.05)
    if not GPIO.input(U_pin):
        return "UP"
    if not GPIO.input(L_pin):
        time.sleep(0.2)
        return "LEFT"
    if not GPIO.input(R_pin):
        time.sleep(0.1)
        return "RIGHT"
    if not GPIO.input(D_pin):
        return "DOWN"
    if not GPIO.input(C_pin):
        time.sleep(0.1)
        return "CENTER"
    if not GPIO.input(A_pin):
        # Return Key
        time.sleep(0.2)
        return "A"
    if not GPIO.input(B_pin):
        # Enter Key
        return "B"
    else:
        return ""


def getAnyKeyEvent():
    """
    Blocking
    If any key are pressed, returns True
    :return: True
    """
    if getKeyStroke() != "":
        return True
