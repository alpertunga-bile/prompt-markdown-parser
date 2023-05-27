from os import getcwd
from threading import Thread

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
    generatorPath = getcwd()
    generatorPathLabel = None
    generatorEntry = None
    seedEntry = None
    generatorTextbox = None
    recursiveSlider = None
    recursiveLabel = None
    selfRecursiveIntVar = None
    selfRecursiveCheckbox = None

    def __init__(self, parent, tab):
        from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkCheckBox, CTkTextbox, CTkSlider
        from tkinter import IntVar

        self.parentWindow = parent
        self.thisTab = tab

        self.variableFrame = CTkFrame(self.thisTab)

        generatorNameLabel = CTkLabel(master=self.variableFrame, text="Model Name")
        self.generatorEntry = CTkEntry(master=self.variableFrame, placeholder_text="E.g. gpt2")
        self.generatorPathLabel = CTkLabel(master=self.variableFrame, text=self.generatorPath)
        
        chooseGenerator = CTkButton(
            master=self.variableFrame,
            text="Choose Model",
            command=self.ChooseGenerator
        )

        minLengthLabel = CTkLabel(master=self.variableFrame, text="Minimum number of generated tokens")
        self.minLengthEntry = CTkEntry(master=self.variableFrame, placeholder_text="10")

        maxLengthLabel = CTkLabel(master=self.variableFrame, text="Maximum number of generated tokens")
        self.maxLengthEntry = CTkEntry(master=self.variableFrame, placeholder_text="50")

        self.doSampleIntVar = IntVar()
        self.doSampleCheckbox = CTkCheckBox(
            master=self.variableFrame,
            text='When checked, picks words based on their conditional probability',
            variable=self.doSampleIntVar,
            onvalue=1,
            offvalue=0
        )

        self.earlyStoppingCheckboxIntVar = IntVar()
        self.earlyStoppingCheckbox = CTkCheckBox(
            master=self.variableFrame,
            text='When checked, generation finishes if the EOS token is reached',
            variable=self.earlyStoppingCheckboxIntVar,
            onvalue=1,
            offvalue=0
        )

        self.seedEntry = CTkEntry(master=self.thisTab, placeholder_text="Enter Your Seed e.g. goddess", width=400)

        self.generatorTextbox = CTkTextbox(
            master=self.thisTab,
            width=500,
            height=200
        )

        self.recursiveLabel = CTkLabel(master=self.variableFrame, text="Recursive Level : 0")
        self.recursiveSlider = CTkSlider(
            master=self.variableFrame,
            width=400,
            from_=0,
            to=10,
            number_of_steps=10,
            command=self.SliderEvent
        )
        self.recursiveSlider.set(0)

        self.selfRecursiveIntVar = IntVar()
        self.selfRecursiveCheckbox = CTkCheckBox(
            master=self.thisTab,
            text="Self Recursive",
            variable=self.selfRecursiveIntVar,
            onvalue=1,
            offvalue=0
        )

        generatorNameLabel.grid(column=0, row=0, padx=(0, 50), ipady=5, pady=10)
        self.generatorEntry.grid(column=1, row=0)
        self.generatorPathLabel.grid(column=0, row=1, padx=(0, 50), ipady=5, pady=10)
        chooseGenerator.grid(column=1, row=1)
        minLengthLabel.grid(column=0, row=2, padx=(0, 50), ipady=5, pady=10)
        self.minLengthEntry.grid(column=1, row=2)
        maxLengthLabel.grid(column=0, row=3, padx=(0, 50), ipady=5, pady=10)
        self.maxLengthEntry.grid(column=1, row=3)
        self.doSampleCheckbox.grid(column=0, row=4, padx=(0, 50), ipady=5, pady=10)
        self.earlyStoppingCheckbox.grid(column=1, row=4,)
        self.recursiveLabel.grid(column=0, row=5, padx=(0, 50), ipady=5, pady=10)
        self.recursiveSlider.grid(column=1, row=5)

        self.variableFrame.pack()

        self.selfRecursiveCheckbox.pack(pady=10)
        self.seedEntry.pack(pady=10)
        self.generatorTextbox.pack(pady=10)

        generateButton = CTkButton(
            master=self.thisTab,
            text="Generate Text",
            command=self.StartGenerate
        )

        generateButton.pack()

    def ChooseGenerator(self):
        from tkinter.filedialog import askdirectory

        self.generatorPath = askdirectory(initialdir=getcwd(), mustexist=True)
        self.generatorPathLabel.configure(text=self.generatorPath)

    def StartGenerate(self):
        self.Refresh()
        Thread(target=self.Generate).start()

    def RemoveDuplicates(self, line):
        uniqueList = []
        [uniqueList.append(x) for x in line if x not in uniqueList]
        return uniqueList

    def Preprocess(self, line):
        tempLine = line.replace("\n", ", ")
        tempLine = tempLine.replace("  ", " ")
        tempLine = tempLine.replace("\t", " ")
        tempLine = tempLine.replace(",,", ",")
        tempLine = tempLine.replace(",, ", ", ")

        tempLine = ''.join(self.RemoveDuplicates(tempLine.split(",")))

        return tempLine

    def Generate(self):
        self.generatorTextbox.delete("0.0", "end")
        seed = "mature woman" if self.seedEntry.get() == "" else self.seedEntry.get()
        minLength = 10 if self.minLengthEntry.get() == "" else int(self.minLengthEntry.get())
        maxLength = 50 if self.maxLengthEntry.get() == "" else int(self.maxLengthEntry.get())
        doSample = True if self.doSampleIntVar.get() == 1 else False
        earlyStopping = True if self.earlyStoppingCheckboxIntVar.get() == 1 else False
        recursiveLevel = int(self.recursiveSlider.get())
        selfRecursive = True if self.selfRecursiveIntVar.get() == 1 else False

        from happytransformer import HappyGeneration, GENSettings

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

        generatedText = self.Preprocess(result.text)

        if selfRecursive:
            for _ in range(0, recursiveLevel):
                result = happy_gen.generate_text(generatedText, generatorArgs)
                generatedText = self.Preprocess(result.text)
            generatedText = self.Preprocess(seed + generatedText)
        else:
            for _ in range(0, recursiveLevel):
                result = happy_gen.generate_text(generatedText, generatorArgs)
                generatedText += result.text
                generatedText = self.Preprocess(generatedText)

        self.generatorTextbox.insert("0.0", generatedText)
    
    def SliderEvent(self, value):
        self.recursiveLabel.configure(text=f"Recursive Level : {int(self.recursiveSlider.get())}")

    def Refresh(self):
        self.parentWindow.update()
        self.parentWindow.after(1000, self.Refresh)
