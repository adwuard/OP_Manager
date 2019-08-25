import multiprocessing
import threading
import os
import time
import serial
import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageOps
from FileBrowser import RenderOptionsMenu
import rtmidi
from GPIO_Init import getFont, displayImage
from UPS_Battery_Module import readCapacity, getBatteryImagePath
from config import batteryConfig

workDir = os.path.dirname(os.path.realpath(__file__))
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


class MidiTool:
    def __init__(self):
        self.stopFlag = False

        self.in_Midi_tool_screen_flag = False
        self.in_out_device_selector_flag = 0  # 0, 1, -1

        # Midi device search filter
        self.sysMidiFilterRemoveLst = ["Midi Through", "RtMidiIn Client", "RtMidiOut Client", "RtMidi", "Through"]
        # self.sysMidiFilterRemoveLst = []
        self.threads = []

        # Current Mounted Device
        self.currentInDevice = "Not Connected"
        self.currentOutDevice = "Not Connected"

        # Serial In out initialization
        # self.serialport = serial.Serial('/dev/serial0', 38400, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)  # /dev/ttyS0, ttyAMA0
        self.ser = serial.Serial(port="/dev/serial0", baudrate=38400, timeout=0)

        # Rtmidi USB Midi Initialization
        self.usbOut = rtmidi.MidiOut()
        self.usbIn = rtmidi.MidiIn()

        self.semitone_MinMax = (-7, 7)
        self.octave_MinMax = (-4, 4)
        self.octave = 0
        self.semiTone = 0

    def read(self):
        """
        Midi Serial Read.(In)
        :return: Midi message
        """
        msg = [None, None, None]
        for i in range(len(msg)):
            raw_byte = self.ser.read()
            if not raw_byte:
                return
            byte_value = ord(raw_byte)
            if byte_value in [248, 250, 252]:
                return byte_value
            else:
                msg[i] = byte_value
        return msg

    def write(self, message):
        """
        Midi Serial write (Out)
        :param message: Midi Message [144, 60, 100]
        :return: N/A
        """
        self.ser.write(message)

    def toHex(self, Dec):
        return "0x%0.2X" % Dec

    def tobin(self, Bin):
        return format(Bin, '08b')

    def _showCurrentConnectedDevice(self):
        if not self.in_Midi_tool_screen_flag:
            image = Image.new('1', (128, 64))
            image.paste(Image.open(workDir + "/Assets/Img/Midi.png").convert("1"))
            draw = ImageDraw.Draw(image)

            if batteryConfig["enable"]:
                # Battery Level in percentage
                # draw.text((105, 0), readCapacity(), fill='black', font=self.smallFont)
                # Battery Level Icon
                icon = Image.open(os.path.join(workDir, getBatteryImagePath(readCapacity()))).convert("L")
                inverted_image = ImageOps.invert(icon)
                image.paste(inverted_image, (117, 0))

            if self.in_out_device_selector_flag == 1:  # Top Device Highlighted
                draw.rectangle(((15, 5), (120, 15)), 'white')
                draw.text((20, 5), str(self._strip_Midi_Name(self.currentInDevice, maxLen=16)), fill='black',
                          font=getFont())
            else:
                draw.text((20, 5), str(self._strip_Midi_Name(self.currentInDevice, maxLen=16)), fill='white',
                          font=getFont())

            if self.in_out_device_selector_flag == -1:  # Bottom Device Highlighted
                draw.rectangle(((15, 50), (120, 60)), 'white')
                draw.text((20, 50), str(self._strip_Midi_Name(self.currentOutDevice, maxLen=16)), fill='black',
                          font=getFont())
            else:
                draw.text((20, 50), str(self._strip_Midi_Name(self.currentOutDevice, maxLen=16)), fill='white',
                          font=getFont())
            displayImage(image)

    def _showParamAdjust(self, title="", message=""):
        self.in_Midi_tool_screen_flag = True
        image = Image.new('1', (128, 64))
        draw = ImageDraw.Draw(image)
        draw.rectangle(((0, 0), (128, 64)), 'black')
        draw.rectangle(((0, 0), (128, 10)), 'white')
        # Title
        draw.text((0, 0), str(title), fill='black', font=getFont())
        if "\n" in message:
            draw.text((30, 20), str(message), fill='white', font=getFont())
        else:
            draw.text((30, 30), str(message), fill='white', font=getFont())
        displayImage(image)
        time.sleep(1)
        self.in_Midi_tool_screen_flag = False

    def pos_neg_toString(self, val):
        if val > 0:
            return " +" + str(val)
        elif val < 0:
            return " " + str(val)
        else:
            return " 0"

    # ======================== Midi tool transpose event ========================
    def _semitone_up(self, channel):
        Min, Max = self.semitone_MinMax
        if self.semiTone + 1 <= Max:
            self.semiTone += 1
        self._showParamAdjust(title="Transpose", message=str("Semitone:" + self.pos_neg_toString(self.semiTone)))
        # self._showCurrentConnectedDevice()

    def _semitone_down(self, channel):
        Min, Max = self.semitone_MinMax
        if self.semiTone - 1 >= Min:
            self.semiTone -= 1
        self._showParamAdjust(title="Transpose", message=str("Semitone:" + self.pos_neg_toString(self.semiTone)))
        # self._showCurrentConnectedDevice()

    def _octave_up(self, channel):
        Min, Max = self.octave_MinMax
        if self.octave + 1 <= Max:
            self.octave += 1
        self._showParamAdjust(title="Transpose", message=str("Octave:" + self.pos_neg_toString(self.octave)))
        # self._showCurrentConnectedDevice()

    def _octave_down(self, channel):
        Min, Max = self.octave_MinMax
        if self.octave - 1 >= Min:
            self.octave -= 1
        self._showParamAdjust(title="Transpose", message=str("Octave" + self.pos_neg_toString(self.octave)))
        # self._showCurrentConnectedDevice()

    def _reset_change(self, channel):
        self.octave = 0
        self.semiTone = 0
        self._showParamAdjust(title="Transpose", message=str(
            "Octave" + self.pos_neg_toString(self.octave) + "\n" + "Semitone" + self.pos_neg_toString(self.semiTone)))
        # self._showCurrentConnectedDevice()

    def upKey(self, channel):
        if not self.in_Midi_tool_screen_flag:
            self.in_out_device_selector_flag = 1

        pass

    def downKay(self, channel):
        if not self.in_Midi_tool_screen_flag:
            self.in_out_device_selector_flag = -1
        pass

    def leftKey(self, channel):
        pass

    def rightKey(self, channel):
        pass

    def centerKey(self, channel):
        self.in_Midi_tool_screen_flag = True
        if self.in_out_device_selector_flag == 1:
            select = RenderOptionsMenu(self._filterMidiDevice(self.usbIn.get_ports()), title="Midi In Devices")
            if select != "RETURN":
                self.terminateThread(self.currentInDevice, "MidiIn")
                self.mountMidiDevice(assignIn=select)
                self.currentInDevice = select


        elif self.in_out_device_selector_flag == -1:
            print("Midi Out Select")
            select = RenderOptionsMenu(self._filterMidiDevice(self.usbOut.get_ports()), title="Midi Out Devices")
            if select != "RETURN":
                self.terminateThread(self.currentOutDevice, "MidiOut")
                self.mountMidiDevice(assignOut=select)
                self.currentOutDevice = select

        print(self.threads)
        self.in_Midi_tool_screen_flag = False

    def aKey(self, channel):
        pass

    def bKey(self, channel):
        pass

    def terminateThread(self, deviceName, port):
        """
        :param deviceName: Name of the device
        :param port: "MidiIn", "MidiOut"
        :return:
        """
        # for i in self.threads:
        #     IO, name, thread = i
        #     print(IO, port, name, deviceName)
        #     if IO == port and deviceName == name:
        #         self.threads.remove(i)
        self.threads = []

    def stopInterruptCallBack(self, channel):
        print('Stop Midi')
        self.stopFlag = True

    def gpiocleanup(self):
        pins = [27, 23, 4, 17, 22, 5, 6]  # [L, R, C, U, D, A, B]
        for i in pins:
            GPIO.remove_event_detect(i)

    def startKeyEvent(self):
        print('Start Key Event Catcher')
        # Add return key to interrupt callback
        pins = [27, 23, 4, 17, 22, 5, 6]  # [L, R, C, U, D, A, B]
        # Add each to to key detect
        for i in pins:
            GPIO.add_event_detect(i, GPIO.RISING)

        # GPIO.add_event_callback(27, callback=self._semitone_down)
        # GPIO.add_event_callback(23, callback=self._semitone_up)
        # GPIO.add_event_callback(4, callback=self._reset_change)
        # GPIO.add_event_callback(17, callback=self._octave_up)
        # GPIO.add_event_callback(22, callback=self._octave_down)
        GPIO.add_event_callback(5, callback=self.stopInterruptCallBack)
        # GPIO.add_event_callback(6, callback=self.stopInterruptCallBack)

        # GPIO.add_event_callback(27, callback=self.leftKey)
        # GPIO.add_event_callback(23, callback=self.rightKey)
        # GPIO.add_event_callback(4, callback=self.centerKey)
        # GPIO.add_event_callback(17, callback=self.upKey)
        # GPIO.add_event_callback(22, callback=self.downKay)
        # GPIO.add_event_callback(5, callback=self.aKey)
        # GPIO.add_event_callback(6, callback=self.bKey)

    def getSerialMIDIByteStream(self):
        while 1:
            if self.currentInDevice == "Not Connected":
                print("Terminated getSerial")
                self.terminateThread(self.currentOutDevice, "MidiIn")
                print(self.threads)
                return
            # mesg = self.read()
            mesg = self.ser.read()
            if mesg:
                mesg = ord(mesg)
                # print("From Deluge:  ", mesg)
                # if isinstance(mesg, list):
                #     self.usbOut.send_message(mesg)
                # else:
                self.usbOut.send_message([mesg])

    def getUSBMidi(self):
        while 1:
            mesg = None
            while mesg == None:
                if self.currentOutDevice== "Not Connected":
                    print("Terminated getUSB")
                    self.terminateThread(self.currentOutDevice, "MidiOut")
                    print(self.threads)
                    return
                else:
                    mesg = self.usbIn.get_message()

            message, _ = mesg
            print("From USB:  ", message)

            if len(message) == 1:
                self.ser.write(message)
            else:
                self.ser.write(message)

    def _filterMidiDevice(self, lst):
        filteredLst = []
        flag = True
        for j in lst:
            for i in self.sysMidiFilterRemoveLst:
                if i in j:
                    flag = False
            if flag:
                filteredLst.append(j)
            else:
                flag = True
            print ("Filtered:", filteredLst)
        return filteredLst

    def _availOutPortCheck(self):
        lst = self._filterMidiDevice(self.usbOut.get_ports())
        # while not lst:
        #     lst = self._filterMidiDevice(self.usbOut.get_ports())
        return lst

    def _availInPortCheck(self):
        lst = self._filterMidiDevice(self.usbIn.get_ports())
        # while not lst:
        #     lst = self._filterMidiDevice(self.usbIn.get_ports())
        return lst

    def _get_In_Port_By_Name(self, name):
        """
        Find In Midi ID by Midi Name
        :param name: Name of the MIDI Device
        :return: The index of the Midi List
        """
        for i in range(0, len(self.usbIn.get_ports())):
            if name in self.usbIn.get_ports()[i]:
                return i

    def _get_Out_Port_By_Name(self, name):
        """
        Find Out Midi ID by Midi Name
        :param name: Name of the MIDI Device
        :return: The index of the Midi List
        """
        for i in range(0, len(self.usbOut.get_ports())):
            if name in self.usbOut.get_ports()[i]:
                return i

    def _setInPort(self, item):
        port_ID = self._get_In_Port_By_Name(item)
        self.usbIn.open_port(port_ID)
        self.currentInDevice = item

    def _setOutPort(self, item):
        port_ID = self._get_Out_Port_By_Name(item)
        self.usbOut.open_port(port_ID)
        self.currentOutDevice = item

    def _strip_Midi_Name(self, name, maxLen=16):
        """
        For Display use only.
        Midi Device Name Length over 16 Char will get striped down to 16 Char
        :param name: Full Midi Device Name
        :param maxLen: Allowed length to be displayed
        :return: Shortened Name
        """
        name = name.split(":")[0]
        if len(name) > maxLen:
            return name[:maxLen] + "..."
        else:
            return name

    def mountMidiDevice(self, assignIn=None, assignOut=None):
        if assignIn is not None or assignOut is not None:
            if assignIn is not None:
                self._setInPort(assignIn)
                print("Mounting Device--", " | Device Lst: ", self.usbIn.get_ports(), "| Mounting: ",
                      assignIn)
                USB_In_Stream_Thread = threading.Thread(target=self.getSerialMIDIByteStream)
                USB_In_Stream_Thread.start()
                self.threads.append(["MidiIn", self.currentInDevice, USB_In_Stream_Thread])
            elif assignOut is not None:
                self._setOutPort(assignOut)
                print("Mounting Device--", " | Device Lst: ", self.usbOut.get_ports(), "| Mounting: ",
                      assignOut)
                USB_Out_Stream_Thread = threading.Thread(target=self.getUSBMidi)
                USB_Out_Stream_Thread.start()
                self.threads.append(["MidiOut", self.currentOutDevice, USB_Out_Stream_Thread])
            return
        # Start Wait Device Connection Process
        else:
            In, Out = self._availInPortCheck(), self._availOutPortCheck()
            print(self.usbIn.get_ports())
            print(self.usbOut.get_ports())
            if In != None and Out != None:
                image = Image.new('1', (128, 64))
                image.paste(Image.open(workDir + "/Assets/Img/Midi.png").convert("1"))
                draw = ImageDraw.Draw(image)
                # Mount first USB Midi in device that's available
                if In:
                    self._setInPort(In[0])
                    draw.text((20, 5), str(self._strip_Midi_Name(self.currentInDevice, maxLen=16)), fill='white',
                              font=getFont())

                    # In Device Mounted---start Midi thread
                    USB_In_Stream_Thread = threading.Thread(name=self.currentInDevice, target=self.getSerialMIDIByteStream)
                    USB_In_Stream_Thread.start()
                    self.threads.append(["MidiIn", self.currentInDevice, USB_In_Stream_Thread])


                else:
                    draw.text((20, 5), str(self.currentInDevice), fill='white', font=getFont())
                # Mount first Midi out device that's available
                if Out:
                    self._setOutPort(Out[0])
                    draw.text((20, 50), str(self._strip_Midi_Name(self.currentOutDevice, maxLen=16)), fill='white',
                              font=getFont())

                    # Out Device Mounted---start Midi thread
                    USB_Out_Stream_Thread = threading.Thread(name=self.currentOutDevice, target=self.getUSBMidi)
                    USB_Out_Stream_Thread.start()
                    self.threads.append(["MidiOut", self.currentOutDevice, USB_Out_Stream_Thread])


                else:
                    draw.text((20, 50), str(self.currentInDevice), fill='white', font=getFont())
                print(self.threads)
                displayImage(image)

    def usbMIDIOut(self):
        # Ensure the connection with the usb device.
        self._showCurrentConnectedDevice()
        self.startKeyEvent()
        # self.mountMidiDevice()
        while 1:
            if self.stopFlag:
                self.usbOut.close_port()
                self.usbIn.close_port()
                self.currentOutDevice = "Not Connected"
                self.currentInDevice = "Not Connected"
                self.gpiocleanup()
                return

            I, O = self.usbIn.get_ports(), self.usbOut.get_ports()
            if self.currentOutDevice not in O or self.currentInDevice not in I:
                if self.currentOutDevice not in O:
                    self.currentOutDevice = "Not Connected"
                    self.usbOut.close_port()
                if self.currentInDevice not in I:
                    self.currentInDevice = "Not Connected"
                    self.usbIn.close_port()
                self._showCurrentConnectedDevice()
                mount = self.mountMidiDevice()

            self._showCurrentConnectedDevice()
