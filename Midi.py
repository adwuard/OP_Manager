import subprocess
import time

import RPi.GPIO as GPIO

# GPIO.setmode(GPIO.BOARD)
from PIL import Image, ImageDraw

from GPIO_Init import getFont, checkKeyInterrupt, displayImage

GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# import unittest
# import rtmidi

hardware_ports = []


def getConnectedDevices():
    midi_connections = subprocess.check_output(["aconnect", "-l"])
    components = midi_connections.split("client ")
    relevant_connections = components[3:]

    print('Found ' + str(len(relevant_connections)) + ' connected devices')
    print(relevant_connections)
    print('\n')

    global hardware_ports
    hardware_ports = map(lambda c: c.split(":")[0], relevant_connections)


def disconnectAllDevices():
    output = subprocess.call(["aconnect", "-x"])
    print('Disconnecting all devices')


def connectDevices():
    if len(hardware_ports) < 2:
        print('Not enough connected devices\n')
        return

    input_device = hardware_ports[0] + ':0'
    output_device = hardware_ports[1] + ':0'

    print('Connecting device ' + input_device + ' -> ' + output_device)
    subprocess.call(["aconnect", input_device, output_device])

    print('Connecting device ' + output_device + ' -> ' + input_device + '\n')
    subprocess.call(["aconnect", output_device, input_device])


def lookForButtonPress():
    while True:
        try:
            channel = GPIO.wait_for_edge(10, GPIO.RISING, timeout=3000)
            if channel is None:
                print('Timeout occurred')
            else:
                print('Edge detected on channel', channel)
                getConnectedDevices()
                disconnectAllDevices()
                connectDevices()

        except KeyboardInterrupt:
            print("*** Ctrl+C pressed, exiting")
            break


def toHex(Dec):
    return "0x%0.2X" % Dec
    # return '{0:08b}'.format(Dec)

def startMidi():
    import rtmidi_python as rtmidi
    midi_in = rtmidi.MidiIn()
    available_ports_in = midi_in.ports
    print(available_ports_in)

    midi_in.open_port(1)
    image = Image.new('1', (128, 64))
    draw = ImageDraw.Draw(image)
    displayImage(image)

    import serial
    ser = serial.Serial('/dev/ttyAMA0', baudrate=38400)
    while True:
        message, delta_time = midi_in.get_message()
        if message and message != [248]:
            print(message)

            # for i in message:
            #     print(hex(i))
            print(toHex(message[0])+" "+str(message[1])+" "+str(message[2]))
            ser.write(toHex(message[0])+" "+str(message[1])+" "+str(message[2]))

        # draw.rectangle([(0, 0), (128, 64)], fill="black")
        # draw.text((50, 13), str(message), font=getFont(), fill="white")  # Disk Storage Render
        # displayImage(image)


def usbMIDIOut():
    # import rtmidi_python as rtmidi
    # midiout = rtmidi.MidiOut()
    # available_ports = midiout.ports
    # print(available_ports)
    # if available_ports:
    #     midiout.open_port(1)
    # If you want to read MIDI message

    import serial
    ser = serial.Serial('/dev/ttyAMA0', baudrate=38400)
    # note_on = [0x90, 60, 112]  # channel 1, middle C, velocity 112
    # note_off = [0x80, 60, 0]
    print("In Midi")
    while True:

        print(ser.read())
        # midiout.send_message(note_on)
        # time.sleep(0.5)
        # midiout.send_message(note_off)
