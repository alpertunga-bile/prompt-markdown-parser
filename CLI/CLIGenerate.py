from os.path import exists
from Completer import Completer
from Utility import ClearTerminal
from re import compile, sub


class CLIGenerate:
    minLength = 10
    maxLength = 50
    doSample = False
    earlyStop = False
    modelFolder = ""
    modelName = ""
    recursiveLevel = 0
    selfRecursive = False
    completer = None

    def __init__(self, completer: Completer):
        self.completer = completer

    def Start(self):
        self.modelName = input("Generate> Model Name (E.g. gpt2) : ")
        self.modelFolder = input("Generate> Model Folder Path : ")
        while exists(self.modelFolder) is False:
            print(
                f"Generate> {self.modelFolder} is not exists. Please enter a valid path!"
            )
            self.modelFolder = input("Generate> Model Folder Path : ")
        self.completer.SetCompleteFunction("yesOrNo")
        self.minLength = int(input("Generate> Min Length : "))
        self.maxLength = int(input("Generate> Max Length : "))
        self.completer.SetCompleteFunction("yesOrNo")
        self.doSample = (
            True if input("Generate> Do Sample [yes|no] : ") == "yes" else False
        )
        self.completer.SetCompleteFunction("yesOrNo")
        self.earlyStop = (
            True if input("Generate> Early Stopping [yes|no] : ") == "yes" else False
        )
        self.recursiveLevel = int(input("Generate> Recursive Level : "))
        self.completer.SetCompleteFunction("yesOrNo")
        self.selfRecursive = (
            True if input("Generate> Self Recursive [yes|no] : ") == "yes" else False
        )
        self.Generate()

    def GenerateText(self, seed, model, generatorArgs):
        result = model.generate_text(seed, generatorArgs)
        generatedText = self.Preprocess(seed + result.text)

        if self.selfRecursive:
            for _ in range(0, self.recursiveLevel):
                result = model.generate_text(generatedText, generatorArgs)
                generatedText = self.Preprocess(result.text)
            generatedText = self.Preprocess(seed + generatedText)
        else:
            for _ in range(0, self.recursiveLevel):
                result = model.generate_text(generatedText, generatorArgs)
                generatedText += result.text
                generatedText = self.Preprocess(generatedText)

        return generatedText

    def SetVariable(self, variableName):
        if variableName == "minLength":
            self.minLength = int(input("Generate-Set> Set Min Length : "))
        elif variableName == "maxLength":
            self.maxLength = int(input("Generate-Set> Set Max Length : "))
        elif variableName == "doSample":
            self.doSample = (
                True
                if input("Generate-Set> Set Do Sample [yes|no] : ") == "yes"
                else False
            )
        elif variableName == "earlyStop":
            self.earlyStop = (
                True
                if input("Generate-Set> Set Early Stopping [yes|no] : ") == "yes"
                else False
            )
        elif variableName == "recursiveLevel":
            self.recursiveLevel = int(input("Generate-Set> Set Recursive Level : "))
        elif variableName == "selfRecursive":
            self.selfRecursive = (
                True
                if input("Generate-Set> Set Self Recursive [yes|no] : ") == "yes"
                else False
            )

    def PrintVariables(self):
        print(f"Model Name      : {self.modelName}")
        print(f"Model Folder    : {self.modelFolder}")
        print(f"Min Length      : {self.minLength}")
        print(f"Max Length      : {self.maxLength}")
        print(f"Do Sample       : {self.doSample}")
        print(f"Early Stop      : {self.earlyStop}")
        print(f"Recursive Level : {self.recursiveLevel}")
        print(f"Self Recursive  : {self.selfRecursive}")

    def Generate(self):
        upperModelName = self.modelName.upper()

        if self.modelName.find("/") != -1:
            upperModelName = self.modelName.split("/")[1].upper()

        from happytransformer import HappyGeneration, GENSettings

        model = HappyGeneration(
            upperModelName, self.modelName, load_path=self.modelFolder
        )

        while 1:
            self.completer.SetCompleteFunction("generateOrSet")
            operation = input(
                "Generate> Select an operation [generate|set|print|clear|cls|exit] : "
            )

            if operation == "generate":
                generatorArgs = GENSettings(
                    min_length=self.minLength,
                    max_length=self.maxLength,
                    do_sample=self.doSample,
                    early_stopping=self.earlyStop,
                )

                seed = input("Generate> Enter seed : ")
                generatedText = self.GenerateText(seed, model, generatorArgs)

                print(f"Generate> Generated Text : {generatedText}")
            if operation == "print":
                self.PrintVariables()
            elif operation == "set":
                self.completer.SetCompleteFunction("selectVariableToSet")
                variableName = input(
                    "Generate> Choose A Variable To Set [minLength|maxLength|doSample|earlyStop|recursiveLevel|selfRecursive] : "
                )
                self.SetVariable(variableName)
            elif operation == "clear" or operation == "cls":
                ClearTerminal()
            elif operation == "exit":
                return

    def RemoveDuplicates(self, lineList):
        return list(dict.fromkeys(lineList))

    def Preprocess(self, line):
        pattern = compile(r"(,\s){2,}")

        tempLine = line.replace("\xa0", " ")
        tempLine = tempLine.replace("\n", ", ")
        tempLine = tempLine.replace("  ", " ")
        tempLine = tempLine.replace("\t", " ")
        tempLine = sub(pattern, ", ", tempLine)

        tempLine = ", ".join(self.RemoveDuplicates(tempLine.split(",")))

        return tempLine
