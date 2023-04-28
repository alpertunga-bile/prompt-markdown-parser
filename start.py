import os
from subprocess import call, DEVNULL

if __name__ == "__main__":
    if(os.path.exists("venv") == False):
        venvCommand = "py -m venv venv && "
        venvCommand += ".\\venv\Scripts\\activate.bat && "
        venvCommand += ".\\venv\Scripts\\pip.exe install deep-translator customtkinter Pillow && "
        venvCommand += ".\\venv\\Scripts\\deactivate.bat"
        
        print("Preparing virtual environment ...")
        result = call(venvCommand, shell=True, stdout=DEVNULL)
        _ = print("Virtual environment is created") if result == 0 else print("Error")

    print("Starting GUI ...")
    guiCommand = ".\\venv\\Scripts\\activate.bat && .\\venv\\Scripts\\python.exe main.py"
    result = call(guiCommand, shell=True, stdout=DEVNULL)
    result = call(".\\venv\\Scripts\\deactivate.bat", shell=True, stdout=DEVNULL)