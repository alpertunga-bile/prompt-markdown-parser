from os.path import exists, join
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from sources.Completer import Completer
import requests

from sources.Utility import (
    EnhancePreprocess,
    GetFilenameWithExtension,
    WritePromptsFile,
    GetPromptSets,
)


class CLICreate:
    completer = None

    def __init__(completer: Completer):
        completer = completer

    def Start(self):
        datasetPath = input("Create> Dataset Path : ")
        while exists(datasetPath) is False:
            print(f"Create> {datasetPath} is not exists. Please enter a valid path!")
            datasetPath = input("Create> Dataset Path : ")

        positiveFilename = input("Create> Positive Filename : ")
        negativeFilename = input("Create> Negative Filename : ")
        self.Create(datasetPath, positiveFilename, negativeFilename)

    def Create(self, datasetPath: str, positiveFilename: str, negativeFilename: str):
        linksFile = open(datasetPath, "r")
        promptLinks = linksFile.readlines()

        if len(promptLinks) == 0:
            print("Create> There are no links in the file")
            return

        positiveFilename = GetFilenameWithExtension(
            join("dataset", positiveFilename), "txt"
        )
        negativeFilename = GetFilenameWithExtension(
            join("dataset", negativeFilename), "txt"
        )

        positivePrompts, negativePrompts = GetPromptSets(
            positiveFilename, self.negativeFilename
        )

        for promptLink in tqdm(promptLinks, desc="Create> Getting and Writing Prompts"):
            info = requests.get(promptLink).text
            soup = bs(info, "lxml")
            prompts = soup.findAll(
                "pre", {"class": "mantine-Code-root mantine-Code-block mantine-2v44jn"}
            )

            if len(prompts) == 2:
                positiveLine = EnhancePreprocess(prompts[0].text)
                negativeLine = EnhancePreprocess(prompts[1].text)
                positivePrompts.append(f"{positiveLine}\n")
                negativePrompts.append(f"{negativeLine}\n")
            elif len(prompts) == 1:
                positiveLine = EnhancePreprocess(prompts[0].text)
                positivePrompts.append(f"{positiveLine}\n")

            positivePrompts = [*set(positivePrompts)]
            negativePrompts = [*set(negativePrompts)]

        try:
            positivePrompts.remove("\n")
            negativePrompts.remove("\n")
        except:
            pass

        WritePromptsFile(positivePrompts, positiveFilename)
        WritePromptsFile(negativePrompts, negativeFilename)

        print("Create> DONE !!!")
