from readline import parse_and_bind, set_completer, get_completer
from os import listdir, getcwd
from os.path import isfile, join


class CompleteFunction:
    vocabs: list = None
    completeFunc = None

    def __init__(self, completeFunc=None, vocabs=None):
        self.vocabs = vocabs
        self.completeFunc = completeFunc

    def Completer(self, text, state):
        results = [x for x in self.vocabs if x.startswith(text)] + [None]
        return results[state]

    def GetCompleter(self):
        if self.vocabs is None:
            return self.completeFunc
        else:
            return self.Completer


class Completer:
    completeDict = {}

    def __init__(self):
        parse_and_bind("tab: complete")

    def AddCompleteFunction(self, name, func, vocabs):
        completeFunc = CompleteFunction(func, vocabs)
        self.completeDict[name] = completeFunc

    def GetCompleteFunction(self, name):
        return self.completeDict[name]

    def DeleteCompleteFunction(self, name):
        if self.completeDict[name]:
            del self.completeDict[name]

    def SetCompleteFunction(self, name):
        if self.completeDict[name]:
            set_completer(self.completeDict[name].GetCompleter())

    def ClearCompleteFunction(self):
        set_completer(None)

    def GetCurrentCompleteFunction(self):
        return get_completer()

    def ClearAllFunctions(self):
        self.completeDict.clear()

    """
    Create Functions
    """

    def CreateCompleteFunction(self, name, vocabs: list):
        if name in self.completeDict:
            return

        self.AddCompleteFunction(name, None, vocabs)

    def CreateCurrentDirectoryFilesCompleteFunction(self, name):
        self.CreateGivenDirectoryFilesCompleteFunction(name, getcwd())

    def CreateGivenDirectoryFilesCompleteFunction(self, name, path):
        files = [f for f in listdir(path) if isfile(join(path, f))]
        self.AddCompleteFunction(name, None, files)

    def CreateCurrentDirectoryFilesAndFoldersCompleteFunction(self, name):
        self.CreateGivenDirectoryFilesAndFoldersCompleteFunction(name, getcwd())

    def CreateGivenDirectoryFilesAndFoldersCompleteFunction(self, name, path):
        files = listdir(path)
        self.AddCompleteFunction(name, None, files)

    def CreateCurrentDirectoryGivenExtensionFilesCompleteFunction(self, name, ext):
        self.CreateGivenDirectoryGivenExtensionFilesCompleteFunction(
            name, getcwd(), ext
        )

    def CreateGivenDirectoryGivenExtensionFilesCompleteFunction(self, name, path, ext):
        files = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith(ext)]
        self.AddCompleteFunction(name, None, files)

    def CreateCurrentDirectoryFoldersCompleteFunction(self, name):
        self.CreateGivenDirectoryFoldersCompleteFunction(name, getcwd())

    def CreateGivenDirectoryFoldersCompleteFunction(self, name, path):
        files = [f for f in listdir(path) if isfile(join(path, f)) is False]
        self.AddCompleteFunction(name, None, files)
