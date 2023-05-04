from os import getcwd
from os.path import exists
from tkinter.filedialog import askopenfilename
from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkEntry, CTkProgressBar
from threading import Thread
from re import sub
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
import requests

class DatasetTab:
    parentWindow = None
    thisTab = None
    
    datasetPath = None
    
    variableFrame = None
    datasetLinkLabel = None
    positiveFileEntry = None
    negativeFileEntry = None
    infoLabel = None

    progressBar = None

    def __init__(self, parent, tab):
        self.parentWindow = parent
        self.thisTab = tab
        self.datasetPath = getcwd()

        self.variableFrame = CTkFrame(master=self.thisTab)

        self.datasetLinkLabel = CTkLabel(master=self.variableFrame, text=self.datasetPath)
        
        selectDatasetButton = CTkButton(
            master=self.variableFrame, 
            text="Choose Dataset",
            command=self.ChooseDataset
        )

        positiveNameLabel = CTkLabel(master=self.variableFrame, text="Dataset Positive Filename")
        self.positiveFileEntry = CTkEntry(master=self.variableFrame, placeholder_text="E.g. positive")
        negativeNameLabel = CTkLabel(master=self.variableFrame, text="Dataset Negative Filename")
        self.negativeFileEntry = CTkEntry(master=self.variableFrame, placeholder_text="E.g. negative")

        self.datasetLinkLabel.grid(column=0, row=0, padx=(0, 50), ipady=5, pady=10)
        selectDatasetButton.grid(column=1, row=0)
        positiveNameLabel.grid(column=0, row=1, padx=(0, 50), ipady=5, pady=10)
        self.positiveFileEntry.grid(column=1, row=1)
        negativeNameLabel.grid(column=0, row=2, padx=(0, 50), ipady=5, pady=10)
        self.negativeFileEntry.grid(column=1, row=2)

        self.variableFrame.pack(pady=10)

        self.infoLabel = CTkLabel(master=self.thisTab, text="")
        self.infoLabel.pack()

        createDatasetButton = CTkButton(
            master=self.thisTab,
            text="Create Dataset",
            command=self.CreateDataset
        )
        createDatasetButton.pack()

        self.progressBar = CTkProgressBar(
            master=self.thisTab,
            orientation='horizontal',
            mode='determinate'
        )
        self.progressBar.set(0)
        self.progressBar.pack_forget()

    def ChooseDataset(self):
        self.datasetPath = askopenfilename(initialdir=getcwd())
        self.datasetLinkLabel.configure(text=self.datasetPath)

    def CreateDataset(self):
        self.Refresh()
        Thread(target=self.Create).start()

    def Create(self):
        positiveFilename = self.positiveFileEntry.get()
        negativeFilename = self.negativeFileEntry.get()

        if positiveFilename == "" or negativeFilename == "":
            self.infoLabel.configure(text="Please Enter Filename")
            return
        
        if self.datasetPath == getcwd():
            self.infoLabel.configure(text="Please Select Valid Dataset File")
            return

        self.infoLabel.configure(text="")
        linksFile = open(self.datasetPath, "r")
        promptLinks = linksFile.readlines()
        linksFile.close()

        if len(promptLinks) == 0:
            self.infoLabel.configure(text="There are no links in given file")
            return

        positivePrompts = []
        negativePrompts = []

        """
        Set progressbar variables
        """
        self.progressBar.set(0)
        self.progressBar.pack(ipadx=100, pady=10)
        completedLink = 0
        totalLinks = len(promptLinks)

        if positiveFilename.endswith(".txt") is False:
            positiveFilename = f"dataset/{positiveFilename}.txt"
        else:
            positiveFilename = f"dataset/{positiveFilename}"
        
        if negativeFilename.endswith(".txt") is False:
            negativeFilename = f"dataset/{negativeFilename}.txt"
        else:
            negativeFilename = f"dataset/{negativeFilename}"

        if exists(positiveFilename) == True:
            positiveFile = open(positiveFilename, 'r')
            positivePrompts = positiveFile.readlines()
            positiveFile.close()
            
        if exists(negativeFilename) == True:
            negativeFile = open(negativeFilename, 'r')
            negativePrompts = negativeFile.readlines()
            negativeFile.close()

        for promptLink in tqdm(promptLinks, desc="Getting and Writing Prompts"):
            info = requests.get(promptLink).text
            soup = bs(info, "lxml")
            prompts = soup.findAll("pre", {"class":"mantine-Code-root mantine-Code-block mantine-2v44jn"})
            
            if len(prompts) == 2:
                positiveLine = self.Preprocess(prompts[0].text)
                negativeLine = self.Preprocess(prompts[1].text)
                positivePrompts.append(f"{positiveLine}\n")
                negativePrompts.append(f"{negativeLine}\n")
            elif len(prompts) == 1:
                positiveLine = self.Preprocess(prompts[0].text)
                positivePrompts.append(f"{positiveLine}\n")

            completedLink = completedLink + 1
            self.progressBar.set(float(completedLink) / float(totalLinks))

        self.progressBar.pack_forget()

        positivePrompts = [*set(positivePrompts)]
        negativePrompts = [*set(negativePrompts)]

        try:
            positivePrompts.remove("\n")
            negativePrompts.remove("\n")
        except:
            print("Allrighto")

        positiveFile = open(positiveFilename, 'w')
        negativeFile = open(negativeFilename, 'w')

        positiveFile.writelines(positivePrompts)
        negativeFile.writelines(negativePrompts)

        positiveFile.close()
        negativeFile.close()

        self.infoLabel.configure(text="DONE !!!")

    def Preprocess(self, line):
        tempLine = line.replace("\n", "")
        tempLine = sub(r'<.+?>', '', tempLine)
        tempLine = tempLine.replace("  ", " ")
        tempLine = tempLine.replace("\t", " ")
        if tempLine.startswith(" "):
            tempLine = tempLine[1:]
        return tempLine
    
    def Refresh(self):
        self.parentWindow.update()
        self.parentWindow.after(1000, self.Refresh)