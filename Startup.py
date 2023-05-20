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

    def GetVenvCreateCommand(self):
        venvCommand = ""
        if self.osName == 'Linux':
            venvCommand = "pip install virtualenv && virtualenv venv && "
            venvCommand += "source venv/bin/activate && "
            venvCommand += "pip3 install -r requirements.txt && pip3 uninstall torch --yes && "
            venvCommand += "pip3 install torch && "
            venvCommand += "deactivate"
        elif self.osName == 'Windows':
            venvCommand = "python -m venv venv && "
            venvCommand += ".\\venv\\Scripts\\activate.bat && "
            venvCommand += ".\\venv\\Scripts\\pip.exe install -r requirements.txt && "
            venvCommand += ".\\venv\\Scripts\\pip.exe uninstall torch --yes && "
            venvCommand += ".\\venv\\Scripts\\pip.exe install torch --index-url https://download.pytorch.org/whl/cu117 && "
            venvCommand += ".\\venv\\Scripts\\deactivate.bat"
        
        return venvCommand
    
    def GetStartGUICommand(self):
        guiCommand = ""
        if self.osName == 'Linux':
            guiCommand = "source venv/bin/activate && python3 GUImain.py"
        elif self.osName == 'Windows':
            guiCommand = ".\\venv\\Scripts\\activate.bat && .\\venv\\Scripts\\python.exe GUImain.py"
        
        return guiCommand
    
    def CreateVenv(self, isPass):
        if isPass is False:
            if exists("venv"):
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

    def UpdateVenv(self):
        print("Updating ...")
        if self.osName == 'Linux':
            call("source venv/gui_venv/bin/activate && pip3 freeze > new_requirements.txt", shell=True, stdout=DEVNULL)
        elif self.osName == 'Windows':
            call(".\\venv\\Scripts\\activate.bat && .\\venv\\Scripts\\pip.exe freeze > new_requirements.txt", shell=True, stdout=DEVNULL)

        sleep(0.5)

        file = open("new_requirements.txt", "r")
        lines = file.readlines()
        file.close()

        file = open("new_requirements.txt", "w")
        for line in lines:
            file.writelines(line.replace("==", ">="))

        file.close()
        
        sleep(0.5)

        if self.osName == 'Linux':
            call("pip3 install -r new_requirements.txt --upgrade && deactivate", shell=True, stdout=DEVNULL)
        elif self.osName == 'Windows':
            call(".\\venv\\Scripts\\pip.exe install -r new_requirements.txt --upgrade && .\\venv\\Scripts\\deactivate.bat", shell=True, stdout=DEVNULL)

        remove("new_requirements.txt")

        print("Updating is Finished")

    def ReInstallVenv(self):
        if exists('venv') is False:
            return
        
        rmtree('venv')
        self.CreateVenv(False)

    """
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // CLI
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    """

    def GetStartCLICommand(self):
        cliCommand = ""
        if self.osName == 'Linux':
            cliCommand = "source venv/bin/activate && python3 CLImain.py"
        elif self.osName == 'Windows':
            cliCommand = ".\\venv\\Scripts\\activate.bat && .\\venv\\Scripts\\python.exe CLImain.py"
        
        return cliCommand

    def StartCLI(self):
        if exists("dataset") is False:
            mkdir("dataset")

        if exists("prompts") is False:
            mkdir("prompts")

        print("Starting CLI ...")
        cliCommand = self.GetStartCLICommand()
        result = call(cliCommand, shell=True)
        
        if self.osName == 'Linux':
            result = call("deactivate", shell=True, stdout=DEVNULL)
        elif self.osName == 'Windows':
            result = call(".\\venv\\Scripts\\deactivate.bat", shell=True, stdout=DEVNULL)
        
        if result == 0:
            print("Finished successfully")