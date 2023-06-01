from json import loads
from requests import get
from re import sub
from os.path import exists
from CLI.Utility import Clamp
from threading import Thread

class CivitaiTab:
    parentWindow = None
    thisTab = None

    maxPage = 0
    wantedPrompts = ["beautiful", "female", "breasts", "woman", "girl", "masterpiece"]
    unwantedPrompts = ["obese", "fat", "ugly", "weird", "creepy", "loli", "old woman", "old", "child", "creature", "kid"]

    enhanceFrame = None
    positiveFilenameEntry = None
    negativeFilenameEntry = None
    imageLimitEntry = None
    pageNumberStartEntry = None
    pageNumberEndEntry = None
    sortVariable = None
    periodVariable = None
    nsfwVariable = None

    def __init__(self, parent, tab):
        from customtkinter import StringVar, CTkFrame, CTkButton, CTkLabel, CTkEntry, CTkComboBox

        self.parentWindow = parent
        self.thisTab = tab

        url = f"https://civitai.com/api/v1/images?limit=1"
        header = {"content-type":"application.json"}
        jsonFile = loads(get(url, headers=header).text)
        self.maxPage = int(jsonFile['metadata']['totalPages'])

        if exists("dataset/wantedPrompts.txt") is False:
            file = open("dataset/wantedPrompts.txt", "w")
            file.write(", ".join(self.wantedPrompts))
            file.close()

        if exists("dataset/unwantedPrompts.txt") is False:
            file = open("dataset/unwantedPrompts.txt", "w")
            file.write(", ".join(self.unwantedPrompts))
            file.close()

        self.enhanceFrame = CTkFrame(self.thisTab)

        positiveFilenameLabel = CTkLabel(self.enhanceFrame, text="Positive Filename")
        self.positiveFilenameEntry = CTkEntry(self.enhanceFrame)

        positiveFilenameLabel.grid(column=0, row=0, padx=(0, 50), ipady=5, pady=10)
        self.positiveFilenameEntry.grid(column=1, row=0)

        negativeFilenameLabel = CTkLabel(self.enhanceFrame, text="Negative Filename")
        self.negativeFilenameEntry = CTkEntry(self.enhanceFrame)

        negativeFilenameLabel.grid(column=0, row=1, padx=(0, 50), ipady=5, pady=10)
        self.negativeFilenameEntry.grid(column=1, row=1)

        imageLimitLabel = CTkLabel(self.enhanceFrame, text="Image Per Page [1, 200]")
        self.imageLimitEntry = CTkEntry(self.enhanceFrame)

        imageLimitLabel.grid(column=0, row=2, padx=(0, 50), ipady=5, pady=10)
        self.imageLimitEntry.grid(column=1, row=2)

        pageNumberStartLabel = CTkLabel(self.enhanceFrame, text=f"Page Number To Start [1, {self.maxPage - 1}]")
        self.pageNumberStartEntry = CTkEntry(self.enhanceFrame)

        pageNumberStartLabel.grid(column=0, row=3, padx=(0, 50), ipady=5, pady=10)
        self.pageNumberStartEntry.grid(column=1, row=3)

        pageNumberEndLabel = CTkLabel(self.enhanceFrame, text=f"Page Number To End [1, {self.maxPage}]")
        self.pageNumberEndEntry = CTkEntry(self.enhanceFrame)

        pageNumberEndLabel.grid(column=0, row=4, padx=(0, 50), ipady=5, pady=10)
        self.pageNumberEndEntry.grid(column=1, row=4)
        
        sortLabel = CTkLabel(self.enhanceFrame, text="Sort")
        self.sortVariable = StringVar(value="Most Reactions")
        sortCheckbox = CTkComboBox(
            self.enhanceFrame,
            variable= self.sortVariable,
            state='readonly',
            width=160,
            values=[
                'Most Reactions',
                'Most Comments',
                'Newest'
            ]
        )

        sortLabel.grid(column=0, row=5, padx=(0, 50), ipady=5, pady=10)
        sortCheckbox.grid(column=1, row=5)

        periodLabel = CTkLabel(self.enhanceFrame, text="Period")
        self.periodVariable = StringVar(value="All Time")
        periodCheckbox = CTkComboBox(
            self.enhanceFrame,
            variable=self.periodVariable,
            state='readonly',
            values=[
                'All Time',
                'Year',
                'Month',
                'Week',
                'Day'
            ]
        )

        periodLabel.grid(column=0, row=6, padx=(0, 50), ipady=5, pady=10)
        periodCheckbox.grid(column=1, row=6)

        nsfwLabel = CTkLabel(self.enhanceFrame, text="NSFW")
        self.nsfwVariable = StringVar(value="None")
        nsfwCheckbox = CTkComboBox(
            self.enhanceFrame,
            variable=self.nsfwVariable,
            state='readonly',
            values=[
                "None",
                "Soft",
                "Mature",
                "X",
                "All"
            ]
        )

        nsfwLabel.grid(column=0, row=7, padx=(0, 50), ipady=5, pady=10)
        nsfwCheckbox.grid(column=1, row=7)

        self.enhanceFrame.pack()

        enhanceButton = CTkButton(
            master=self.thisTab,
            text="Enhance",
            command=self.StartEnhance
        )

        enhanceButton.pack()

    def Refresh(self):
        self.parentWindow.update()
        self.parentWindow.after(1000, self.Refresh)

    def StartEnhance(self):
        self.Refresh()
        Thread(target=self.Enhance).start()

    def GetWantedAndUnwantedPrompts(self):
        positiveFile = open("dataset/wantedPrompts.txt", "r")
        self.wantedPrompts = positiveFile.read().split(",")
        positiveFile.close()

        negativeFile = open("dataset/unwantedPrompts.txt", "r")
        self.unwantedPrompts = negativeFile.read().split(",")
        negativeFile.close()

    def GetUrl(self, imageLimit):
        sort = self.sortVariable.get().replace(" ", "+")
        period = self.periodVariable.get().replace(" ", "")
        nsfw = self.nsfwVariable.get()

        url = ""
        if nsfw == "All":
            url = f"https://civitai.com/api/v1/images?limit={imageLimit}&sort={sort}&period={period}&page="
        else:
            url = f"https://civitai.com/api/v1/images?limit={imageLimit}&sort={sort}&period={period}&nsfw={nsfw}&page="

        return url

    def Enhance(self):
        from tqdm import tqdm
        import gc

        imageLimit = Clamp(int(self.imageLimitEntry.get()), 1, 200)
        pageStart = Clamp(int(self.pageNumberStartEntry.get()), 1, self.maxPage)
        pageEnd = Clamp(int(self.pageNumberEndEntry.get()), pageStart + 1, self.maxPage)

        self.GetWantedAndUnwantedPrompts()
        baseUrl = self.GetUrl(imageLimit)

        positiveFilename = f"dataset/{self.positiveFilenameEntry.get()}.txt"
        negativeFilename = f"dataset/{self.negativeFilenameEntry.get()}.txt"

        positivePrompts = []
        negativePrompts = []

        if exists(positiveFilename) is False:
            file = open(positiveFilename, "w")
            file.close()
        else:
            file = open(positiveFilename, "r")
            positivePrompts = file.readlines()
            file.close()
        
        if exists(negativeFilename) is False:
            file = open(negativeFilename, "w")
            file.close()
        else:
            file = open(negativeFilename, "r")
            negativePrompts = file.readlines()
            file.close()

        header = {"content-type":"application.json"}

        for pageNumber in tqdm(range(pageStart, pageEnd), desc="Getting Data From Pages"):
            url = baseUrl + str(pageNumber)
            try:
                jsonFile = loads(get(url, headers=header).text)
            except:
                continue

            for imageIndex in range(0, imageLimit + 1):
                positive, negative = self.GetPrompts(jsonFile, imageIndex)
                if positive is None: 
                    continue

                positive = self.Preprocess(positive).lower()

                if self.CanAdd(positive) is False:
                    continue
                
                positive += "\n"
                positivePrompts.append(positive)

                if negative is None:
                    continue

                negative = self.Preprocess(negative).lower()

                negative += "\n"
                negativePrompts.append(negative)

            positivePrompts = list(set(positivePrompts))
            negativePrompts = list(set(negativePrompts))
            gc.collect()

        positiveFile = open(positiveFilename, "w")
        positiveFile.writelines(positivePrompts)
        positiveFile.close()

        positivePrompts.clear()

        negativeFile = open(negativeFilename, "w")
        negativeFile.writelines(negativePrompts)
        negativeFile.close()

        negativePrompts.clear()

        gc.collect()

    def GetPrompts(self, jsonFile, imageIndex):
        positivePrompt = None
        negativePrompt = None

        try:
            positivePrompt = jsonFile['items'][imageIndex]['meta']['prompt']
        except:
            positivePrompt = None

        try:
            negativePrompt = jsonFile['items'][imageIndex]['meta']['negativePrompt']
        except:
            negativePrompt = None

        return positivePrompt, negativePrompt

    def CanAdd(self, positivePrompt):
        canAdd = True

        for unwanted in self.unwantedPrompts:
            if unwanted in positivePrompt:
                canAdd = False

        if canAdd is False:
            return canAdd

        canAdd = False

        for wanted in self.wantedPrompts:
            if wanted in positivePrompt:
                canAdd = True

        return canAdd

    def Preprocess(self, line):
        tempLine = line.encode("ascii", "ignore")
        tempLine = tempLine.decode()
        tempLine = tempLine.replace("\n", ", ")
        tempLine = sub(r'<.+?>', '', tempLine)
        tempLine = tempLine.strip()
        tempLine = tempLine.replace("  ", " ")
        tempLine = tempLine.replace("\t", " ")
        tempLine = tempLine.replace(", ,", ", ")
        tempLine = tempLine.replace(",,", ",")
        tempLine = tempLine.replace(",  , ", ", ")
        if tempLine.startswith(" "):
            tempLine = tempLine[1:]
        return tempLine
