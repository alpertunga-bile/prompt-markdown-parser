from pmr_sources.Utility import ClearTerminal
from pmr_sources.CLI.CLIParse import CLIParse
from pmr_sources.CLI.CLICivitai import CLICivitai
from pmr_sources.CLI.CLICreate import CLICreate
from pmr_sources.CLI.CLITrain import CLITrain
from pmr_sources.CLI.CLIEvaluate import CLIEvaluate
from pmr_sources.CLI.CLIGenerate import CLIGenerate
from pmr_sources.Completer import Completer
from pmr_sources.CompleteUtility import AddFunctions, mainCompleter


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
