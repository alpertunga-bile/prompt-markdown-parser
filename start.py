from Startup import Startup
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser(description="Prompting tools")
    parser.add_argument("--update", action='store_true', help="Update packages in the virtual environment")
    args = parser.parse_args()

    startup = Startup()
    startup.CreateVenv()

    if args.update:
        startup.Update()
    
    startup.StartGUI()