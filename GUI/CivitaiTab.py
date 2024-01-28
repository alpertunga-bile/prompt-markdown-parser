from json import loads
from requests import get
from re import sub
from os.path import exists, join
from Utility import Clamp, GetPromptSets, CheckIfContainsWord, AddNewlineToList
from threading import Thread
from datetime import datetime


class CivitaiTab:
    parentWindow = None
    thisTab = None

    wantedPromptsFile = join("dataset", "wantedPrompts.txt")
    unwantedPromptsFile = join("dataset", "unwantedPrompts.txt")

    wantedPrompts = ["beautiful", "female", "breasts", "woman", "girl", "masterpiece"]
    unwantedPrompts = [
        "obese",
        "fat",
        "ugly",
        "weird",
        "creepy",
        "loli",
        "old woman",
        "old",
        "child",
        "creature",
        "kid",
    ]

    enhanceFrame = None

    positiveFilenameEntry = None
    negativeFilenameEntry = None
    imageLimitEntry = None
    imageCursorStartEntry = None
    hourEndEntry = None
    minuteEndEntry = None

    enhanceInfoLabel = None

    sortVariable = None
    periodVariable = None
    nsfwVariable = None

    def __init__(self, parent, tab):
        from customtkinter import (
            StringVar,
            CTkFrame,
            CTkButton,
            CTkLabel,
            CTkEntry,
            CTkComboBox,
        )

        self.parentWindow = parent
        self.thisTab = tab

        if exists(self.wantedPromptsFile) is False:
            with open(self.wantedPromptsFile, "w") as wanted_file:
                wanted_file.write(", ".join(self.wantedPrompts))

        if exists(self.unwantedPromptsFile) is False:
            with open(self.unwantedPromptsFile, "w") as unwanted_file:
                unwanted_file.write(", ".join(self.unwantedPrompts))

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

        imageCursorStartLabel = CTkLabel(
            self.enhanceFrame, text="Image Cursor To Start"
        )
        self.imageCursorStartEntry = CTkEntry(self.enhanceFrame)

        imageCursorStartLabel.grid(column=0, row=3, padx=(0, 50), ipady=5, pady=10)
        self.imageCursorStartEntry.grid(column=1, row=3)

        hourEndLabel = CTkLabel(self.enhanceFrame, text="Ending Hour [0, 24]")
        self.hourEndEntry = CTkEntry(self.enhanceFrame)

        hourEndLabel.grid(column=0, row=4, padx=(0, 50), ipady=5, pady=10)
        self.hourEndEntry.grid(column=1, row=4)

        minuteEndLabel = CTkLabel(self.enhanceFrame, text="Ending Minute [0, 60]")
        self.minuteEndEntry = CTkEntry(self.enhanceFrame)

        minuteEndLabel.grid(column=0, row=5, padx=(0, 50), ipady=5, pady=10)
        self.minuteEndEntry.grid(column=1, row=5)

        sortLabel = CTkLabel(self.enhanceFrame, text="Sort")
        self.sortVariable = StringVar(value="Most Reactions")
        sortCheckbox = CTkComboBox(
            self.enhanceFrame,
            variable=self.sortVariable,
            state="readonly",
            width=160,
            values=["Most Reactions", "Most Comments", "Newest"],
        )

        sortLabel.grid(column=0, row=6, padx=(0, 50), ipady=5, pady=10)
        sortCheckbox.grid(column=1, row=6)

        periodLabel = CTkLabel(self.enhanceFrame, text="Period")
        self.periodVariable = StringVar(value="All Time")
        periodCheckbox = CTkComboBox(
            self.enhanceFrame,
            variable=self.periodVariable,
            state="readonly",
            values=["All Time", "Year", "Month", "Week", "Day"],
        )

        periodLabel.grid(column=0, row=7, padx=(0, 50), ipady=5, pady=10)
        periodCheckbox.grid(column=1, row=7)

        nsfwLabel = CTkLabel(self.enhanceFrame, text="NSFW")
        self.nsfwVariable = StringVar(value="None")
        nsfwCheckbox = CTkComboBox(
            self.enhanceFrame,
            variable=self.nsfwVariable,
            state="readonly",
            values=["None", "Soft", "Mature", "X", "All"],
        )

        nsfwLabel.grid(column=0, row=8, padx=(0, 50), ipady=5, pady=10)
        nsfwCheckbox.grid(column=1, row=8)

        self.enhanceFrame.pack()

        self.enhanceInfoLabel = CTkLabel(self.thisTab, text="")
        self.enhanceInfoLabel.pack()

        enhanceButton = CTkButton(
            master=self.thisTab, text="Enhance", command=self.StartEnhance
        )

        enhanceButton.pack()

    def Refresh(self):
        self.parentWindow.update()
        self.parentWindow.after(1000, self.Refresh)

    def StartEnhance(self):
        self.Refresh()
        Thread(target=self.Enhance).start()

    def GetWantedAndUnwantedPrompts(self):
        with open(self.wantedPromptsFile, "r") as positiveFile:
            self.wantedPrompts = positiveFile.read().split(",")

        with open(self.unwantedPromptsFile, "r") as negativeFile:
            self.unwantedPrompts = negativeFile.read().split(",")

    def GetUrl(self, imageLimit):
        sort = self.sortVariable.get().replace(" ", "+")
        period = self.periodVariable.get().replace(" ", "")
        nsfw = self.nsfwVariable.get()

        url = ""
        if nsfw == "All":
            url = f"https://civitai.com/api/v1/images?limit={imageLimit}&sort={sort}&period={period}&cursor="
        else:
            url = f"https://civitai.com/api/v1/images?limit={imageLimit}&sort={sort}&period={period}&nsfw={nsfw}&cursor="

        return url

    def Enhance(self):
        import gc
        from time import sleep

        imageLimit = Clamp(int(self.imageLimitEntry.get()), 1, 200)
        currentCursor = int(self.imageCursorStartEntry.get())

        self.GetWantedAndUnwantedPrompts()
        baseUrl = self.GetUrl(imageLimit)

        positiveFilepath = join("dataset", f"{self.positiveFilenameEntry.get()}.txt")
        negativeFilepath = join("dataset", f"{self.negativeFilenameEntry.get()}.txt")

        positivePrompts, negativePrompts = GetPromptSets(
            positiveFilepath, negativeFilepath
        )

        header = {"content-type": "application.json"}

        hourEnd = Clamp(int(self.hourEndEntry.get()), 0, 23)
        minuteEnd = Clamp(int(self.minuteEndEntry.get()), 0, 59)

        while True:
            currentTime = datetime.now()

            if currentTime.hour == hourEnd and currentTime.minute >= minuteEnd:
                self.enhanceInfoLabel.configure(
                    text=f"Finished at {currentCursor} | Reached to specified time limit"
                )
                break

            url = baseUrl + str(currentCursor)

            try:
                jsonFile = loads(get(url, headers=header).text)
            except:
                self.enhanceInfoLabel.configure(
                    text=f"Can't fetch the json file at {currentCursor}"
                )
                return

            self.enhanceInfoLabel.configure(text=f"Image Cursor : {currentCursor}")

            totalImageSize = len(jsonFile["items"])

            for index in range(totalImageSize):
                positivePrompt, negativePrompt = self.GetPrompts(jsonFile, index)

                if positivePrompt is None:
                    continue

                if self.CanAdd(positivePrompt) is False:
                    continue

                positivePrompts.add(self.Preprocess(positivePrompt))

                if negativePrompt is None:
                    continue

                negativePrompts.add(self.Preprocess(negativePrompt))

            currentCursor = jsonFile["metadata"]["nextCursor"]
            currentCursor = (
                int(currentCursor)
                if currentCursor != None
                else currentCursor + totalImageSize
            )

            sleep(5.0)

        self.WritePromptsFile(positivePrompts, positiveFilepath)
        del positivePrompts

        self.WritePromptsFile(negativePrompts, negativeFilepath)
        del negativePrompts

        gc.collect()

    def WritePromptsFile(self, prompts: set[str], filepath: str) -> None:
        listPrompts = AddNewlineToList(prompts)
        print(f"Saving to {filepath}")

        with open(filepath, "w") as file:
            file.writelines(listPrompts)

    def GetPrompts(self, jsonFile, imageIndex):
        positivePrompt = None
        negativePrompt = None

        try:
            positivePrompt = jsonFile["items"][imageIndex]["meta"]["prompt"]
        except:
            positivePrompt = None

        try:
            negativePrompt = jsonFile["items"][imageIndex]["meta"]["negativePrompt"]
        except:
            negativePrompt = None

        return positivePrompt, negativePrompt

    def CanAdd(self, positivePrompt):
        processedPrompt = self.Preprocess(positivePrompt)

        if processedPrompt is None:
            return False

        if CheckIfContainsWord(self.unwantedPrompts, processedPrompt):
            return False

        if CheckIfContainsWord(self.wantedPrompts, processedPrompt):
            return True

        return False

    def Preprocess(self, line: str) -> str:
        if line is None:
            return None

        tempLine = line.encode("ascii", "ignore")
        tempLine = tempLine.decode()
        tempLine = tempLine.replace("\n", ", ")
        tempLine = sub(r"<.+?>", "", tempLine)
        tempLine = tempLine.replace("\t", " ")

        if tempLine.startswith(" "):
            tempLine = tempLine[1:]

        wo_whitespace_list = [s.strip() for s in tempLine.split(",")]
        cleared_list = [s for s in wo_whitespace_list if s != " " and s != ""]

        tempLine = ", ".join(cleared_list)

        tempLine.replace(", ,", ", ")
        tempLine.replace(",\n", "\n")

        if tempLine.startswith(", "):
            tempLine = tempLine[2:]

        return tempLine
