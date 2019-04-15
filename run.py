import os
from PIL import Image, ImageDraw
import Menu_Page_Router
from GPIO_Init import getKeyStroke, displayImage, getFont

__author__ = "Hsuan Han Lai (Edward Lai)"
__date__ = "2019-04-02"

workDir = os.path.dirname(os.path.realpath(__file__))


def start():
    currentCursor = 1
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
            pass
        elif key == "A":
            pass

        else:
            raise ("Log: Key ", key, "Not recognized")


if __name__ == "__main__":
    # from multiprocessing import Process
    # server = Process(target=app.run)
    # server.start()
    start()
    # server.terminate()
    # server.join()

    # while True:
    #     print("\nStarting " + filename)
    #     p = Popen("python " + filename, shell=True)
    # p.wait()
