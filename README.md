# prompt-markdown-parser

- Markdown is a lightweight markup language for creating formatted text using a plain-text editor. You can easily format your texts with Markdown format. Prompts can be difficult to organize. So with this GUI based solution you can easily structure your prompts with Markdown file format and get positive and negative prompts as seperate txt files.

## Updates
### Update Date : 27/04/2023
- Translator is added with deep-translator
- Modern GUI style is added with customtkinter
- Virtual environment automation is added. No need to configure manually. Just run ```python start.py``` command.
- Progress bar is added.
- Parsing and translation is done in threads so no freezing when parsing.

## Requirements
- Venv, deep-translator, customtkinter and Tkinter packages are used.
- Tested with Python 3.10.6. As a note for Python 3.10.6 version Tkinter comes as default. You can easily test it with these commands:

### Check Tkinter Module
- From command line enter ```python``` command and press Enter button.
- Write ```import tkinter``` command and press Enter button. If there are no errors. You are ready to go.
- Write ```exit()``` command and press Enter button to exit.

## Usage
- Clone the repository with ```git clone https://github.com/alpertunga-bile/prompt-markdown-parser.git``` command.
- Get into folder with ```cd prompt-markdown-parser``` command.
- Start the application with ```python start.py``` command. This command is going to look for 'venv' file for virtual environment. It is going to setup the dependencies (deep-translator and customtkinter) and start the application. After the first setup, it is just going to start the GUI application.
- You can choose ***Translate Prompts*** checkbox to translate your prompts to English. You can write prompts in a mixture of English and your native language. GoogleTranslator is used for translation. This checkbox works with ***Parse All Files In 'prompts' Folder*** and ***Parse And Save*** functionalities.
- ***Parse All Files In 'prompts' Folder*** button is getting all markdown files under 'prompts' folder which is located in repo directory and parse and save them.
- ***Select Prompt Files*** button is going to show a window to let you select your Markdown files. You can choose multiple files.
- After the selection press ***Parse And Save*** button and it's done. You can find your text files in the folder where are your selected Markdown files. You can see that it seperates negative and positive prompts with ***_negative*** and ***_positive*** names.
- DO NOT EDIT ***Positive Prompts*** and ***Negative Prompts*** strings in Markdown files. These are used to seperate prompts. You can add or reduce # symbol but do not edit the strings.
- DO NOT ADD comma "," at the end of your rows. Parser is adding for you.

### Example
- You can access the [Markdown file](https://github.com/alpertunga-bile/prompt-markdown-parser/blob/master/example/example.md) that is used for the below image.
- Image is upscaled with [AIUpscaleGUI](https://github.com/alpertunga-bile/AIUpscaleGUI) project.

![00069-3749032177_out](https://user-images.githubusercontent.com/76731692/233834377-0b2b717b-5301-4672-93d4-0d8a56d68a88.png)
