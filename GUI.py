import tkinter as tk
from Parser import Parser
import os

class GUI:
    window = None
    startFrame = None
    initializeFrame = None
    parser = Parser()

    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("600x120")

        tempPath = os.path.join(os.getcwd(), "test")

        initializeButton = tk.Button(
            master=self.window,
            text="Fast Parse",
            command=self.parser.Fast
        )

        initializeButton.pack()

        self.startFrame = tk.Frame()

        directoryLabel = tk.Label(master=self.startFrame, text=f"{tempPath}")
        directoryLabel.grid(column=0, row=0, padx=(0, 50), ipady=5)

        selectButton = tk.Button(
            master=self.startFrame,
            text="Select Prompt Files",
            command=self.parser.SelectDirectory
        )

        selectButton.grid(column=1, row=0)

        self.startFrame.pack()

        self.parser.directoryLabel = directoryLabel

        initializeFrame = tk.Frame()

        initializeButton = tk.Button(
            master=initializeFrame,
            text="Parse And Save",
            command=self.parser.Run
        )

        informationLabel = tk.Label(master=self.initializeFrame, text="")

        initializeButton.pack()
        informationLabel.pack(pady=10)
        initializeFrame.pack()

        self.parser.textLabel = informationLabel
    
    def Loop(self):
        self.window.mainloop()