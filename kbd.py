import time
import keyboard
import serial


class kb_Midi:
    def __init__(self):
        self.ser = serial.Serial(port="/dev/serial0", baudrate=38400, timeout=0)

        self.octave = 0
        self.MAX_OCTAVE = 4
        self.MIN_OCTAVE = -4

        self.channel = 1

        self.isPlaying = False

        self.currentOnNotes = []

        self.note_off_channels = list(range(128, 143))
        self.note_on_channels = list(range(144, 159))

        self.keyMap = {
            # C4 - C5
            "z": ("C", 60),
            "s": ("C#", 61),
            "x": ("D", 62),
            "d": ("D#", 63),
            "c": ("E", 64),
            "v": ("F", 65),
            "g": ("F#", 66),
            "b": ("G", 67),
            "h": ("G#", 68),
            "n": ("A", 69),
            "j": ("A#", 70),
            "m": ("B", 71),

            # C5
            ",": ("C", 72),
            "l": ("C#", 73),
            ".": ("D", 74),
            ";": ("D#", 75),
            "/": ("E", 76),

            # C5 - C6
            "q": ("C", 72),
            "2": ("C#", 73),
            "w": ("D", 74),
            "3": ("D#", 75),
            "e": ("E", 76),
            "r": ("F", 77),
            "5": ("F#", 78),
            "t": ("G", 79),
            "6": ("G#", 80),
            "y": ("A", 81),
            "7": ("A#", 82),
            "u": ("B", 83),

            # C6
            "i": ("C", 84),
            "9": ("C#", 85),
            "o": ("D", 86),
            "0": ("D#", 87),
            "p": ("E", 88)

            # others keys to assign actions
            # "1": ("C", 84),
            # "4": ("C#", 85),
            # "8": ("D", 86),
            # "-": ("D#", 87),
            # "=": ("E", 88)
            # ........
        }

    def octave_up(self):
        if self.octave + 1 <= self.MAX_OCTAVE:
            self.octave += 1
        print("Octave UP", "Current Octave: ", self.octave)

    def octave_down(self):
        if self.octave - 1 >= self.MIN_OCTAVE:
            self.octave -= 1
        print("Octave DOWN", "Current Octave: ", self.octave)

    def toggle_play_pause(self):
        if not self.isPlaying:
            self.isPlaying = True
            print("Play")
        else:
            self.isPlaying = False
            print("Pause")

    def hook(self, key):
        action = key.event_type
        keyname = key.name
        # Pressed
        if action == "down":
            if keyname not in self.currentOnNotes:
                self.currentOnNotes.append(keyname)
                if keyname in self.keyMap:
                    oct_change = self.octave * 8
                    note, note_val = self.keyMap[keyname]

                    midiMesg = [self.note_on_channels[self.channel - 1], note_val + oct_change, 64]
                    print(midiMesg)
                    self.ser.write(midiMesg)

                if keyname == "esc":
                    self.toggle_play_pause()
                elif keyname == "up":
                    self.octave_up()
                elif keyname == "down":
                    self.octave_down()
                elif keyname in ["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12"]:
                    self.channel = keyname[1:]
                    print ("Set Channel", self.channel)
                else:
                    print(keyname)

        # Release
        if action == "up":
            if keyname in self.currentOnNotes:
                self.currentOnNotes.remove(keyname)
            if keyname in self.keyMap:
                oct_change = self.octave * 8
                note, note_val = self.keyMap[keyname]

                midiMesg= [self.note_off_channels[self.channel - 1], note_val + oct_change, 0]
                print (midiMesg)
                self.ser.write(midiMesg)

    def start(self):
        # Start keyboard listening threads
        keyboard.hook(self.hook, suppress=True)


print("Start")
kb = kb_Midi()
while kb.start() is None:
    time.sleep(1)
