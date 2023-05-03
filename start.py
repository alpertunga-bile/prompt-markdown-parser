from Startup import Startup
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser(description="Prompting tools")
    parser.add_argument("--update", action='store_true', help="Update packages in the virtual environment")
    parser.add_argument("--reinstall", action='store_true', help="Reinstall virtual environment")
    args = parser.parse_args()

    startup = Startup()
    startup.CreateVenv()

    if args.update:
        startup.Update()
    
    if args.reinstall:
        startup.ReInstall()
    
    startup.StartGUI()