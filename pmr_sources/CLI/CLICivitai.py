from json import loads
from requests import get
from re import findall
from collections import Counter
from string import punctuation
from os.path import exists, join
import gc

from pmr_sources.Completer import Completer

from pmr_sources.Utility import (
    ClearTerminal,
    Clamp,
    GetPromptSets,
    EnhancePreprocess,
    CheckPrompt,
    WritePromptsFile,
)

from pmr_sources.CompleteUtility import (
    creatorCompleter,
    sortCompleter,
    nsfwCompleter,
    periodCompleter,
)


class CLICivitai:
    positiveFilename = None
    negativeFilename = None
    wantedPrompts = ["beautiful", "female", "woman", "girl", "masterpiece"]
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
        self.completer.SetCompleteFunction(creatorCompleter)
        operation = ""
        while True:
            if operation == "enhance":
                self.positiveFilename = join(
                    "dataset", f"{input('Civitai> Positive Filename : ')}.txt"
                )
                self.negativeFilename = join(
                    "dataset", f"{input('Civitai> Negative Filename : ')}.txt"
                )
                imageLimit = Clamp(
                    int(input("Civitai> Image limit [1, 200] : ")), 1, 200
                )
                imageCursorStart = input("Civitai> Which image cursor to start : ")
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

                self.completer.SetCompleteFunction(sortCompleter)
                sort = (
                    input(
                        "Civitai> Select Sort [most_reactions, most_comments, newest] : "
                    )
                    .replace("_", "+")
                    .title()
                )

                self.completer.SetCompleteFunction(periodCompleter)
                period = input(
                    "Civitai> Select Period [allTime, year, month, week, day] : "
                ).capitalize()

                if period == "Alltime":
                    period = "AllTime"

                self.completer.SetCompleteFunction(nsfwCompleter)
                nsfw = input(
                    "Civitai> Select NSFW [none, soft, mature, x, all] : "
                ).capitalize()

                url = ""
                if nsfw == "All":
                    url = f"https://civitai.com/api/v1/images?limit={imageLimit}&sort={sort}&period={period}&cursor="
                else:
                    url = f"https://civitai.com/api/v1/images?limit={imageLimit}&sort={sort}&period={period}&nsfw={nsfw}&cursor="

                self.EnhanceDataset(imageCursorStart, url, hourEnd, minuteEnd)
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

    def EnhanceDataset(
        self,
        imageCursorStart: str,
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

        lastCurrentCursor = imageCursorStart
        checkErrorCounter = 0

        while True:
            currentTime = datetime.now()

            if currentTime.hour == hourEnd and currentTime.minute >= minuteEnd:
                print(f"Finished at {currentCursor} | Reached to specified time limit")
                break

            url = givenUrl + str(currentCursor)

            try:
                jsonFile = loads(get(url, headers=header).text)
            except:
                sleep(15.0)
                print("Trying again ...")
                continue

            print(f"Current Cursor : {currentCursor}")

            totalImageSize = len(jsonFile["items"])

            for index in range(totalImageSize):
                positivePrompt, negativePrompt = self.GetPrompts(jsonFile, index)

                if positivePrompt is None:
                    continue

                if (
                    CheckPrompt(
                        positivePrompt, self.wantedPrompts, self.unwantedPrompts
                    )
                    is False
                ):
                    continue

                positivePrompts.add(EnhancePreprocess(positivePrompt))

                if negativePrompt is None:
                    continue

                negativePrompts.add(EnhancePreprocess(negativePrompt))

            currentCursor = jsonFile["metadata"]["nextCursor"]
            currentCursor = (
                str(currentCursor)
                if currentCursor != None
                else str(currentCursor + totalImageSize)
            )

            checkErrorCounter = (
                checkErrorCounter + 1 if currentCursor == lastCurrentCursor else 0
            )

            lastCurrentCursor = currentCursor

            sleep(5.0)

        WritePromptsFile(positivePrompts, self.positiveFilename)
        del positivePrompts

        WritePromptsFile(negativePrompts, self.negativeFilename)
        del negativePrompts

        gc.collect()

    def GetPrompts(self, jsonFile, imageIndex):
        positivePrompt = None
        negativePrompt = None

        try:
            positivePrompt = jsonFile["items"][imageIndex]["meta"]["prompt"]
        except:
            pass

        try:
            negativePrompt = jsonFile["items"][imageIndex]["meta"]["negativePrompt"]
        except:
            pass

        return positivePrompt, negativePrompt

    def PruneFiles(self):
        positivePrompts, negativePrompts = GetPromptSets(
            self.positiveFilename, self.negativeFilename
        )

        WritePromptsFile(positivePrompts, self.positiveFilename)
        WritePromptsFile(negativePrompts, self.negativeFilename)

        print("Civitai> Done!!!")

    def FindWordFrequencies(self, filename):
        with open(filename, "r") as file:
            fileStr = file.read().translate(str.maketrans("", "", punctuation))

        counts = Counter(findall("\w+", fileStr))
        with open(join("dataset", "frequencies.txt"), "w") as f:
            for key, value in counts.items():
                f.write(f"{key} : {value}\n")

        print("Civitai> Done!!!")
