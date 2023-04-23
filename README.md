# prompt-markdown-parser

- Markdown is a lightweight markup language for creating formatted text using a plain-text editor. You can easily format your texts with Markdown format. Prompts can be difficult to organize. So with this GUI based solution you can easily structure your prompts with Markdown file format and get positive and negative prompts as seperate txt files.

## Requirements
- Tested with Python 3.10.6 and used Tkinter for GUI. If Tkinter is installed it will not be a problem.

## Usage
- Clone the repository with ```git clone https://github.com/alpertunga-bile/prompt-markdown-parser.git``` command
- Get into folder with ```cd prompt-markdown-parser``` command
- Start GUI with  with ```python main.py``` command
- Press ***Select Prompt Files*** button. It is going to show a window to let you select your Markdown files. You can choose multiple files.
- After the selection press ***Parse And Save*** button and it's done. You can find your text files in the folder where are your selected Markdown files. You can see that it seperates negative and positive prompts with ***_negative*** and ***_positive*** names.
- DO NOT EDIT ***Positive Prompts*** and ***Negative Prompts*** strings in Markdown files. These are used to seperate prompts. You can add # symbol but do not edit the strings.
- DO NOT ADD comma "," at the end of your rows. Parser is adding for you. 

### Example
- You can access the [Markdown file](https://github.com/alpertunga-bile/prompt-markdown-parser/blob/master/example/example.md) that is used for the below image.
- Image is upscaled with [AIUpscaleGUI](https://github.com/alpertunga-bile/AIUpscaleGUI) project.

![00069-3749032177_out](https://user-images.githubusercontent.com/76731692/233834377-0b2b717b-5301-4672-93d4-0d8a56d68a88.png)
