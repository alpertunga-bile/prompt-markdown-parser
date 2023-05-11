from Startup import Startup
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser(description="Prompting tools")
    parser.add_argument("--update", action='store_true', help="Update packages in the virtual environment")
    parser.add_argument("--reinstall", action='store_true', help="Reinstall virtual environment")
    parser.add_argument("--no_check", action='store_true', help="Pass the virtual envrionment folder check")
    parser.add_argument("--gui", action='store_true', help="Starts GUI application")
    parser.add_argument("--cli", action='store_true', help="Starts CLI application")
    args = parser.parse_args()

    startup = Startup()
    startup.CreateVenv(args.no_check)

    if args.update:
        startup.UpdateVenv()

    if args.reinstall:
        startup.ReInstallVenv()

    if args.gui:
        startup.StartGUI()
    elif args.cli:
        startup.StartCLI()