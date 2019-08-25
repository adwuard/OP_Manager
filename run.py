import os
import threading

import Menu_Page_Router
from GPIO_Init import checkKeyInterrupt
from OP_1_Connection import autoMountUnmontThread
from file_util import createImportantFolders

__author__ = "Hsuan Han Lai (Edward Lai)"
__date__ = "2019-04-02"

workDir = os.path.dirname(os.path.realpath(__file__))


def start():
    # create important missing folders
    createImportantFolders()
    threading.Thread(target=autoMountUnmontThread).start()
    currentCursor = 1
    # Initialize Menu System
    pg = Menu_Page_Router.PageRouter()
    # Start First Page
    pg.renderPage(0, currentCursor)

    while 1:
        key = checkKeyInterrupt()

        if key == "UP":
            if currentCursor - 1 >= 1:
                currentCursor -= 1
            pg.renderPage(0, currentCursor)

        elif key == "DOWN":
            if currentCursor + 1 < pg.getListSize():
                currentCursor += 1
            pg.renderPage(0, currentCursor)

        elif key == "LEFT":
            # currentCursor = 1
            currentCursor = pg.renderPage(-1, 1)
            pg.renderPage(0, currentCursor)

        elif key == "RIGHT":
            pg.renderPage(1, currentCursor)
            currentCursor = 1

        elif key == "CENTER":
            pg.renderPage(1, currentCursor)
            currentCursor = 1

        elif key == "B":
            pg.renderPage(1, currentCursor)
            currentCursor = 1
            pass

        elif key == "A":
            currentCursor = pg.renderPage(-1, 1)
            pg.renderPage(0, currentCursor)
            pass


if __name__ == "__main__":
    start()


