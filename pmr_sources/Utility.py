from subprocess import run
from os import name as os_name
from typing import Tuple
from os.path import exists
from string import punctuation
from re import IGNORECASE, compile, sub, split


def ClearTerminal() -> None:
    run("cls" if os_name == "nt" else "clear", shell=True)


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


def CheckPrompt(
    positive_prompt: str, wanted_prompts: list[str], unwanted_prompts: list[str]
) -> bool:
    processed_prompt = EnhancePreprocess(positive_prompt)

    if CheckIfContainsWord(unwanted_prompts, processed_prompt):
        return False

    if CheckIfContainsWord(wanted_prompts, processed_prompt):
        return True

    return False


def WritePromptsFile(prompts: set[str], filepath: str) -> None:
    listPrompts = AddNewlineToList(prompts)
    print(f"Saving to {filepath}")

    with open(filepath, "w") as file:
        file.writelines(listPrompts)


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


def EnhancePreprocess(line: str) -> str:
    # encodings
    tempLine = line.encode("ascii", "xmlcharrefreplace").decode()
    tempLine = tempLine.encode(errors="xmlcharrefreplace").decode()  # utf-8

    tempLine = tempLine.replace("\n", ", ")
    tempLine = sub(r",?\s*<.+?>:?[0-9]*\.?[0-9]*", "", tempLine)  # delete lora names
    tempLine = tempLine.replace("\t", " ")
    tempLine = tempLine.lstrip()

    tempLine = sub(
        r",\s*:[0-9]*\.?[0-9]+", "", tempLine
    )  # delete scalars that left without prompts

    cleared_list = []

    prompts = split(
        r",\s*(?![^()]*\))", tempLine
    )  # split by comma respect to single parantheses

    # clear the scalars without prompts and non alphabetical prompts
    for prompt in prompts:
        tempPrompt = sub(r"[^a-zA-Z()\[\]{}]*", "", prompt).lstrip()

        if tempPrompt == "":
            continue

        # check if just contains parantheses if it is than it is valuable else it is not
        if sub(r"[()\[\]{}]*", "", tempPrompt) == "":
            cleared_list.append(tempPrompt)
        else:
            cleared_list.append(prompt)

    tempLine = ", ".join(cleared_list)

    # fix join function artifacts
    tempLine = tempLine.replace("(,", "(")
    tempLine = tempLine.replace("[,", "[")
    tempLine = tempLine.replace("{,", "{")

    return tempLine
