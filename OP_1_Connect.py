import os
from config import config


class OP_1_Connect:
    def __init__(self):
        connection_Status = "False"
        OP1_Synth_Patch_Count = 0
        OP1_Sample_Patch_Count = 0
        OP1_Drum_Patch_Count = 0

    def findStrInAif(self, lookingfor, pathToTargetFile):
        with open(pathToTargetFile, 'rb') as reader:
            if lookingfor in str(reader.read()):
                return True
            else:
                return False

    def list_files(self, startpath):
        sampleEngine = []
        synthEngine = []
        others = []
        for root, dirs, files in os.walk(startpath):
            for f in files:
                currentFilePath = str(root) + "/" + f
                if f.endswith('.aif') and not f.startswith(".") and "synth" in root:
                    if self.findStrInAif("\"type\":\"digital\"", currentFilePath):
                        sampleEngine.append(currentFilePath)
                    else:
                        synthEngine.append(currentFilePath)

                elif f.endswith('.aif') and not f.startswith("."):
                    others.append(currentFilePath)

        # print(len(sampleEngine))
        # print(len(filePaths))
        return [sampleEngine, synthEngine, others]

    # "type":"sampler"
    # "type":"digital"

    def importOP1SynthDir(self):
        return self.list_files(config["OP_1_System_Path"] + "synth")

    def importOP1AlbumDir(self):
        return self.list_files(config["OP_1_System_Path"] + "album")

    def importOP1drumDir(self):
        return self.list_files(config["OP_1_System_Path"] + "drum")

    def importOP1tapeDir(self):
        return self.list_files(config["OP_1_System_Path"] + "tape")

    def importOP1Dirs(self):
        print("Synth, Sampler: ", len(self.importOP1SynthDir()[1]), ",", len(self.importOP1SynthDir()[0]), "/",
              str(config["Max_Synth_Synthesis_patches"] + config["Max_Synth_Sampler_patches"]))
        print("Drum: ", len(self.importOP1drumDir()[2]), "/", str(config["Max_Drum_Patches"]))
        print("Tapes: ", len(self.importOP1tapeDir()[2]), "/", 4)
        print("Album: ", len(self.importOP1AlbumDir()[2]))

    def copyfileobj(self, fsrc, fdst, callback, length=16 * 1024):
        copied = 0
        while True:
            buf = fsrc.read(length)
            if not buf:
                break
            fdst.write(buf)
            copied += len(buf)
            callback(copied)


temp = OP_1_Connect()
temp.importOP1Dirs()
