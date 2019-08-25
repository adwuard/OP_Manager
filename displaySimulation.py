import time

import cv2
import numpy as np
from tkinter import *
# pip install pillow
from PIL import Image, ImageTk, ImageEnhance

# Display size
displaySize = (128, 64)
zoom = 3


def rescale(img):
    size = img.size
    print(size)
    size = (displaySize[0] * zoom, displaySize[1] * zoom)
    img = img.resize(size, Image.ANTIALIAS)
    enhancer = ImageEnhance.Sharpness(img)
    enhanced_im = enhancer.enhance(5.0)
    return enhanced_im


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)
        load = Image.open("Assets/Img/BackupProject.png")
        load = rescale(load)
        rescale(load)
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)


# File: animated-hello-world-pi.py
import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

'''
# Virtual display
import cv2
import numpy as np
'''
# Import Luma.OLED libraries
similated = True

if not similated:
    from luma.core.interface.serial import spi
    from luma.oled.device import ssd1331

    # Configure the serial port
    serial = spi(device=0, port=0)
    device = ssd1331(serial)

globalimg = ""


def display():

    font = ImageFont.truetype("FreeMonoBold.ttf", 12)
    # draw = ImageDraw.Draw(image)

    # image2 = Image.new('RGB', (128, 64), 'white')
    # load = Image.open("Assets/Img/BackupProject.png")
    pathToImage = "Assets/Img/BackupProject.png"

    # image = Image.new('RGB', (1000, 1000), 'white')
    load = Image.new('RGB', (128, 64))
    load.paste(Image.open(pathToImage).convert("1"))
    load = rescale(load)
    # image.paste(load, (10, 10))

    # Output to OLED display
    # device.display(image)

    # Virtual display
    frameBGR = cv2.cvtColor(np.asarray(load), cv2.COLOR_RGB2BGR)
    blank_image = np.zeros(((64*zoom)+100, (128*zoom)+100, 3), np.uint8)
    blank_image[10:10 + (64*zoom), 10:10 + (128*zoom)] = frameBGR

    # blank_image[:, 0:786 // 2] = (255, 0, 0)

    # cv2.namedWindow("output", cv2.WINDOW_NORMAL)  # Create window with freedom of dimensions
    # imS = cv2.resize(blank_image, (200, 200))  # Resize image
    cv2.imshow("RSPI-MIDI", blank_image)

    k = cv2.waitKey(1) & 0xFF
    time.sleep(100)


def main():
    frameSize = (1024, 768)
    timeCheck = time.time()
    time.sleep(0.1)
    while 1:
        image = Image.new('RGB', frameSize, 'white')
        font = ImageFont.truetype("FreeMonoBold.ttf", 12)
        draw = ImageDraw.Draw(image)
        time.sleep(0.01)
        fps = "FPS: {0:0.3f}".format(1 / (time.time() - timeCheck))
        timeCheck = time.time()
        draw.text((2, 0), fps, fill='white')

        # image2 = Image.new('RGB', (128, 64), 'white')
        load = Image.open("Assets/Img/BackupProject.png")
        draw2 = ImageDraw.Draw(load)
        draw2.rectangle([(0, 0), (128, 64)], 'black', 'white')
        draw2.text((0, 0), 'Hello World', fill="black", font=font)
        image2 = rescale(load)
        image.paste(image2, (100, 100))

        # Output to OLED display
        # device.display(image)

        # Virtual display
        npImage = np.asarray(image)
        frameBGR = cv2.cvtColor(npImage, cv2.COLOR_RGB2BGR)

        cv2.imshow('Test', frameBGR)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

        '''
        # Virtual display
        npImage = np.asarray(image)
        frameBGR = cv2.cvtColor(npImage, cv2.COLOR_RGB2BGR)
        cv2.imshow('Test', frameBGR)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
        '''

    # Virtual display
    # cv2.destroyAllWindows()


if __name__ == "__main__":
    display()

# COUNTER = 0
# while 1:
#     COUNTER += 1
#     print(COUNTER)
#     root = Tk()
#     app = Window(root)
#     root.wm_title("Rspi-Midi")
#     root.geometry("1024x768")
#     root.mainloop()
#     time.sleep(1)
#
