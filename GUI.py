import customtkinter as ctk
from PIL import Image

from ParseTab import ParseTab
from DatasetTab import DatasetTab
from TrainTab import TrainTab
from EvaluateTab import EvaluateTab
from GenerateTab import GenerateTab

class GUI:
    window = None
    
    tabview = None
    parseTab = None
    datasetTab = None
    trainTab = None
    evaluateTab = None
    generateTab = None

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
        self.window.geometry("600x500")

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
        // Create TabView
        //////////////////////////////////////////////////////////////////////////////////////////////
        """
        self.tabview = ctk.CTkTabview(self.window, width=500, height = 300)

        self.parseTab = ParseTab(self.window, self.tabview.add("Parse"))
        self.datasetTab = DatasetTab(self.window, self.tabview.add("Dataset"))
        self.trainTab = TrainTab(self.window, self.tabview.add("Train"))
        self.evaluateTab = EvaluateTab(self.window, self.tabview.add("Evaluate"))
        self.generateTab = GenerateTab(self.window, self.tabview.add("Generate"))

        self.tabview.set("Parse")
        self.tabview.pack(side=ctk.TOP, anchor=ctk.N)

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