from CLI.Utility import ClearTerminal, MainOperationComplete
from CLI.CLIParse import CLIParse
from CLI.CLICreate import CLICreate
from CLI.CLITrain import CLITrain
from CLI.CLIEvaluate import CLIEvaluate
from CLI.CLIGenerate import CLIGenerate
from readline import parse_and_bind, set_completer

if __name__ == "__main__":
    ClearTerminal()
    parse_and_bind("tab: complete")
    set_completer(MainOperationComplete)
    operation = input("Select an operation [parse|create|train|evaluate|generate|clear|cls|exit] : ")
    
    while 1:
        if operation == 'parse':
            cliParse = CLIParse()
            cliParse.Start()
            operation=''
        elif operation == 'clear' or operation == 'cls':
            ClearTerminal()
            operation=''
        elif operation == 'create':
            cliCreate = CLICreate()
            cliCreate.Start()
            operation=''
        elif operation == 'train':
            cliTrain = CLITrain()
            cliTrain.Start()
            operation=''
        elif operation == 'evaluate':
            cliEvaluate = CLIEvaluate()
            cliEvaluate.Start()
            operation=''
        elif operation == 'exit':
            exit(0)
        elif operation == 'generate':
            cliGenerate = CLIGenerate()
            cliGenerate.Start()
            operation=''
        else:
            set_completer(MainOperationComplete)
            operation = input("Select an operation [parse|create|train|evaluate|generate|clear|cls|exit] : ")