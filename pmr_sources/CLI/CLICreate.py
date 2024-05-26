from re import sub
from os.path import exists
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from pmr_sources.Completer import Completer
import requests


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

        if self.positiveFilename.endswith(".txt") is False:
            self.positiveFilename = f"dataset/{self.positiveFilename}.txt"
        else:
            self.positiveFilename = f"dataset/{self.positiveFilename}"

        if self.negativeFilename.endswith(".txt") is False:
            self.negativeFilename = f"dataset/{self.negativeFilename}.txt"
        else:
            self.negativeFilename = f"dataset/{self.negativeFilename}"

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
                positiveLine = self.Preprocess(prompts[0].text)
                negativeLine = self.Preprocess(prompts[1].text)
                positivePrompts.append(f"{positiveLine}\n")
                negativePrompts.append(f"{negativeLine}\n")
            elif len(prompts) == 1:
                positiveLine = self.Preprocess(prompts[0].text)
                positivePrompts.append(f"{positiveLine}\n")

            positivePrompts = [*set(positivePrompts)]
            negativePrompts = [*set(negativePrompts)]

        try:
            positivePrompts.remove("\n")
            negativePrompts.remove("\n")
        except:
            temp = True

        positiveFile = open(self.positiveFilename, "w")
        negativeFile = open(self.negativeFilename, "w")

        positiveFile.writelines(positivePrompts)
        negativeFile.writelines(negativePrompts)

        positiveFile.close()
        negativeFile.close()

        print("Create> DONE !!!")

    def Preprocess(self, line):
        tempLine = line.replace("\n", "")
        tempLine = sub(r"<.+?>", "", tempLine)
        tempLine = tempLine.replace("  ", " ")
        tempLine = tempLine.replace("\t", " ")
        if tempLine.startswith(" "):
            tempLine = tempLine[1:]
        return tempLine
