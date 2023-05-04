from os import getcwd
from threading import Thread

class EvaluateTab:
    parentWindow = None
    thisTab = None

    variableFrame = None
    modelNameEntry = None
    databaseName = getcwd()
    modelPath = getcwd()
    datasetLabel = None
    modelLabel = None

    infoLabel = None

    def __init__(self, parent, tab):
        from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton

        self.parentWindow = parent
        self.thisTab = tab

        self.variableFrame = CTkFrame(master=self.thisTab)

        modelNameLabel = CTkLabel(master=self.variableFrame, text="Model Name")
        self.modelNameEntry = CTkEntry(master=self.variableFrame, placeholder_text="E.g. gpt2")

        self.datasetLabel = CTkLabel(master=self.variableFrame, text=self.databaseName)

        selectDatasetButton = CTkButton(
            master=self.variableFrame,
            text="Choose Dataset",
            command=self.ChooseDataset
        )

        self.modelLabel = CTkLabel(master=self.variableFrame, text=self.modelPath)

        selectModelButton = CTkButton(
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

        self.infoLabel = CTkLabel(master=self.thisTab, text="")
        self.infoLabel.pack()

        evaluateButton = CTkButton(
            master=self.thisTab,
            text="Evaluate",
            command=self.StartEvaluate
        )
        evaluateButton.pack()

    def StartEvaluate(self):
        self.Refresh()
        Thread(target=self.Evaluate).start()

    def Evaluate(self):
        self.infoLabel.configure(text="")
        modelName = self.modelNameEntry.get()
        upperModelName = modelName.upper()

        if modelName.find("/") != -1:
            upperModelName = modelName.split("/")[1].upper()

        from happytransformer import HappyGeneration

        happy_gen = HappyGeneration(upperModelName, modelName, load_path=self.modelPath)
        result = happy_gen.eval(self.databaseName)
        self.infoLabel.configure(text=f"Evaluation Score : {result.loss}")

    def ChooseDataset(self):
        from tkinter.filedialog import askopenfilename

        self.databaseName = askopenfilename(initialdir=getcwd())
        self.datasetLabel.configure(text=self.databaseName)
    
    def ChooseModel(self):
        from tkinter.filedialog import askdirectory

        self.modelPath = askdirectory(initialdir=getcwd(), mustexist=True)
        self.modelLabel.configure(text=self.modelPath)

    def Refresh(self):
        self.parentWindow.update()
        self.parentWindow.after(1000, self.Refresh)