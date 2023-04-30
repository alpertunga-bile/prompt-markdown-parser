import os
from subprocess import call, DEVNULL
import platform

class Startup:
    osName = None

    def __init__(self):
        self.osName = platform.system()

    def GetVenvCreateCommand(self):
        venvCommand = ""
        if self.osName == 'Linux':
            venvCommand = "pip install virtualenv && virtualenv venv && "
            venvCommand += "source /venv/bin/activate && "
            venvCommand += "pip3 install deep-translator customtkinter Pillow beautifulsoup4 requests tqdm lxml happytransformer && "
            venvCommand += "pip3 uninstall torch --yes && "
            venvCommand += "pip3 torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117 && "
            venvCommand += "deactivate"
        elif self.osName == 'Windows':
            venvCommand = "py -m venv venv && "
            venvCommand += ".\\venv\Scripts\\activate.bat && "
            venvCommand += ".\\venv\Scripts\\pip.exe install deep-translator customtkinter Pillow beautifulsoup4 requests tqdm lxml happytransformer && "
            venvCommand += ".\\venv\\Scripts\\pip.exe uninstall torch --yes && "
            venvCommand += ".\\venv\\Scripts\\pip.exe install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117 && "
            venvCommand += ".\\venv\\Scripts\\deactivate.bat"
        
        return venvCommand
    
    def CreateVenv(self):
        if os.path.exists("venv") == True:
            return

        print("Preparing virtual environment ...")
        result = call(self.GetVenvCreateCommand(), shell=True, stdout=DEVNULL)
        _ = print("Virtual environment is created") if result == 0 else print("Error")
    
    def GetStartGUICommand(self):
        guiCommand = ""
        if self.osName == 'Linux':
            guiCommand = "source /venv/bin/activate && python3 main.py"
        elif self.osName == 'Windows':
            guiCommand = ".\\venv\\Scripts\\activate.bat && .\\venv\\Scripts\\python.exe main.py"
        
        return guiCommand
    
    def StartGUI(self):
        if os.path.exists("dataset") is False:
            os.mkdir("dataset")

        print("Starting GUI ...")
        guiCommand = self.GetStartGUICommand()
        result = call(guiCommand, shell=True, stdout=DEVNULL)
        
        if self.osName == 'Linux':
            result = call("deactivate", shell=True, stdout=DEVNULL)
        elif self.osName == 'Windows':
            result = call(".\\venv\\Scripts\\deactivate.bat", shell=True, stdout=DEVNULL)
        
        if result == 0:
            print("Finished successfully")


if __name__ == "__main__":
    startup = Startup()
    startup.CreateVenv()
    startup.StartGUI()