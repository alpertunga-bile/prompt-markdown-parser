import os
import customtkinter as ctk
import threading
from tkinter import filedialog
from happytransformer import HappyGeneration

class EvaluateTab:
    parentWindow = None
    thisTab = None

    variableFrame = None
    modelNameEntry = None
    databaseName = os.getcwd()
    modelPath = os.getcwd()
    datasetLabel = None
    modelLabel = None

    infoLabel = None

    def __init__(self, parent, tab):
        self.parentWindow = parent
        self.thisTab = tab

        self.variableFrame = ctk.CTkFrame(master=self.thisTab)

        modelNameLabel = ctk.CTkLabel(master=self.variableFrame, text="Model Name")
        self.modelNameEntry = ctk.CTkEntry(master=self.variableFrame, placeholder_text="E.g. gpt2")

        self.datasetLabel = ctk.CTkLabel(master=self.variableFrame, text=self.databaseName)

        selectDatasetButton = ctk.CTkButton(
            master=self.variableFrame,
            text="Choose Dataset",
            command=self.ChooseDataset
        )

        self.modelLabel = ctk.CTkLabel(master=self.variableFrame, text=self.modelPath)

        selectModelButton = ctk.CTkButton(
            master=self.variableFrame,
            text="Choose Model Folder",
            command=self.ChooseModel   
        )

        self.datasetLabel.grid(column=0, row=0, padx=(0, 50), ipady=5, pady=10)
        selectDatasetButton.grid(column=1, row=0)
        modelNameLabel.grid(column=0, row=1, padx=(0, 50), ipady=5, pady=10)
        self.modelNameEntry.grid(column=1, row=1)
        self.modelLabel.grid(column=0, row=2, padx=(0, 50), ipady=5, pady=10)
        selectModelButton.grid(column=1, row=2)

        self.variableFrame.pack()

        self.infoLabel = ctk.CTkLabel(master=self.thisTab, text="")
        self.infoLabel.pack()

        evaluateButton = ctk.CTkButton(
            master=self.thisTab,
            text="Evaluate",
            command=self.StartEvaluate
        )
        evaluateButton.pack()

    def StartEvaluate(self):
        self.Refresh()
        threading.Thread(target=self.Evaluate).start()

    def Evaluate(self):
        self.infoLabel.configure(text="")
        modelName = self.modelNameEntry.get()
        upperModelName = modelName.upper()

        if modelName.find("/") != -1:
            upperModelName = modelName.split("/")[1].upper()

        happy_gen = HappyGeneration(upperModelName, modelName, load_path=self.modelPath)
        result = happy_gen.eval(self.databaseName)
        self.infoLabel.configure(text=f"Evaluation Score : {result.loss}")

    def ChooseDataset(self):
        self.databaseName = filedialog.askopenfilename(initialdir=os.getcwd())
        self.datasetLabel.configure(text=self.databaseName)
    
    def ChooseModel(self):
        self.modelPath = filedialog.askdirectory(initialdir=os.getcwd(), mustexist=True)
        self.modelLabel.configure(text=self.modelPath)

    def Refresh(self):
        self.parentWindow.update()
        self.parentWindow.after(1000, self.Refresh)