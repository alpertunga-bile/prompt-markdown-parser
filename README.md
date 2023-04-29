# prompt-markdown-parser

[Updates](https://github.com/alpertunga-bile/prompt-markdown-parser/edit/master/README.md#updates) | [Requirements](https://github.com/alpertunga-bile/prompt-markdown-parser/edit/master/README.md#requirements) | [Usage](https://github.com/alpertunga-bile/prompt-markdown-parser/edit/master/README.md#usage) | [Example](https://github.com/alpertunga-bile/prompt-markdown-parser/edit/master/README.md#example)

<p align="center">
  <img src=https://user-images.githubusercontent.com/76731692/234883310-86fceaa3-45b3-4870-83ca-3642b98ccf20.gif alt="animated" />
</p>

- Markdown is a lightweight markup language for creating formatted text using a plain-text editor. You can easily format your texts with Markdown format. Prompts can be difficult to organize. So with this GUI based solution you can easily structure your prompts with Markdown file format and get positive and negative prompts as seperate txt files. 
- Now you can create datasets, train your prompt generator model, evaluate your model and generate prompts with it.

## Updates
### Update Date : 29/04/2023
- GUI is divided into tabs such as parse, dataset, train, evaluate, generate.
- Parse tab has the functionality of the parser which is translating prompts and parsing Markdown files.
- In the dataset tab, you can create prompt datasets to use in other tabs.
- In the train tab, you can train your prompt transformer such as GPT2.
- In the evaluate tab, you can get loss score of your model for the given dataset.
- In the generate tab, you can use your model to generate texts. You can enter seed text and configure recursive level.

### Update Date : 28/04/2023
- Virtual environment is using bat files to activate and deactivate.
- GUI appearance can be changed between light and dark mode.
- New translators are added but Google is the only one working without errors.

### Update Date : 27/04/2023
- Translator is added with deep-translator
- Modern GUI style is added with customtkinter
- Virtual environment automation is added. No need to configure manually. Just run ```python start.py``` command.
- Progress bar is added.
- Parsing and translation is done in threads so no freezing when parsing.

## Requirements
- Tested in Windows OS environment.
- Venv, deep-translator, customtkinter, happytransformer, Pillow, beautifulsoup4, tqdm, lxml and Tkinter packages are used.
- Tested with Python 3.10.6. As a note for Python 3.10.6 version Tkinter comes as default. You can easily test it with these commands:

### Check Tkinter Module
- From command line enter ```python``` command and press Enter button.
- Write ```import tkinter``` command and press Enter button. If there are no errors. You are ready to go.
- Write ```exit()``` command and press Enter button to exit.

## Usage
### Parser Tab
- Clone the repository with ```git clone https://github.com/alpertunga-bile/prompt-markdown-parser.git``` command.
- Get into folder with ```cd prompt-markdown-parser``` command.
- Start the application with ```python start.py``` command. This command is going to look for 'venv' file for virtual environment. It is going to setup the dependencies and start the application. It will take minutes so please be patient. After the first setup, it is just going to start the GUI application. 
- You can choose ***Translate Prompts*** checkbox to translate your prompts to English. You can write prompts in a mixture of English and your native language. GoogleTranslator is used for translation. This checkbox works with ***Parse All Files In 'prompts' Folder*** and ***Parse And Save*** functionalities.
- ***Parse All Files In 'prompts' Folder*** button is getting all markdown files under 'prompts' folder which is located in repo directory and parse and save them.
- ***Select Prompt Files*** button is going to show a window to let you select your Markdown files. You can choose multiple files.
- After the selection press ***Parse And Save*** button and it's done. You can find your text files in the folder where are your selected Markdown files. You can see that it seperates negative and positive prompts with ***_negative*** and ***_positive*** names.
- DO NOT EDIT ***Positive Prompts*** and ***Negative Prompts*** strings in Markdown files. These are used to seperate prompts. You can add or reduce # symbol but do not edit the strings.
- DO NOT ADD comma "," at the end of your rows. Parser is adding for you.
### Dataset Tab
- Save prompt links in a txt file. Just select image from CivitAi and copy and paste its link into a txt file. 
- Choose your link dataset which is provided in txt file.
- Write positive and negative filenames as you want to name them.
- Click ***Create Dataset*** button and wait. You can watch the progress with progressbar in GUI and in terminal.
### Train Tab
- Enter your model name. You can found the [model names](https://huggingface.co/models?pipeline_tag=text-generation)
- Enter epochs, batch size.
- Enter folder name for your model. Your model is going to be saved into 'dataset' folder.
- Choose dataset to train with model.
- Click ***Train*** button and wait for ***Done!!!*** text to appear above the button.
### Evaluate Tab
- Choose your dataset which is used for training.
- Enter your model name that you used for training. DO NOT enter the folder name of your model.
- Choose your model's saved folder.
- Click ***Evaluate*** button and wait for a ***Evaluation score*** output above the button.
### Generate Tab
- Enter your model name that you used for training. DO NOT enter the folder name of your model.
- Choose your model's saved folder.
- Enter min length that model can generate.
- Enter max length that model can generate.
- Tick the checkboxes if you want these features.
- Set recursive level with slider. It is going to give model the previous result in each step.
- Enter your seed and click ***Generate Text*** button and wait for text to be appeared in the textbox.

### Example
- You can access the [Markdown file](https://github.com/alpertunga-bile/prompt-markdown-parser/blob/master/example/example.md) that is used for the below image.
- Image is upscaled with [AIUpscaleGUI](https://github.com/alpertunga-bile/AIUpscaleGUI) project.

![00069-3749032177_out](https://user-images.githubusercontent.com/76731692/233834377-0b2b717b-5301-4672-93d4-0d8a56d68a88.png)
