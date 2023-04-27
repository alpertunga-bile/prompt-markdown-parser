from tkinter import filedialog
import os
from glob import glob
from deep_translator import GoogleTranslator

class Parser:
    promptFiles = None
    textLabel = None
    directoryLabel = None
    translateValue = None
    progressBar = None

    def SelectDirectory(self):
        self.promptFiles = filedialog.askopenfilenames(initialdir=os.getcwd())
        text = "1 file is selected" if len(self.promptFiles) == 1 else f"{len(self.promptFiles)} files are selected"
        self.directoryLabel.configure(text=text)

    def ParseAllFiles(self):
        fastPath = os.path.join(os.getcwd(), "prompts")
        if(os.path.exists(fastPath) == False):
            self.textLabel.configure(text="There is no folder named 'prompts'")
            return
        self.promptFiles = glob(f"{fastPath}\*.md")
        self.textLabel.configure(text=f"{self.promptFiles.count} files are found ...")
        self.Run()

    def Run(self):
        if self.promptFiles is None:
            self.textLabel.configure(text=f"Please Select At Least One File")
            return
        self.progressBar.set(0)
        self.progressBar.pack(ipadx=100, pady=10)
        parsedFileCount = 0
        totalPromptFiles = len(self.promptFiles)
        for promptFile in self.promptFiles:
            if(os.path.exists(promptFile) == False):
                self.textLabel.configure(text=f"{promptFile} is not exists | Skipping ...")
                continue
            text = f"Parsing {promptFile}"
            self.textLabel.configure(text=text)
            self.ParseAndSave(promptFile)
            text = f"{text}   DONE!!!"
            parsedFileCount = parsedFileCount + 1
            self.progressBar.set(float(parsedFileCount) / float(totalPromptFiles))
            self.textLabel.configure(text=text)
        
        if parsedFileCount == 1:
            text = "1 file is Parsed!!! Happy Prompting!!!"
        elif parsedFileCount > 1:
            text = f"{parsedFileCount} files are Parsed!!! Happy Prompting!!!"
        else:
            text = "0 file is Parsed!!! Please Select At Least One File"

        self.textLabel.configure(text=text)
        self.progressBar.pack_forget()

    def Preprocess(self, line):
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

        if self.translateValue.get():
            line = GoogleTranslator(source='auto', target='en').translate(line)

        return line

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

            line = self.Preprocess(line)

            line = line + ", "

            if isPositive:
                positiveStr = positiveStr + line
            else:
                negativeStr = negativeStr + line

        positiveStr = positiveStr[:-2]
        negativeStr = negativeStr[:-2]

        positiveFile = open(positiveFilename, "w")
        negativeFile = open(negativeFilename, "w")

        positiveFile.write(positiveStr)
        negativeFile.write(negativeStr)

        positiveFile.close()
        negativeFile.close()