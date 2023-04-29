import os
import customtkinter as ctk
import threading
from tkinter import filedialog, IntVar
from happytransformer import HappyGeneration, GENSettings

class GenerateTab:
    parentWindow = None
    thisTab = None

    variableFrame = None

    minLengthEntry = None
    maxLengthEntry = None
    doSampleCheckbox = None
    doSampleIntVar = None
    earlyStoppingCheckbox = None
    earlyStoppingCheckboxIntVar = None
    generatorPath = os.getcwd()
    generatorPathLabel = None
    generatorEntry = None
    seedEntry = None
    generatorTextbox = None
    recursiveSlider = None
    recursiveLabel = None

    def __init__(self, parent, tab):
        self.parentWindow = parent
        self.thisTab = tab

        self.variableFrame = ctk.CTkFrame(self.thisTab)

        generatorNameLabel = ctk.CTkLabel(master=self.variableFrame, text="Model Name")
        self.generatorEntry = ctk.CTkEntry(master=self.variableFrame, placeholder_text="Enter Model Name")
        self.generatorPathLabel = ctk.CTkLabel(master=self.variableFrame, text=self.generatorPath)
        
        chooseGenerator = ctk.CTkButton(
            master=self.variableFrame,
            text="Choose Model",
            command=self.ChooseGenerator
        )

        minLengthLabel = ctk.CTkLabel(master=self.variableFrame, text="Minimum number of generated tokens")
        self.minLengthEntry = ctk.CTkEntry(master=self.variableFrame, placeholder_text="Enter Min Length")

        maxLengthLabel = ctk.CTkLabel(master=self.variableFrame, text="Maximum number of generated tokens")
        self.maxLengthEntry = ctk.CTkEntry(master=self.variableFrame, placeholder_text="Enter Max Length")

        self.doSampleIntVar = IntVar()
        self.doSampleCheckbox = ctk.CTkCheckBox(
            master=self.thisTab,
            text='When True, picks words based on their conditional probability',
            variable=self.doSampleIntVar,
            onvalue=1,
            offvalue=0
        )

        self.earlyStoppingCheckboxIntVar = IntVar()
        self.earlyStoppingCheckbox = ctk.CTkCheckBox(
            master=self.thisTab,
            text='When True, generation finishes if the EOS token is reached',
            variable=self.earlyStoppingCheckboxIntVar,
            onvalue=1,
            offvalue=0
        )

        self.seedEntry = ctk.CTkEntry(master=self.thisTab, placeholder_text="Enter Your Seed", width=400)

        self.generatorTextbox = ctk.CTkTextbox(
            master=self.thisTab,
            width=400,
            height=200
        )

        self.recursiveLabel = ctk.CTkLabel(master=self.thisTab, text="Recursive Level : 0")
        self.recursiveSlider = ctk.CTkSlider(
            master=self.thisTab,
            width=400,
            from_=0,
            to=10,
            number_of_steps=10,
            command=self.SliderEvent
        )
        self.recursiveSlider.set(0)

        generatorNameLabel.grid(column=0, row=0, padx=(0, 50), ipady=5, pady=10)
        self.generatorEntry.grid(column=1, row=0)
        self.generatorPathLabel.grid(column=0, row=1, padx=(0, 50), ipady=5, pady=10)
        chooseGenerator.grid(column=1, row=1)
        minLengthLabel.grid(column=0, row=2, padx=(0, 50), ipady=5, pady=10)
        self.minLengthEntry.grid(column=1, row=2)
        maxLengthLabel.grid(column=0, row=3, padx=(0, 50), ipady=5, pady=10)
        self.maxLengthEntry.grid(column=1, row=3)
        
        self.variableFrame.pack()

        self.doSampleCheckbox.pack(pady=10)
        self.earlyStoppingCheckbox.pack(pady=10)
        self.recursiveLabel.pack(pady=10)
        self.recursiveSlider.pack(pady=10)
        self.seedEntry.pack(pady=10)
        self.generatorTextbox.pack(pady=10)

        generateButton = ctk.CTkButton(
            master=self.thisTab,
            text="Generate Text",
            command=self.StartGenerate
        )

        generateButton.pack()

    def ChooseGenerator(self):
        self.generatorPath = filedialog.askdirectory(initialdir=os.getcwd, mustexist=True)
        self.generatorPathLabel.configure(text=self.generatorPath)

    def StartGenerate(self):
        self.Refresh()
        threading.Thread(target=self.Generate).start()

    def Generate(self):
        seed = "mature woman" if self.seedEntry.get() == "" else self.seedEntry.get()
        minLength = 10 if self.minLengthEntry.get() == "" else int(self.minLengthEntry.get())
        maxLength = 50 if self.maxLengthEntry.get() == "" else int(self.maxLengthEntry.get())
        doSample = True if self.doSampleIntVar.get() == 1 else False
        earlyStopping = True if self.earlyStoppingCheckboxIntVar.get() == 1 else False
        recurseLevel = int(self.recursiveSlider.get())

        generatorArgs = GENSettings(
            min_length=minLength,
            max_length=maxLength,
            do_sample=doSample,
            early_stopping=earlyStopping
        )

        modelName = self.generatorEntry.get()
        upperModelName = modelName.upper()

        if modelName.find("/") != -1:
            upperModelName = modelName.split("/")[1].upper()

        happy_gen = HappyGeneration(upperModelName, modelName, load_path=self.generatorPath)
        result = happy_gen.generate_text(seed, generatorArgs)

        if recurseLevel == 0:
            self.generatorTextbox.insert("0.0", result.text)
            return

        for _ in range(0, recurseLevel):
            result = happy_gen.generate_text(result.text, generatorArgs)

        self.generatorTextbox.insert("0.0", result.text)
    
    def SliderEvent(self, value):
        self.recursiveLabel.configure(text=f"Recursive Level : {int(self.recursiveSlider.get())}")

    def Refresh(self):
        self.parentWindow.update()
        self.parentWindow.after(1000, self.Refresh)