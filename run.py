import time
# import cv2
import numpy as np
from PIL import Image, ImageDraw

import Menu_Page_Router
from FileBrowser import renderFolders

from GPIO_Init import getKeyStroke, displayImage, getFont
from OP_1_Connection import start_OP_1_Connection, is_connected, currentStorageStatus
from config import config, savePaths

__author__ = "Hsuan Han Lai (Edward Lai)"
__date__ = "2019-04-02"


def displayLine(line, indent):
    return indent, line * 10

def start():
    image = Image.open("Assets/Img/OP_1Connect_64.png").convert("1")
    displayImage(image)
    # start_OP_1_Connection()
    connected = Image.new('1', (128, 64))
    draw2 = ImageDraw.Draw(connected)
    draw2.text(displayLine(3, 25), "Connected !", font=getFont(), fill='white')
    displayImage(connected)
    # time.sleep(3)
    currentCursor = 1

    # Get OP1 Connection
    # Initialize Menu System
    pg = Menu_Page_Router.PageRouter()
    # Start First Page
    pg.renderPage(0, currentCursor)

    while 1:
        # if not is_connected():
        #     print("Disconnected")
        #     start()

        key = getKeyStroke()
        if key == "UP":
            if currentCursor - 1 >= 1:
                currentCursor -= 1
            pg.renderPage(0, currentCursor)

        elif key == "DOWN":
            if currentCursor + 1 < pg.getListSize():
                currentCursor += 1
            pg.renderPage(0, currentCursor)

        elif key == "LEFT":
            currentCursor = 1
            pg.renderPage(-1, 1)

        elif key == "RIGHT":
            pg.renderPage(1, currentCursor)
            currentCursor = 1

        elif key == "CENTER":
            pg.renderPage(1, currentCursor)
            currentCursor = 1

        elif key == "B":
            pg.renderPage(1, currentCursor)
            currentCursor = 1

        elif key == "A":
            currentCursor = 1
            pg.renderPage(-1, 1)

        else:
            raise ("Log: Key ", key, "Not recognized")

if __name__ == "__main__":
    start()

