from os.path import exists
from os import mkdir, remove
from subprocess import call, DEVNULL
from platform import system
from time import sleep
from shutil import rmtree

class Startup:
    osName = None

    def __init__(self):
        self.osName = system()

        if exists("venv") is False:
            mkdir("venv")

    def GetGUIVenvCreateCommand(self):
        venvCommand = ""
        if self.osName == 'Linux':
            venvCommand = "pip install virtualenv && virtualenv venv/gui_venv && "
            venvCommand += "source venv/gui_venv/bin/activate && "
            venvCommand += "pip3 install deep-translator customtkinter Pillow beautifulsoup4 requests tqdm lxml happytransformer && "
            venvCommand += "pip3 uninstall torch --yes && "
            venvCommand += "pip3 install torch torchvision torchaudio && "
            venvCommand += "deactivate"
        elif self.osName == 'Windows':
            venvCommand = "py -m venv venv/gui_venv && "
            venvCommand += ".\\venv\\gui_venv\Scripts\\activate.bat && "
            venvCommand += ".\\venv\\gui_venv\Scripts\\pip.exe install deep-translator customtkinter Pillow beautifulsoup4 requests tqdm lxml happytransformer && "
            venvCommand += ".\\venv\\gui_venv\\Scripts\\pip.exe uninstall torch --yes && "
            venvCommand += ".\\venv\\gui_venv\\Scripts\\pip.exe install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117 && "
            venvCommand += ".\\venv\\gui_venv\\Scripts\\deactivate.bat"
        
        return venvCommand
    
    def GetStartGUICommand(self):
        guiCommand = ""
        if self.osName == 'Linux':
            guiCommand = "source venv/gui_venv/bin/activate && python3 GUImain.py"
        elif self.osName == 'Windows':
            guiCommand = ".\\venv\\gui_venv\\Scripts\\activate.bat && .\\venv\\gui_venv\\Scripts\\python.exe GUImain.py"
        
        return guiCommand
    
    def CreateGUIVenv(self, isPass):
        if isPass is False:
            if exists("venv/gui_venv"):
                return

        print("Preparing GUI virtual environment ...")
        result = call(self.GetGUIVenvCreateCommand(), shell=True, stdout=DEVNULL)
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
            result = call(".\\venv\\gui_venv\\Scripts\\deactivate.bat", shell=True, stdout=DEVNULL)
        
        if result == 0:
            print("Finished successfully")

    def UpdateGUIVenv(self):
        print("Updating ...")
        if self.osName == 'Linux':
            call("source venv/gui_venv/bin/activate && pip3 freeze > requirements.txt", shell=True, stdout=DEVNULL)
        elif self.osName == 'Windows':
            call(".\\venv\\gui_venv\\Scripts\\activate.bat && .\\venv\\gui_venv\\Scripts\\pip.exe freeze > requirements.txt", shell=True, stdout=DEVNULL)

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
            call(".\\venv\\gui_venv\\Scripts\\pip.exe install -r requirements.txt --upgrade && .\\venv\\gui_venv\\Scripts\\deactivate.bat", shell=True, stdout=DEVNULL)

        remove("requirements.txt")

        print("Updating is Finished")

    def ReInstallGUIVenv(self):
        if exists('venv/gui_venv') is False:
            return
        
        rmtree('venv/gui_venv')
        self.CreateGUIVenv()

    """
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // CLI
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    """

    def GetCLIVenvCreateCommand(self):
        venvCommand = ""
        if self.osName == 'Linux':
            venvCommand = "pip install virtualenv && virtualenv venv/cli_venv && "
            venvCommand += "source venv/cli_venv/bin/activate && "
            venvCommand += "pip3 install deep-translator beautifulsoup4 requests tqdm lxml happytransformer && "
            venvCommand += "pip3 uninstall torch --yes && "
            venvCommand += "pip3 install torch torchvision torchaudio && "
            venvCommand += "deactivate"
        elif self.osName == 'Windows':
            venvCommand = "py -m venv venv/cli_venv && "
            venvCommand += ".\\venv\\cli_venv\Scripts\\activate.bat && "
            venvCommand += ".\\venv\\cli_venv\Scripts\\pip.exe install deep-translator beautifulsoup4 requests tqdm lxml happytransformer pyreadline3 && "
            venvCommand += ".\\venv\\cli_venv\\Scripts\\pip.exe uninstall torch --yes && "
            venvCommand += ".\\venv\\cli_venv\\Scripts\\pip.exe install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117 && "
            venvCommand += ".\\venv\\cli_venv\\Scripts\\deactivate.bat"

        return venvCommand

    def CreateCLIVenv(self, isPass):
        if isPass is False:
            if exists("venv/cli_venv"):
                return
        
        print("Preparing CLI virtual environment ...")
        result = call(self.GetCLIVenvCreateCommand(), shell=True, stdout=DEVNULL)
        _ = print("Virtual environment is created") if result == 0 else print("Error")

    def GetStartCLICommand(self):
        cliCommand = ""
        if self.osName == 'Linux':
            cliCommand = "source venv/cli_venv/bin/activate && python3 CLImain.py"
        elif self.osName == 'Windows':
            cliCommand = ".\\venv\\cli_venv\\Scripts\\activate.bat && .\\venv\\cli_venv\\Scripts\\python.exe CLImain.py"
        
        return cliCommand

    def StartCLI(self):
        if exists("dataset") is False:
            mkdir("dataset")

        print("Starting CLI ...")
        cliCommand = self.GetStartCLICommand()
        result = call(cliCommand, shell=True)
        
        if self.osName == 'Linux':
            result = call("deactivate", shell=True, stdout=DEVNULL)
        elif self.osName == 'Windows':
            result = call(".\\venv\\cli_venv\\Scripts\\deactivate.bat", shell=True, stdout=DEVNULL)
        
        if result == 0:
            print("Finished successfully")

    def UpdateCLIVenv(self):
        print("Updating ...")
        if self.osName == 'Linux':
            call("source venv/cli_venv/bin/activate && pip3 freeze > requirements.txt", shell=True, stdout=DEVNULL)
        elif self.osName == 'Windows':
            call(".\\venv\\cli_venv\\Scripts\\activate.bat && .\\venv\\cli_venv\\Scripts\\pip.exe freeze > requirements.txt", shell=True, stdout=DEVNULL)

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
            call(".\\venv\\cli_venv\\Scripts\\pip.exe install -r requirements.txt --upgrade && .\\venv\\cli_venv\\Scripts\\deactivate.bat", shell=True, stdout=DEVNULL)

        remove("requirements.txt")

        print("Updating is Finished")

    def ReInstallCLIVenv(self):
        if exists('venv/cli_venv') is False:
            return
        
        rmtree('venv/cli_venv')
        self.CreateCLIVenv()