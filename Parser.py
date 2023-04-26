from tkinter import filedialog
from tkinter import messagebox
import os
from glob import glob

class Parser:
    promptFiles = None
    textLabel = None
    directoryLabel = None

    def SelectDirectory(self):
        self.promptFiles = filedialog.askopenfilenames(initialdir=os.getcwd())
        while len(self.promptFiles) == 0:
            messagebox.showerror(message="You dont select any markdown file! Please select at least one file to proceed")
            self.promptFiles = filedialog.askopenfilenames(initialdir=os.getcwd())
        text = "1 file is selected" if len(self.promptFiles) == 1 else f"{len(self.promptFiles)} files are selected"
        self.directoryLabel.config(text=text)

    def Fast(self):
        fastPath = os.path.join(os.getcwd(), "test")
        self.promptFiles = glob(f"{fastPath}\*.md")
        self.Run()
        exit(0)

    def Run(self):       
        for promptFile in self.promptFiles:
            text = f"Parsing {promptFile} ..."
            self.textLabel.config(text=text)
            self.ParseAndSave(promptFile)
            text = f"{text}   DONE!!!"
            self.textLabel.config(text=text)
        
        text = "1 file is Parsed!!! Happy Prompting!!!" if len(self.promptFiles) == 1 else f"{len(self.promptFiles)} files are Parsed!!! Happy Prompting!!!"
        self.textLabel.config(text=text)

    def ParseAndSave(self, promptFile):
        file = open(promptFile, "r")
        lines = file.readlines()
        file.close()

        filename = os.path.splitext(promptFile)[0]
        
        positiveFilename = f"{filename}_positive.txt"
        negativeFilename = f"{filename}_negative.txt"

        positiveStr = ""
        negativeStr = ""

        isPositive = True
        for line in lines:
            if line.find("Positive Prompts") != -1:
                isPositive = True
            elif line.find("Negative Prompts") != -1:
                isPositive = False
            
            if line.startswith("#") or line == "\n" or line.startswith("---") or line == '  \n':
                continue

            if line.startswith("- [ ] ") or line.startswith("- [x] "):
                line = line[6:]
            elif line.startswith("-[ ] ") or line.startswith("-[x] "):
                line = line[5:]
            elif line.startswith("-[] "):
                line = line[4:]
            elif line.startswith("- ") or line.startswith("> "):
                line = line[2:]
                
            if line.endswith("\n"):
                line = line[:-1]

            line = line + ","

            if isPositive:
                positiveStr = positiveStr + line
            else:
                negativeStr = negativeStr + line

        positiveStr = positiveStr[:-1]
        negativeStr = negativeStr[:-1]

        positiveFile = open(positiveFilename, "w")
        negativeFile = open(negativeFilename, "w")

        positiveFile.write(positiveStr)
        negativeFile.write(negativeStr)

        positiveFile.close()
        negativeFile.close()