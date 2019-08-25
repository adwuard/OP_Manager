import os
import json
from config import config, savePaths, batteryConfig

workDir = os.path.dirname(os.path.realpath(__file__))


def readConfigJsonFile():
    import json
    with open(os.path.join(workDir, "op1funSetup.txt")) as json_file:
        data = json.load(json_file)
        return data


def internetIsOn():
    import requests
    r = requests.get('http://216.58.192.142', stream=True)
    if r.status_code == 200:
        return True
    else:
        return False
    # try:
    #     urllib.urlopen('http://216.58.192.142', timeout=1)
    #     return True
    # except:
    #     return False


def JSONPrettyPrint(jsonstr):
    return json.dumps(jsonstr.json(), sort_keys=True, indent=4)


def unzip(source_filename, dest_dir):
    print (source_filename, dest_dir)
    from zipfile import ZipFile
    zipfile = ZipFile(source_filename)
    zipfile.extractall(dest_dir)


    # with zipfile.ZipFile(source_filename) as zf:
    #     zf.extractall(dest_dir)


class op1funRequests:
    def __init__(self):
        self.userAccount = readConfigJsonFile()

        self.USER_ID = self.userAccount["USER_ID"]
        self.USER_API_TOKEN = self.userAccount["API_TOKEN"]
        self.USER_EMAIL = self.userAccount["USER_EMAIL"]
        print (self.USER_ID, self.USER_ID, self.USER_EMAIL)
        self.localSavePath = savePaths["Local_Patches"]

        # URL Request paths
        self.headers = {'X-User-Token': self.USER_API_TOKEN, 'X-User-Email': self.USER_EMAIL}
        self.PacksURL = "https://api.op1.fun/v1/users/" + self.USER_ID + "/packs"
        self.PatchesURL = "https://api.op1.fun/v1/users/" + self.USER_ID + "/patches"

        self.packLst = []

    def getUserAccount(self):
        return self.USER_ID, self.USER_API_TOKEN, self.USER_EMAIL

    def getPackDownloadURL(self, APILink):
        import requests
        return requests.get(APILink, headers=self.headers).json()["url"]

    def downloadFile(self, url):
        # downloadURL = self.getPackDownloadURL(url)
        # r = requests.get(url, stream=True)
        # print("Download Finished")
        # return io.StringIO(r.content)
        from io import BytesIO
        from urllib.request import urlopen
        resp = urlopen(url)
        return BytesIO(resp.read())

    def unPackageToLocal(self, zipString, destPath):
        unzip(zipString, destPath)

    def getPackList(self):
        import requests
        try:
            print ("User Account:", self.headers)
            import requests
            packsData = requests.get(self.PacksURL, headers=self.headers)

            print (packsData)
            if packsData:
                j = packsData.json()
                # Updates packlist
                self.packLst = []
                for packIndex in range(0, len(j["data"])):
                    packname = j["data"][packIndex]["id"]
                    packdownloadURL = requests.get(j["data"][packIndex]["links"]["download"], headers=self.headers).json()
                    packdownload = j["data"][packIndex]["links"]["download"]
                    packContainPatches = j["data"][packIndex]["relationships"]["patches"]["data"]
                    packsize = len(packContainPatches)
                    name = "[" + str(packsize) + "]" + str(packname)
                    self.packLst.append((name, packdownload))
                return self.packLst
        except requests.exceptions.RequestException as e:
            print(e)
            return []


# op = op1funRequests()
# op.getPackList()
