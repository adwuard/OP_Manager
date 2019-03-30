from PIL import ImageFont

from OP_1_Connect import OP_1_Connect
from config import config
from display import displayLine


Menu = [["OP-1 File Manager"],
        ["Projects",
         ["Upload Project", ["Upload", [["file1.aif", "Path to the File"], "file2.aif"]]],
         ["Backup Project", []],
         ],

        ["Patches",
         ["Upload Patches"]],
        ["Preset Packs"],
        ["Check OP-1 Storage"],
        ["Eject OP-1"]]


MainPage = {
    "OP-1 File Manager": -1,
    "Projects": 1,
    "Patches": 2,
    "Preset Packs": 3,
    "Check OP-1 Storage": 4,
    "Eject OP-1": 5
}

checkStoragePage = {
    "OP-1 Storage": "-1",
    "Synth": "-1",
    "Sampler": "-1",
    "Drum": "-1"
}

ProjectsPage = {
    "Backup OP-1 Project": "act_3",
    "Load Project": "act_4"
}

ejectPage = {

}

filePathInstance = {
    "FileName": "Full File Path"
}

pageLookUp = {
    4: checkStoragePage,
    5: ejectPage
}


class pageRouter:
    pageQue = [0]
    currentPageDist = MainPage

    def renderPage(self, draw, dict, cur, displayAttribute):
        iterCount = 0
        font = ImageFont.truetype("FreeMonoBold.ttf", 12)
        len(dict)
        # Algo For Scrolling
        for item in Menu:
            for i in item:
                if iterCount == 0:
                    draw.rectangle([(0, 0), (128, 10)], 'white')
                    draw.text(displayLine(iterCount, 2), i, fill='black', font=font)
                else:
                    if cur == -1:
                        if displayAttribute:
                            draw.text(displayLine(iterCount, 2), i + " " + dict[item], fill='white')
                        else:
                            draw.text(displayLine(iterCount, 2), i, fill='white')
                    else:
                        draw.text(displayLine(iterCount, 10), i, fill='white')
            iterCount += 1

        if cur != -1:
            if cur > len(dict):
                cur -= 1
            draw.text(displayLine(cur, 2), "v", fill='white')

    # Routes
    # -1 Previous Page
    # 0 Main Page
    # 1 Project Page
    # 2 Patches
    # 3 Preset
    # 4 Check OP-1 Storage
    # 5 Eject

    # ActionCode
    # act1

    def menuPageRouter(self, draw, routes, cur):
        # print(self.pageQue[])
        if len(self.pageQue) > 0:
            currentPage = self.pageQue[-1]
        else:
            currentPage = self.pageQue[0]

        # self.pageQue.append(routes)

        if routes == -1:
            if len(self.pageQue) > 1:
                print(self.pageQue)
                self.pageQue = self.pageQue[:-1]
                # self.currentPageDist =
                self.menuPageRouter(draw, self.pageQue[-1], cur)

        if currentPage == 0:
            self.renderPage(draw, MainPage, cur, False)
            # return MainPageMenu


        if currentPage == 4:
            connect = OP_1_Connect()
            checkStoragePage["Synth"] = str(len(connect.importOP1SynthDir()[1])) + "/" + str(
                config["Max_Synth_Synthesis_patches"])
            checkStoragePage["Sampler"] = str(len(connect.importOP1SynthDir()[0])) + "/" + str(
                config["Max_Synth_Sampler_patches"])
            checkStoragePage["Drum"] = str(len(connect.importOP1drumDir()[2])) + "/" + str(config["Max_Drum_Patches"])
            self.renderPage(draw, checkStoragePage, -1, True)

        if currentPage == "act1":
            return 23



    def performAction(self, curser):
        self.pageQue.append(self.currentPageDist[curser])

        # Add new page to the page queue


        # page = pageLookUp[curser]
        # count = 0
        # for i in page:
        #     if count == curser:
        #         self.pageQue.append(page[i])
        #     count += 1
