import os
from PIL import Image, ImageDraw
import Menu_Page_Router
from GPIO_Init import getKeyStroke, displayImage, getFont

__author__ = "Hsuan Han Lai (Edward Lai)"
__date__ = "2019-04-02"

workDir = os.path.dirname(os.path.realpath(__file__))


def start():
    image = Image.open(workDir + "/Assets/Img/OP_1Connect_64.png").convert("1")
    displayImage(image)
    # start_OP_1_Connection()
    connected = Image.new('1', (128, 64))
    draw = ImageDraw.Draw(connected)
    draw.text((30, 25), "Connected !", font=getFont(), fill='white')
    displayImage(connected)
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
            # pg.renderPage(1, currentCursor)
            # currentCursor = 1
            pass
        elif key == "A":
            # currentCursor = 1
            # pg.renderPage(-1, 1)
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

