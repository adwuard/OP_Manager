import time
import psutil
from PIL import Image, ImageDraw
from GPIO_Init import getFont, displayImage


def findProcessIdByName(processName):
    listOfProcessObjects = []
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
            # Check if process name contains the given name string.
            if processName.lower() in pinfo['name'].lower():
                listOfProcessObjects.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return listOfProcessObjects;


while len(findProcessIdByName("Python")) < 2:
    Display = Image.new('1', (128, 64))
    draw = ImageDraw.Draw(Display)
    draw.rectangle([(0, 0), (128, 10)], 'white')
    draw.text((30, 0), "Boot Screen", font=getFont(), fill='black')
    displayImage(Display)
    time.sleep(1)
