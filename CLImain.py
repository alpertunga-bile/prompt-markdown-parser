from sources.Utility import ClearTerminal
from sources.CLI.CLIParse import CLIParse
from sources.CLI.CLICivitai import CLICivitai
from sources.CLI.CLICreate import CLICreate
from sources.CLI.CLITrain import CLITrain
from sources.CLI.CLIEvaluate import CLIEvaluate
from sources.CLI.CLIGenerate import CLIGenerate
from sources.Completer import Completer
from sources.CompleteUtility import AddFunctions, mainCompleter


if __name__ == "__main__":
    ClearTerminal()

    completer = Completer()
    AddFunctions(completer)

    completer.SetCompleteFunction(mainCompleter)
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
            completer.SetCompleteFunction(mainCompleter)
            operation = input(
                "Main> Select an operation [parse|create|civitai|train|evaluate|generate|clear|cls|exit] : "
            )
