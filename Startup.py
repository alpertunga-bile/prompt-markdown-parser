from os.path import exists
from os import mkdir, remove
from subprocess import call, DEVNULL
from platform import system
from time import sleep

class Startup:
    osName = None

    def __init__(self):
        self.osName = system()

    def GetVenvCreateCommand(self):
        venvCommand = ""
        if self.osName == 'Linux':
            venvCommand = "pip install virtualenv && virtualenv venv && "
            venvCommand += "source /venv/bin/activate && "
            venvCommand += "pip3 install deep-translator customtkinter Pillow beautifulsoup4 requests tqdm lxml happytransformer && "
            venvCommand += "pip3 uninstall torch --yes && "
            venvCommand += "pip3 install torch torchvision torchaudio && "
            venvCommand += "deactivate"
        elif self.osName == 'Windows':
            venvCommand = "py -m venv venv && "
            venvCommand += ".\\venv\Scripts\\activate.bat && "
            venvCommand += ".\\venv\Scripts\\pip.exe install deep-translator customtkinter Pillow beautifulsoup4 requests tqdm lxml happytransformer && "
            venvCommand += ".\\venv\\Scripts\\pip.exe uninstall torch --yes && "
            venvCommand += ".\\venv\\Scripts\\pip.exe install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117 && "
            venvCommand += ".\\venv\\Scripts\\deactivate.bat"
        
        return venvCommand
    
    def GetStartGUICommand(self):
        guiCommand = ""
        if self.osName == 'Linux':
            guiCommand = "source /venv/bin/activate && python3 main.py"
        elif self.osName == 'Windows':
            guiCommand = ".\\venv\\Scripts\\activate.bat && .\\venv\\Scripts\\pip.exe freeze > requirements.txt && .\\venv\\Scripts\\python.exe main.py"
        
        return guiCommand
    
    def CreateVenv(self):
        if exists("venv") == True:
            return

        print("Preparing virtual environment ...")
        result = call(self.GetVenvCreateCommand(), shell=True, stdout=DEVNULL)
        _ = print("Virtual environment is created") if result == 0 else print("Error")
    
    def StartGUI(self):
        if exists("dataset") is False:
            mkdir("dataset")

        print("Starting GUI ...")
        guiCommand = self.GetStartGUICommand()
        result = call(guiCommand, shell=True, stdout=DEVNULL)
        
        if self.osName == 'Linux':
            result = call("deactivate", shell=True, stdout=DEVNULL)
        elif self.osName == 'Windows':
            result = call(".\\venv\\Scripts\\deactivate.bat", shell=True, stdout=DEVNULL)
        
        if result == 0:
            print("Finished successfully")

    def Update(self):
        print("Updating ...")
        if self.osName == 'Linux':
            call("source /venv/bin/activate && pip3 freeze > requirements.txt", shell=True, stdout=DEVNULL)
        elif self.osName == 'Windows':
            call(".\\venv\\Scripts\\activate.bat && .\\venv\\Scripts\\pip.exe freeze > requirements.txt", shell=True, stdout=DEVNULL)

        sleep(0.5)

        file = open("requirements.txt", "r")
        lines = file.readlines()
        file.close()

        file = open("requirements.txt", "w")
        for line in lines:
            file.writelines(line.replace("==", ">="))

        file.close()
        
        sleep(0.5)

        if self.osName == 'Linux':
            call("pip3 install -r requirements.txt --upgrade && deactivate", shell=True, stdout=DEVNULL)
        elif self.osName == 'Windows':
            call(".\\venv\\Scripts\\pip.exe install -r requirements.txt --upgrade && .\\venv\\Scripts\\deactivate.bat", shell=True, stdout=DEVNULL)

        remove("requirements.txt")

        print("Updating is Finished")