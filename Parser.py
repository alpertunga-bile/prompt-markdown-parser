from tkinter import filedialog
import os
from glob import glob
from deep_translator import GoogleTranslator, MyMemoryTranslator, LingueeTranslator, PonsTranslator

class Parser:
    promptFiles = None
    textLabel = None
    directoryLabel = None
    
    translateValue = None
    translator = None
    translatorName = None

    progressBar = None
    isTranslate = False

    """
    Select Markdown Files
    """
    def SelectDirectory(self):
        self.promptFiles = filedialog.askopenfilenames(initialdir=os.getcwd())
        text = "1 file is selected" if len(self.promptFiles) == 1 else f"{len(self.promptFiles)} files are selected"
        self.directoryLabel.configure(text=text)

    """
    Parse All Files in 'prompts' folder
    """
    def ParseAllFiles(self):
        fastPath = os.path.join(os.getcwd(), "prompts")
        if(os.path.exists(fastPath) == False):
            self.textLabel.configure(text="There is no folder named 'prompts'")
            return
        self.promptFiles = glob(f"{fastPath}\*.md")
        self.textLabel.configure(text=f"{self.promptFiles.count} files are found ...")
        self.Run()

    """
    Select translator if 'Translate Prompts' checkbox is checked
    """
    def SelectTranslator(self):
        if self.isTranslate == False:
            return
        
        translatorName = self.translatorName.get()
        if translatorName == 'Google':
            self.translator = GoogleTranslator(source='auto', target='en')
        elif translatorName == 'Mymemory':
            self.translator = MyMemoryTranslator(source='auto', target='en')
        elif translatorName == 'Linguee':
            self.translator = LingueeTranslator(source='auto', target='english')
        elif translatorName == "PONS":
            self.translator = PonsTranslator(source='auto', target='en')

    """
    Run the parsing
    """
    def Run(self):
        """
        Check if there are no files selected
        """
        if self.promptFiles is None:
            self.textLabel.configure(text=f"Please Select At Least One File")
            return
        
        """
        Set progressbar variables
        """
        self.progressBar.set(0)
        self.progressBar.pack(ipadx=100, pady=10)
        parsedFileCount = 0
        totalPromptFiles = len(self.promptFiles)
        
        """
        Choose translator if it is going to be used
        """
        self.isTranslate = True if self.translateValue.get() else False
        self.SelectTranslator()
        
        for promptFile in self.promptFiles:
            if(os.path.exists(promptFile) == False):
                self.textLabel.configure(text=f"{promptFile} is not exists | Skipping ...")
                continue
            
            text = f"Parsing {promptFile}"
            self.textLabel.configure(text=text)
            self.ParseAndSave(promptFile)
            text = f"{text}   DONE!!!"
            self.textLabel.configure(text=text)

            """
            Update progressbar for every iteration
            """
            parsedFileCount = parsedFileCount + 1
            self.progressBar.set(float(parsedFileCount) / float(totalPromptFiles))
        
        if parsedFileCount == 1:
            text = "1 file is Parsed!!! Happy Prompting!!!"
        elif parsedFileCount > 1:
            text = f"{parsedFileCount} files are Parsed!!! Happy Prompting!!!"
        else:
            text = "0 file is Parsed!!! Please Select At Least One File"

        self.textLabel.configure(text=text)
        self.progressBar.pack_forget()
    
    """
    Preprocess the line that get from markdown file
    """
    def Preprocess(self, line):
        """
        Check mostly used starting syntax
        """
        if line.startswith("- [ ] ") or line.startswith("- [x] "):
            line = line[6:]
        elif line.startswith("-[ ] ") or line.startswith("-[x] "):
            line = line[5:]
        elif line.startswith("-[] "):
            line = line[4:]
        elif line.startswith("- ") or line.startswith("> "):
            line = line[2:]
        
        """
        Check for newline operator
        """
        if line.endswith("\n"):
            line = line[:-1]

        """
        Check for whitespaces
        """
        line = line.strip()

        """
        translation progress is done line by line because summed string's length will exceed the character limit of the translator
        and in experiments it's seen that translator can not translate the non English word from the whole string
        """
        if self.isTranslate:
            if self.translatorName.get() == 'Google':
                line = self.translator.translate(line)
            else:
                tempStrArray = line.split(',')
                tempStr = ""
                for temp in tempStrArray:
                    tempStr += f"{self.translator.translate(temp)}, "
                return tempStr

        """
        Add comma to seperate prompts and provide continuousness 
        """
        line = line + ", "

        return line

    def ParseAndSave(self, promptFile):
        file = open(promptFile, "r")
        lines = file.readlines()
        file.close()

        """
        Get folder path where is the Markdown file located
        """
        filename = os.path.splitext(promptFile)[0]
        
        positiveFilename = f"{filename}_positive.txt"
        negativeFilename = f"{filename}_negative.txt"

        positiveStr = ""
        negativeStr = ""

        isPositive = True
        for line in lines:
            """
            Determine if positive or negative prompt
            """
            if line.find("Positive Prompts") != -1:
                isPositive = True
            elif line.find("Negative Prompts") != -1:
                isPositive = False
            
            """
            Continue if it is heading, new line, long line
            """
            if line.startswith("#") or line == "\n" or line.startswith("---") or line == '  \n':
                continue

            line = self.Preprocess(line)

            if isPositive:
                positiveStr = positiveStr + line
            else:
                negativeStr = negativeStr + line

        """
        Delete comma and white ', ' space which is added in preprocess stage from the last of the line
        """
        positiveStr = positiveStr[:-2]
        negativeStr = negativeStr[:-2]

        positiveFile = open(positiveFilename, "w")
        positiveFile.write(positiveStr)
        positiveFile.close()

        negativeFile = open(negativeFilename, "w")
        negativeFile.write(negativeStr)
        negativeFile.close()