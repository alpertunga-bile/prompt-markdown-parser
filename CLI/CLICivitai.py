from json import loads
from requests import get
from re import sub, findall
from collections import Counter
from string import punctuation
from os.path import exists
from tqdm import tqdm
from readline import set_completer
from CLI.Utility import *
import gc

class CLICivitai:
    maxPage = 0
    positiveFilename = ""
    negativeFilename = ""
    wantedPrompts = ["beautiful", "female", "breasts", "woman", "girl", "masterpiece"]
    unwantedPrompts = ["obese", "fat", "ugly", "weird", "creepy", "loli", "old woman", "old", "child", "creature", "kid"]

    def __init__(self):
        url = f"https://civitai.com/api/v1/images?limit=1"
        header = {"content-type":"application.json"}
        jsonFile = loads(get(url, headers=header).text)
        self.maxPage = int(jsonFile['metadata']['totalPages'])

    def Start(self):
        set_completer(CreatorOperationComplete)
        operation = ''
        while 1:
            if operation == 'enhance':
                self.positiveFilename = f"Civitai> dataset/{input('Positive Filename : ')}.txt"
                self.negativeFilename = f"Civitai> dataset/{input('Negative Filename : ')}.txt"
                limit = int(input("Civitai> Image limit [1, 200] : "))
                minPage = Clamp(int(input("Civitai> Which page number to start : ")), 1, self.maxPage)
                maxPage = Clamp(int(input("Civitai> Which page to end : ")) + 1, minPage + 1, self.maxPage)
                wantedPrompts = input("Civitai> Write Your Wanted Prompts Seperate With Comma (or write none to use default): ")
                
                print(', '.join(self.wantedPrompts))

                if wantedPrompts != "none":
                    self.wantedPrompts = wantedPrompts.split(",")

                unwantedPrompts = input("Civitai> Write Your Unwanted Prompts Seperate With Comma (or write none to use default): ")

                if unwantedPrompts != "none":
                    self.unwantedPrompts = unwantedPrompts.split(",")

                print(', '.join(self.unwantedPrompts))

                set_completer(CreatorSortComplete)
                sort = input("Civitai> Select Sort [most_reactions, most_comments, newest] : ").replace("_", "+").title()
                set_completer(CreatorPeriodComplete)
                period = input("Civitai> Select Period [allTime, year, month, week, day] : ").capitalize().replace("t", "T")
                set_completer(CreatorNSFWComplete)
                nsfw = input("Civitai> Select NSFW [none, soft, mature, x] : ").capitalize()
                url = f"https://civitai.com/api/v1/images?limit={limit}&sort={sort}&period={period}&nsfw={nsfw}&page="
                
                self.EnhanceDataset(minPage, maxPage, url)
                operation = ''
            elif operation == 'prune':
                self.positiveFilename = input("Civitai> Positive Filename : ") + ".txt"
                self.negativeFilename = input("Civitai> Negative Filename : ") + ".txt"
                self.PruneFiles()
                operation = ''
            elif operation == 'frequency':
                filename = input("Civitai> Filename : ") + ".txt"
                self.FindWordFrequencies(filename)
                operation = ''
            elif operation == 'cls' or operation == 'clear':
                ClearTerminal()
                operation = ''
            elif operation == 'exit':
                return
            else:
                operation = input("Civitai> Select an operation [enhance|prune|frequency|clear|cls|exit] : ")
        return

    def EnhanceDataset(self, min, max, givenUrl):
        positivePrompts = []
        negativePrompts = []

        if exists(self.positiveFilename) is False:
            file = open(self.positiveFilename, "w")
            file.close()
        
        if exists(self.negativeFilename) is False:
            file = open(self.negativeFilename, "w")
            file.close()

        header = {"content-type":"application.json"}

        for pageNumber in tqdm(range(min, max), desc="Civitai> Getting Data From Pages"):
            url = givenUrl + str(pageNumber)
            jsonFile = loads(get(url, headers=header).text)

            for imageIndex in range(0, 200):
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

        positiveFile = open(self.positiveFilename, "a")
        positiveFile.writelines(positivePrompts)
        positiveFile.close()

        positivePrompts.clear()

        negativeFile = open(self.negativeFilename, "a")
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

    def PruneFiles(self):
        if exists(self.positiveFilename):
            positiveFile = open(self.positiveFilename, "r")
            positivePrompts = positiveFile.readlines()
            positiveFile.close()

        if exists(self.negativeFilename):
            negativeFile = open(self.negativeFilename, "r")
            negativePrompts = negativeFile.readlines()
            negativeFile.close()

        positivePrompts = list(set(positivePrompts))
        negativePrompts = list(set(negativePrompts))

        positiveFile = open(self.positiveFilename, "w")
        positiveFile.writelines(positivePrompts)
        positiveFile.close()

        negativeFile = open(self.negativeFilename, "w")
        negativeFile.writelines(negativePrompts)
        negativeFile.close()

    def FindWordFrequencies(self, filename):
        file = open(filename, "r")
        fileStr = file.read()
        file.close()

        fileStr = fileStr.translate(str.maketrans('', '', punctuation))

        counts = Counter(findall('\w+', fileStr))
        with open("dataset/frequencies.txt", "w") as f:
            for key, value in counts.items():
                f.write(f'{key} : {value}\n')

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