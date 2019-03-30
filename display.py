# File: animated-hello-world.py
import time

from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import displayPages

'''
# Import Luma.OLED libraries
from luma.core.interface.serial import spi
from luma.oled.device import ssd1331
# Configure the serial port
serial = spi(device=0, port=0)
device = ssd1331(serial)
'''


def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)


def displayLine(line, indent):
    return indent, line * 10


def main():
    frameSize = (128, 64)
    time.sleep(0.1)
    currentCursor = 1
    pg = displayPages.pageRouter()
    while 1:
        image = Image.new('RGB', (frameSize), 'white')
        font = ImageFont.truetype("FreeMonoBold.ttf", 12)
        # menuItmes = ImageFont.truetype("FreeMonoBold.ttf", 10)
        draw = ImageDraw.Draw(image)
        draw.rectangle([(0, 0), (128, 64)], 'black', 'white')

        pg.menuPageRouter(draw, 1, currentCursor)

        # draw.rectangle([(0, 0), (128, 10)], 'white')
        # draw.text(displayLine(currentCursor, 2), "v", fill='white')
        # draw.text(displayLine(0, 0), "OP-1 File Manager", fill='black', font=font)
        # draw.text(displayLine(1, 10), "Projects", fill='white')
        # draw.text(displayLine(2, 10), "Patches", fill='white')
        # draw.text(displayLine(3, 10), "Preset Packs", fill='white')
        # draw.text(displayLine(4, 10), "Check OP-1 Storage", fill='white')
        # draw.text(displayLine(5, 10), "Eject", fill='white')

        '''
        # Output to OLED display
        device.display(image)
        '''

        # Virtual display
        npImage = np.asarray(image)
        frameBGR = cv2.cvtColor(npImage, cv2.COLOR_RGB2BGR)
        newFrame = rescale_frame(frameBGR, percent=300)
        cv2.imshow('Test', newFrame)

        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
        elif k == 39:
             pg.performAction(currentCursor)

        elif k == 47:
            print("Up")
            # renderCursor(draw, currentCursor, currentCursor + 1);
            if currentCursor + 1 <= 5:
                currentCursor += 1

        elif k == 59:
            print("Right")
            currentCursor = 1
            pg.menuPageRouter(draw, -1, currentCursor)

        elif k == 91:
            print("Down")
            if currentCursor - 1 >= 1:
                currentCursor -= 1


        elif k == 97:
            print(" Select/Send/Confirm")
        elif k == 115:
            print("Back/Cancel")

    # Virtual display
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
