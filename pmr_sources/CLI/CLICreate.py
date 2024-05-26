from os.path import exists, join
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from pmr_sources.Completer import Completer
import requests

from pmr_sources.Utility import (
    EnhancePreprocess,
    GetFilenameWithExtension,
    WritePromptsFile,
)


class CLICreate:
    datasetPath = ""
    positiveFilename = ""
    negativeFilename = ""
    completer = None

    def __init__(self, completer: Completer):
        self.completer = completer

    def Start(self):
        self.completer.SetCompleteFunction("currentFilesAndFolders")
        self.datasetPath = input("Create> Dataset Path : ")
        while exists(self.datasetPath) is False:
            print(
                f"Create> {self.datasetPath} is not exists. Please enter a valid path!"
            )
            self.datasetPath = input("Create> Dataset Path : ")
        self.positiveFilename = input("Create> Positive Filename : ")
        self.negativeFilename = input("Create> Negative Filename : ")
        self.Create()

    def Create(self):
        linksFile = open(self.datasetPath, "r")
        promptLinks = linksFile.readlines()

        if len(promptLinks) == 0:
            print("Create> There are no links in the file")
            return

        positivePrompts = []
        negativePrompts = []

        self.positiveFilename = GetFilenameWithExtension(
            join("dataset", self.positiveFilename), "txt"
        )
        self.negativeFilename = GetFilenameWithExtension(
            join("dataset", self.negativeFilename), "txt"
        )

        if exists(self.positiveFilename) == True:
            positiveFile = open(self.positiveFilename, "r")
            positivePrompts = positiveFile.readlines()
            positiveFile.close()

        if exists(self.negativeFilename) == True:
            negativeFile = open(self.negativeFilename, "r")
            negativePrompts = negativeFile.readlines()
            negativeFile.close()

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

        WritePromptsFile(positivePrompts, self.positiveFilename)
        WritePromptsFile(negativePrompts, self.negativeFilename)

        print("Create> DONE !!!")
