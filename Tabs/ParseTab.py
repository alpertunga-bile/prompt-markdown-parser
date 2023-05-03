from os.path import join
from os import getcwd
from tkinter import IntVar
from customtkinter import StringVar, CTkCheckBox, CTkComboBox, CTkFrame, CTkLabel, CTkButton, CTkProgressBar
from threading import Thread
from Parser import Parser

class ParseTab:
    parentWindow = None
    thisTab = None
    startFrame = None
    initializeFrame = None
    parser = Parser()

    def __init__(self, parent, tab):
        self.parentWindow = parent
        self.thisTab = tab
        
        """
        //////////////////////////////////////////////////////////////////////////////////////////////
        // Translation Variables
        //////////////////////////////////////////////////////////////////////////////////////////////
        """
        self.parser.translatorName = StringVar(value='Google')
        translatorCombobox = CTkComboBox(
            master=self.thisTab,
            width=150,
            variable=self.parser.translatorName,
            state='readonly',
            values=[
                'Google',
                'Mymemory',
                'Linguee',
                'PONS'
            ]
        )
        translatorCombobox.pack(pady=10)

        self.parser.translateValue = IntVar()
        translateCheckButton = CTkCheckBox(
            master=self.thisTab,
            text='Translate Prompts',
            variable=self.parser.translateValue,
            onvalue=1,
            offvalue=0
        )
        translateCheckButton.pack(pady=20)

        """
        //////////////////////////////////////////////////////////////////////////////////////////////
        // Parse All Files
        //////////////////////////////////////////////////////////////////////////////////////////////
        """

        tempPath = join(getcwd(), "prompts")

        fastButton = CTkButton(
            master=self.thisTab,
            text="Parse All Files In 'prompts' Folder",
            command=self.ParseAllFiles
        )
        
        fastButton.pack(pady=10)

        """
        //////////////////////////////////////////////////////////////////////////////////////////////
        // Select Markdown Files
        //////////////////////////////////////////////////////////////////////////////////////////////
        """
        self.startFrame = CTkFrame(master=self.thisTab)

        directoryLabel = CTkLabel(master=self.startFrame, text=f"{tempPath}")
        directoryLabel.grid(column=0, row=0, padx=(0, 50), ipady=5, pady=10)

        selectButton = CTkButton(
            master=self.startFrame,
            text="Select Prompt Files",
            command=self.parser.SelectDirectory
        )
        selectButton.grid(column=1, row=0)

        self.startFrame.pack()
        self.parser.directoryLabel = directoryLabel

        """
        //////////////////////////////////////////////////////////////////////////////////////////////
        // Parse And Save Selected Files
        //////////////////////////////////////////////////////////////////////////////////////////////
        """

        self.initializeFrame = CTkFrame(master=self.thisTab)

        initializeButton = CTkButton(
            master=self.initializeFrame,
            text="Parse And Save",
            command=self.Parse
        )

        informationLabel = CTkLabel(master=self.initializeFrame, text="")

        progressBar = CTkProgressBar(
            master=self.initializeFrame,
            orientation='horizontal',
            mode='determinate'
        )
        progressBar.set(0)

        initializeButton.pack(pady=10)
        informationLabel.pack(pady=10)
        progressBar.pack_forget()
        self.initializeFrame.pack()

        self.parser.textLabel = informationLabel
        self.parser.progressBar = progressBar


    def Refresh(self):
        self.parentWindow.update()
        self.parentWindow.after(1000, self.Refresh)

    """
    Run Parse And Save function in new thread
    """
    def Parse(self):
        self.Refresh()
        Thread(target=self.parser.Run).start()

    """
    Run ParseAllFiles function in new thread
    """
    def ParseAllFiles(self):
        self.Refresh()
        Thread(target=self.parser.ParseAllFiles).start()