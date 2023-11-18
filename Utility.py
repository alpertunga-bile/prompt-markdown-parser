from subprocess import call
from os import name
from typing import Tuple
from os.path import exists
from string import punctuation
from re import IGNORECASE, compile


def ClearTerminal() -> None:
    call("cls" if name == "nt" else "clear", shell=True)


def Clamp(number, min, max):
    number = number if number > min else min
    number = number if number < max else max

    return number


def RemoveNewlineFromFileContents(contents: list[str]) -> list[str]:
    return [s.rstrip("\n") for s in contents]


def GetPrompt(filename: str) -> set:
    with open(filename) as file:
        promptSet = set(RemoveNewlineFromFileContents(file.readlines()))

    return promptSet


def GetPromptSets(positiveFilePath: str, negativeFilePath: str) -> Tuple[set, set]:
    if exists(positiveFilePath):
        positiveSet = GetPrompt(positiveFilePath)
    else:
        positiveSet = set()

    if exists(negativeFilePath):
        negativeSet = GetPrompt(negativeFilePath)
    else:
        negativeSet = set()

    return positiveSet, negativeSet


def GetPureString(complex_string: str) -> str:
    char_blacklist = set(f"{punctuation}0123456789")
    return "".join(c for c in complex_string if c not in char_blacklist)


def CheckWholeWord(word: str, whole_string: str) -> bool:
    return (
        True
        if compile(r"\b({0})\b".format(word), flags=IGNORECASE).search(whole_string)
        is not None
        else False
    )


def CheckIfContainsWord(word_list: list[str], whole_string: str) -> bool:
    pure_string = GetPureString(whole_string)

    for word in word_list:
        if CheckWholeWord(word, pure_string):
            return True

    return False


def AddNewlineToList(contents: list[str]) -> list[str]:
    return [s + "\n" for s in contents]
