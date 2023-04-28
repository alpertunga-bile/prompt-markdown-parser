import tkinter as tk
import customtkinter as ctk
import threading
import os
from PIL import Image

from Parser import Parser

class GUI:
    window = None
    startFrame = None
    initializeFrame = None
    debugLabel = None
    parser = Parser()

    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.window = ctk.CTk()
        self.window.title("Markdown Prompt Parser")
        self.window.geometry("600x400")

        iconImage = ctk.CTkImage(light_image=Image.open("icons/light_icon.png"),
                                dark_image=Image.open("icons/dark_icon.png"),
                                size=(30, 30))

        """
        self.debugLabel = ctk.CTkLabel(self.window, text="")
        self.debugLabel.pack()
        """

        appearanceChangeButton = ctk.CTkButton(
            self.window,
            width=30,
            height=30,
            image=iconImage,
            text="",
            fg_color="gray",
            command=self.ChangeAppearance
        )
        appearanceChangeButton.pack(side=ctk.TOP, anchor=ctk.NW)

        self.parser.translateValue = tk.IntVar()
        translateCheckButton = ctk.CTkCheckBox(
            master=self.window,
            text='Translate Prompts',
            variable=self.parser.translateValue,
            onvalue=1,
            offvalue=0
        )
        translateCheckButton.pack(pady=20)

        tempPath = os.path.join(os.getcwd(), "prompts")

        fastButton = ctk.CTkButton(
            master=self.window,
            text="Parse All Files In 'prompts' Folder",
            command=self.ParseAllFiles
        )
        fastButton.pack(pady=30)

        self.startFrame = ctk.CTkFrame(master=self.window)

        directoryLabel = ctk.CTkLabel(master=self.startFrame, text=f"{tempPath}")
        directoryLabel.grid(column=0, row=0, padx=(0, 50), ipady=5)

        selectButton = ctk.CTkButton(
            master=self.startFrame,
            text="Select Prompt Files",
            command=self.parser.SelectDirectory
        )
        selectButton.grid(column=1, row=0)

        self.startFrame.pack()

        self.parser.directoryLabel = directoryLabel

        initializeFrame = ctk.CTkFrame(master=self.window)

        initializeButton = ctk.CTkButton(
            master=initializeFrame,
            text="Parse And Save",
            command=self.Parse
        )

        informationLabel = ctk.CTkLabel(master=self.initializeFrame, text="")

        progressBar = ctk.CTkProgressBar(
            master=self.initializeFrame,
            orientation='horizontal',
            mode='determinate'
        )
        progressBar.set(0)

        initializeButton.pack(pady=10)
        informationLabel.pack(pady=10)
        progressBar.pack_forget()
        initializeFrame.pack()

        self.parser.textLabel = informationLabel
        self.parser.progressBar = progressBar
    
    def Refresh(self):
        self.window.update()
        self.window.after(1000, self.Refresh)

    def Parse(self):
        self.Refresh()
        threading.Thread(target=self.parser.Run).start()

    def ParseAllFiles(self):
        self.Refresh()
        threading.Thread(target=self.parser.ParseAllFiles).start()

    def ChangeAppearance(self):
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")
    
    def Loop(self):
        self.window.mainloop()