from os.path import exists, join, splitext
from os import getcwd
from glob import glob
from tqdm import tqdm
from deep_translator import GoogleTranslator
from Completer import Completer


class CLIParse:
    promptFiles = []
    isTranslate = False
    translator = None
    completer = None

    def __init__(self, completer: Completer):
        self.completer = completer

    def Start(self):
        self.completer.SetCompleteFunction("parserOperation")
        operation = input("Parse> Choose an operation [allParse|parse|exit] : ")

        if operation == "allParse":
            self.ParseAllFiles()
        elif operation == "parse":
            self.completer.SetCompleteFunction("currentFilesAndFolders")
            filename = input("Parse> File path : ")
            self.promptFiles.append(filename)
            self.Run()
            self.promptFiles.clear()
        elif operation == "exit":
            return
        else:
            while (
                operation != "allParse" and operation != "parse" and operation != "exit"
            ):
                print("Parse> Invalid command")
                operation = input("Parse> Choose an operation [allParse|parse|exit] : ")

    def ParseAllFiles(self):
        fastPath = join(getcwd(), "prompts")
        if exists(fastPath) == False:
            print("Parse> There is no folder named 'prompts'")
            return
        self.promptFiles = glob(join(fastPath, "*.md"))
        print(f"Parse> {len(self.promptFiles)} files are found ...")
        self.Run()

    def Run(self):
        if self.promptFiles is None:
            print("Parse> Please Select At Least One File")
            return

        self.completer.SetCompleteFunction("yesOrNo")
        translate = input("Parse> Do you want to translate [yes|no] : ")
        while translate != "yes" and translate != "no":
            print("Parse> Invalid Command")
            translate = input("Parse> Do you want to translate [yes|no] : ")

        self.isTranslate = True if translate == "yes" else False
        if self.isTranslate:
            self.translator = GoogleTranslator(source="auto", target="en")

        for promptFile in tqdm(self.promptFiles, desc="Parsing Files"):
            if exists(promptFile) == False:
                print(f"Parse> {promptFile} is not exists | Skipping ...")
                continue

            self.ParseAndSave(promptFile)

        self.translator = None
        print("Parse> DONE!!!")

    def ParseAndSave(self, promptFile):
        file = open(promptFile, "r")
        lines = file.readlines()
        file.close()

        """
        Get folder path where is the Markdown file located
        """
        filename = splitext(promptFile)[0]

        positiveFilename = f"{filename}_positive.txt"
        negativeFilename = f"{filename}_negative.txt"

        positiveStr = ""
        negativeStr = ""

        isPositive = True
        for line in lines:
            """
            Determine if positive or negative prompt
            """
            if line.find("Positive Prompts") != -1:
                isPositive = True
            elif line.find("Negative Prompts") != -1:
                isPositive = False

            """
            Continue if it is heading, new line, long line
            """
            if (
                line.startswith("#")
                or line == "\n"
                or line.startswith("---")
                or line == "  \n"
            ):
                continue

            line = self.Preprocess(line)

            if isPositive:
                positiveStr = positiveStr + line
            else:
                negativeStr = negativeStr + line

        """
        Delete comma and white space ', ' which is added in preprocess stage from the last of the line
        """
        positiveStr = positiveStr[:-2]
        negativeStr = negativeStr[:-2]

        positiveFile = open(positiveFilename, "w")
        positiveFile.write(positiveStr)
        positiveFile.close()

        negativeFile = open(negativeFilename, "w")
        negativeFile.write(negativeStr)
        negativeFile.close()

    """
    Preprocess the line that get from markdown file
    """

    def Preprocess(self, line):
        """
        Check mostly used starting syntax
        """
        if line.startswith("- [ ] ") or line.startswith("- [x] "):
            line = line[6:]
        elif line.startswith("-[ ] ") or line.startswith("-[x] "):
            line = line[5:]
        elif line.startswith("-[] "):
            line = line[4:]
        elif line.startswith("- ") or line.startswith("> "):
            line = line[2:]

        """
        Check for newline operator
        """
        if line.endswith("\n"):
            line = line[:-1]

        """
        Check for whitespaces
        """
        line = line.strip()

        if self.isTranslate:
            line = self.translator.translate(line)

        """
        Add comma to seperate prompts and provide continuousness 
        """
        line = line + ", "

        return line
