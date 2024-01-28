from json import loads
from requests import get
from re import sub, findall
from collections import Counter
from string import punctuation
from os.path import exists, join
from tqdm import tqdm
from Completer import Completer
from Utility import (
    ClearTerminal,
    Clamp,
    GetPromptSets,
    CheckIfContainsWord,
    AddNewlineToList,
)
import gc


class CLICivitai:
    positiveFilename = ""
    negativeFilename = ""
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
    completer = None

    def __init__(self, completer: Completer) -> None:
        self.completer = completer

    def Start(self) -> None:
        self.completer.SetCompleteFunction("createrOperation")
        operation = ""
        while 1:
            if operation == "enhance":
                self.positiveFilename = join(
                    "dataset", f"{input('Civitai> Positive Filename : ')}.txt"
                )
                self.negativeFilename = join(
                    "dataset", f"{input('Civitai> Negative Filename : ')}.txt"
                )
                imageLimit = Clamp(
                    int(input("Civitai> Image limit [1, 200] : ")), 0, 200
                )
                imageCursorStart = int(input("Civitai> Which image cursor to start : "))
                hourEnd = Clamp(int(input("Civitai> Which hour to end : ")), 0, 23)
                minuteEnd = Clamp(int(input("Civitai> Which minute to end : ")), 0, 59)
                print(f"Current Wanted Prompts Are [{', '.join(self.wantedPrompts)}]")
                wantedPrompts = input(
                    "Civitai> Write Your Wanted Prompts Seperate With Comma (or write none to use default): "
                )

                if wantedPrompts != "none":
                    self.wantedPrompts = wantedPrompts.split(",")

                print(f"Current Unwanted Prompts Are {', '.join(self.unwantedPrompts)}")
                unwantedPrompts = input(
                    "Civitai> Write Your Unwanted Prompts Seperate With Comma (or write none to use default): "
                )

                if unwantedPrompts != "none":
                    self.unwantedPrompts = unwantedPrompts.split(",")

                self.completer.SetCompleteFunction("createSort")
                sort = (
                    input(
                        "Civitai> Select Sort [most_reactions, most_comments, newest] : "
                    )
                    .replace("_", "+")
                    .title()
                )
                self.completer.SetCompleteFunction("createrPeriod")
                period = (
                    input("Civitai> Select Period [allTime, year, month, week, day] : ")
                    .capitalize()
                    .replace("t", "T")
                )
                self.completer.SetCompleteFunction("createrNSFW")
                nsfw = input(
                    "Civitai> Select NSFW [none, soft, mature, x, all] : "
                ).capitalize()
                url = ""
                if nsfw == "All":
                    url = f"https://civitai.com/api/v1/images?limit={imageLimit}&sort={sort}&period={period}&cursor="
                else:
                    url = f"https://civitai.com/api/v1/images?limit={imageLimit}&sort={sort}&period={period}&nsfw={nsfw}&cursor="

                self.EnhanceDataset(
                    imageLimit, imageCursorStart, url, hourEnd, minuteEnd
                )
                operation = ""
            elif operation == "prune":
                self.positiveFilename = join(
                    "dataset", f"{input('Positive Filename : ')}.txt"
                )
                self.negativeFilename = join(
                    "dataset", f"{input('Negative Filename : ')}.txt"
                )
                self.PruneFiles()
                operation = ""
            elif operation == "frequency":
                filename = join("dataset", f"{input('Civitai> Filename : ')}.txt")
                self.FindWordFrequencies(filename)
                operation = ""
            elif operation == "cls" or operation == "clear":
                ClearTerminal()
                operation = ""
            elif operation == "exit":
                return
            else:
                self.completer.SetCompleteFunction("createrOperation")
                operation = input(
                    "Civitai> Select an operation [enhance|prune|frequency|clear|cls|exit] : "
                )
        return

    def EnhanceDataset(
        self,
        imageLimit: int,
        imageCursorStart: int,
        givenUrl: str,
        hourEnd: int,
        minuteEnd: int,
    ) -> None:
        from datetime import datetime
        from time import sleep

        positivePrompts, negativePrompts = GetPromptSets(
            self.positiveFilename, self.negativeFilename
        )

        header = {"content-type": "application.json"}

        currentCursor = imageCursorStart

        while True:
            currentTime = datetime.now()

            if currentTime.hour == hourEnd and currentTime.minute >= minuteEnd:
                print(f"Finished at {currentCursor} | Reached to specified time limit")
                break

            url = givenUrl + str(currentCursor)

            try:
                jsonFile = loads(get(url, headers=header).text)
            except:
                print(f"Can't fetch the json file at {currentCursor}")
                return

            print(f"Image Cursor : {currentCursor}")

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

        self.WritePromptsFile(positivePrompts, self.positiveFilename)
        del positivePrompts

        self.WritePromptsFile(negativePrompts, self.negativeFilename)
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

    def PruneFiles(self):
        positivePrompts, negativePrompts = GetPromptSets(
            self.positiveFilename, self.negativeFilename
        )

        self.WritePromptsFile(positivePrompts, self.positiveFilename)
        self.WritePromptsFile(negativePrompts, self.negativeFilename)

        print("Civitai> Done!!!")

    def FindWordFrequencies(self, filename):
        with open(filename, "r") as file:
            fileStr = file.read().translate(str.maketrans("", "", punctuation))

        counts = Counter(findall("\w+", fileStr))
        with open(join("dataset", "frequencies.txt"), "w") as f:
            for key, value in counts.items():
                f.write(f"{key} : {value}\n")

        print("Civitai> Done!!!")

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
