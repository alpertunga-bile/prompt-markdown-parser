from os import getcwd
from os.path import join
import threading

from happytransformer import HappyGeneration, GENTrainArgs


class TrainTab:
    parentWindow = None
    thisTab = None

    trainName = getcwd()
    datasetLabel = None

    variableFrame = None
    modelNameEntry = None
    epochsEntry = None
    batchEntry = None
    modelFolderEntry = None

    infoLabel = None

    def __init__(self, parent, tab):
        from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton

        self.parentWindow = parent
        self.thisTab = tab

        self.variableFrame = CTkFrame(master=self.thisTab)

        modelNameLabel = CTkLabel(master=self.variableFrame, text="Model Name")
        self.modelNameEntry = CTkEntry(
            master=self.variableFrame, placeholder_text="E.g. gpt2"
        )
        epochsLabel = CTkLabel(master=self.variableFrame, text="Epochs")
        self.epochsEntry = CTkEntry(master=self.variableFrame, placeholder_text="10")
        batchSizeLabel = CTkLabel(master=self.variableFrame, text="Batch Size")
        self.batchEntry = CTkEntry(master=self.variableFrame, placeholder_text="1")
        modelFolderLabel = CTkLabel(master=self.variableFrame, text="Model Folder Name")
        self.modelFolderEntry = CTkEntry(
            master=self.variableFrame, placeholder_text="E.g. positive_model", width=160
        )

        self.datasetLabel = CTkLabel(master=self.variableFrame, text=self.trainName)

        selectDatasetButton = CTkButton(
            master=self.variableFrame, text="Choose Dataset", command=self.ChooseDataset
        )

        modelNameLabel.grid(column=0, row=0, padx=(0, 50), ipady=5, pady=10)
        self.modelNameEntry.grid(column=1, row=0)
        epochsLabel.grid(column=0, row=1, padx=(0, 50), ipady=5, pady=10)
        self.epochsEntry.grid(column=1, row=1)
        batchSizeLabel.grid(column=0, row=2, padx=(0, 50), ipady=5, pady=10)
        self.batchEntry.grid(column=1, row=2)
        modelFolderLabel.grid(column=0, row=3, padx=(0, 50), ipady=5, pady=10)
        self.modelFolderEntry.grid(column=1, row=3)
        self.datasetLabel.grid(column=0, row=4, padx=(0, 50), ipady=5, pady=10)
        selectDatasetButton.grid(column=1, row=4)

        self.variableFrame.pack()

        self.infoLabel = CTkLabel(master=self.thisTab, text="")
        self.infoLabel.pack()

        trainButton = CTkButton(
            master=self.thisTab, text="Train", command=self.StartTrain
        )
        trainButton.pack(pady=10)

    def ChooseDataset(self):
        from tkinter.filedialog import askopenfilename

        self.trainName = askopenfilename(initialdir=getcwd())
        self.datasetLabel.configure(text=self.trainName)

    def StartTrain(self):
        self.Refresh()
        threading.Thread(target=self.Train).start()

    def Train(self):
        self.infoLabel.configure(text="")
        modelName = self.modelNameEntry.get()
        upperModelName = modelName.upper()

        if modelName.find("/") != -1:
            upperModelName = modelName.split("/")[1].upper()

        epochs = 10 if self.epochsEntry.get() == "" else int(self.epochsEntry.get())
        batchSize = 1 if self.batchEntry.get() == "" else int(self.batchEntry.get())
        modelFolder = self.modelFolderEntry.get()

        happy_gen = HappyGeneration(upperModelName, modelName)
        args = GENTrainArgs(num_train_epochs=epochs, batch_size=batchSize)
        happy_gen.train(self.trainName, args=args)
        happy_gen.save(join("dataset", modelFolder))
        self.infoLabel.configure(text="DONE!!!")

    def Refresh(self):
        self.parentWindow.update()
        self.parentWindow.after(1000, self.Refresh)
