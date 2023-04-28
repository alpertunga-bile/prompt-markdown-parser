import os
from subprocess import call, DEVNULL

if __name__ == "__main__":
    if(os.path.exists("env") == False):
        venvCommand = "py -m venv env && "
        venvCommand += ".\\env\Scripts\\activate.bat && "
        venvCommand += ".\\env\Scripts\\pip.exe install beautifulsoup4 requests tqdm lxml && "
        venvCommand += ".\\env\\Scripts\\deactivate.bat"
        
        print("Preparing virtual environment ...")
        result = call(venvCommand, shell=True, stdout=DEVNULL)
        _ = print("Virtual environment is created") if result == 0 else print("Error")

    call('cls' if os.name=='nt' else 'clear', shell=True, stdout=DEVNULL)
    print("Starting Scraper ...")
    scrapperCommand = ".\\env\\Scripts\\activate.bat && .\\env\\Scripts\\python.exe main.py"
    result = call(scrapperCommand, shell=True, stdout=DEVNULL)
    result = call(".\\env\\Scripts\\deactivate.bat", shell=True, stdout=DEVNULL)
    call('cls' if os.name=='nt' else 'clear', shell=True, stdout=DEVNULL)