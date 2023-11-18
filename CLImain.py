from Utility import ClearTerminal
from CLI.CLIParse import CLIParse
from CLI.CLICivitai import CLICivitai
from CLI.CLICreate import CLICreate
from CLI.CLITrain import CLITrain
from CLI.CLIEvaluate import CLIEvaluate
from CLI.CLIGenerate import CLIGenerate
from Completer import Completer


def AddFunctions(completer: Completer):
    completer.CreateCompleteFunction(
        "mainOperation",
        [
            "parse",
            "clear",
            "cls",
            "create",
            "civitai",
            "train",
            "evaluate",
            "exit",
            "generate",
        ],
    )
    completer.CreateCompleteFunction("parserOperation", ["allParse", "exit", "parse"])
    completer.CreateCurrentDirectoryFilesAndFoldersCompleteFunction(
        "currentFilesAndFolders"
    )
    completer.CreateCompleteFunction("yesOrNo", ["yes", "no"])
    completer.CreateCompleteFunction(
        "generateOrSet", ["generate", "set", "exit", "clear", "cls", "print"]
    )
    completer.CreateCompleteFunction(
        "selectVariableToSet",
        [
            "minLength",
            "maxLength",
            "doSample",
            "earlyStop",
            "recursiveLevel",
            "selfRecursive",
        ],
    )
    completer.CreateCompleteFunction(
        "createrOperation", ["enhance", "prune", "frequency", "clear", "cls", "exit"]
    )
    completer.CreateCompleteFunction(
        "createrNSFW", ["none", "soft", "mature", "x", "all"]
    )
    completer.CreateCompleteFunction(
        "createSort", ["most_reactions", "most_comments", "newest"]
    )
    completer.CreateCompleteFunction(
        "createrPeriod", ["allTime", "year", "month", "week", "day"]
    )


if __name__ == "__main__":
    ClearTerminal()
    completer = Completer()
    AddFunctions(completer)
    completer.SetCompleteFunction("mainOperation")
    operation = input(
        "Main> Select an operation [parse|create|civitai|train|evaluate|generate|clear|cls|exit] : "
    )

    while True:
        if operation == "parse":
            cliParse = CLIParse(completer)
            cliParse.Start()
            operation = ""
        elif operation == "clear" or operation == "cls":
            ClearTerminal()
            operation = ""
        elif operation == "create":
            cliCreate = CLICreate(completer)
            cliCreate.Start()
            operation = ""
        elif operation == "civitai":
            cliCivitai = CLICivitai(completer)
            cliCivitai.Start()
            operation = ""
        elif operation == "train":
            cliTrain = CLITrain()
            cliTrain.Start()
            operation = ""
        elif operation == "evaluate":
            cliEvaluate = CLIEvaluate()
            cliEvaluate.Start()
            operation = ""
        elif operation == "exit":
            exit(0)
        elif operation == "generate":
            cliGenerate = CLIGenerate(completer)
            cliGenerate.Start()
            operation = ""
        else:
            completer.SetCompleteFunction("mainOperation")
            operation = input(
                "Main> Select an operation [parse|create|civitai|train|evaluate|generate|clear|cls|exit] : "
            )
