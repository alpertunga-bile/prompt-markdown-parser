import tkinter as tk
from tkinter import filedialog
import os

class Functions:
    promptFiles = None

    def SelectDirectory(self):
        self.promptFiles = filedialog.askopenfilenames(initialdir=os.getcwd())

    def Run(self):  
        print("Parsing ...")      
        for promptFile in self.promptFiles:
            print(f"Parsing {promptFile} ...")
            self.ParseAndSave(promptFile)
        print("Done!")

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
            
            if line.startswith("#") or line == "\n" or line.startswith("---"):
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


if __name__ == "__main__":
    func = Functions()

    window = tk.Tk()
    window.geometry("600x100")

    tempPath = os.path.join(os.getcwd(), "test.md")

    startFrame = tk.Frame()

    directoryLabel = tk.Label(master=startFrame, text=f"{tempPath}")
    directoryLabel.grid(column=0, row=0, padx=(0, 50), ipady=5)

    selectButton = tk.Button(
        master=startFrame,
        text="Select Prompt Files",
        command=func.SelectDirectory
    )

    selectButton.grid(column=1, row=0)

    startFrame.pack()

    initializeFrame = tk.Frame()

    initializeButton = tk.Button(
        master=initializeFrame,
        text="Parse And Save",
        command=func.Run
    )

    initializeButton.pack()
    initializeFrame.pack()

    window.mainloop()