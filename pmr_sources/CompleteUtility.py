from .Completer import Completer

mainCompleter = "mainOperation"
parserCompleter = "parserOperation"
ynQuestionCompleter = "yesOrNo"
genOrSetCompleter = "generateOrSet"
variableSelectCompleter = "selectVariableToSet"
creatorCompleter = "createrOperation"
nsfwCompleter = "createrNSFW"
sortCompleter = "createSort"
periodCompleter = "createrPeriod"


def AddFunctions(completer: Completer):
    completer.CreateCompleteFunction(
        mainCompleter,
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
    completer.CreateCompleteFunction(parserCompleter, ["allParse", "exit", "parse"])
    completer.CreateCompleteFunction(ynQuestionCompleter, ["yes", "no"])
    completer.CreateCompleteFunction(
        genOrSetCompleter, ["generate", "set", "exit", "clear", "cls", "print"]
    )
    completer.CreateCompleteFunction(
        variableSelectCompleter,
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
        creatorCompleter, ["enhance", "prune", "frequency", "clear", "cls", "exit"]
    )
    completer.CreateCompleteFunction(
        nsfwCompleter, ["none", "soft", "mature", "x", "all"]
    )
    completer.CreateCompleteFunction(
        sortCompleter, ["most_reactions", "most_comments", "newest"]
    )
    completer.CreateCompleteFunction(
        periodCompleter, ["allTime", "year", "month", "week", "day"]
    )
