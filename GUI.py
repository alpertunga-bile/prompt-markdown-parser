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
    parser = Parser()

    def __init__(self):
        """
        //////////////////////////////////////////////////////////////////////////////////////////////
        // Initialize Window
        //////////////////////////////////////////////////////////////////////////////////////////////
        """
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.window = ctk.CTk()
        self.window.title("Markdown Prompt Parser")
        self.window.geometry("600x400")

        """
        //////////////////////////////////////////////////////////////////////////////////////////////
        // Change Appearance
        //////////////////////////////////////////////////////////////////////////////////////////////
        """

        iconImage = ctk.CTkImage(light_image=Image.open("icons/light_icon.png"),
                                dark_image=Image.open("icons/dark_icon.png"),
                                size=(30, 30))

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

        """
        //////////////////////////////////////////////////////////////////////////////////////////////
        // Translation Variables
        //////////////////////////////////////////////////////////////////////////////////////////////
        """
        self.parser.translatorName = ctk.StringVar(value='Google')
        translatorCombobox = ctk.CTkComboBox(
            master=self.window,
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
        translatorCombobox.pack()

        self.parser.translateValue = tk.IntVar()
        translateCheckButton = ctk.CTkCheckBox(
            master=self.window,
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

        tempPath = os.path.join(os.getcwd(), "prompts")

        fastButton = ctk.CTkButton(
            master=self.window,
            text="Parse All Files In 'prompts' Folder",
            command=self.ParseAllFiles
        )
        fastButton.pack(pady=10)

        """
        //////////////////////////////////////////////////////////////////////////////////////////////
        // Select Markdown Files
        //////////////////////////////////////////////////////////////////////////////////////////////
        """
        self.startFrame = ctk.CTkFrame(master=self.window)

        directoryLabel = ctk.CTkLabel(master=self.startFrame, text=f"{tempPath}")
        directoryLabel.grid(column=0, row=0, padx=(0, 50), ipady=5, pady=10)

        selectButton = ctk.CTkButton(
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
    
    """
    Refresh The GUI Application
    """
    def Refresh(self):
        self.window.update()
        self.window.after(1000, self.Refresh)

    """
    Run Parse And Save function in new thread
    """
    def Parse(self):
        self.Refresh()
        threading.Thread(target=self.parser.Run).start()

    """
    Run ParseAllFiles function in new thread
    """
    def ParseAllFiles(self):
        self.Refresh()
        threading.Thread(target=self.parser.ParseAllFiles).start()

    """
    Change Appearance based on the button click
    """
    def ChangeAppearance(self):
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")
    
    def Loop(self):
        self.window.mainloop()