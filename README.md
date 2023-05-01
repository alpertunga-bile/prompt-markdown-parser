# prompt-markdown-parser

<p align="center">
  <img src=https://user-images.githubusercontent.com/76731692/234883310-86fceaa3-45b3-4870-83ca-3642b98ccf20.gif alt="animated" />
</p>

- Markdown is a lightweight markup language for creating formatted text using a plain-text editor. You can easily format your texts with Markdown format. Prompts can be difficult to organize. So with this GUI based solution you can easily structure your prompts with Markdown file format and get positive and negative prompts as seperate txt files. 
- Now you can create datasets, train your prompt generator model, evaluate your model and generate prompts with it.

# Contents

- [Updates](https://github.com/alpertunga-bile/prompt-markdown-parser#updates)
- [Requirements](https://github.com/alpertunga-bile/prompt-markdown-parser#requirements)
- [Usage](https://github.com/alpertunga-bile/prompt-markdown-parser#usage)
    - [Parser Tab](https://github.com/alpertunga-bile/prompt-markdown-parser#parser-tab)
    - [Dataset Tab](https://github.com/alpertunga-bile/prompt-markdown-parser#dataset-tab)
    - [Train Tab](https://github.com/alpertunga-bile/prompt-markdown-parser#train-tab)
    - [Evaluate Tab](https://github.com/alpertunga-bile/prompt-markdown-parser#evaluate-tab)
    - [Generate Tab](https://github.com/alpertunga-bile/prompt-markdown-parser#generate-tab)
- [Examples](https://github.com/alpertunga-bile/prompt-markdown-parser#examples)
    - [Parser Example](https://github.com/alpertunga-bile/prompt-markdown-parser#parser-example)
    - [Generator Examples](https://github.com/alpertunga-bile/prompt-markdown-parser#generator-examples)

# Updates
## Update Date : 01/05/2023
- SelfRecursive algorithm is added.
- Preprocess is added for generating tab to get prompt more accurately.

## Update Date : 30/04/2023
- Adding datasets to previous datasets functionality is added
- Removing duplicates from datasets when adding new data functionality is added
- New models are trained and added to Google Drive link.
- Startup class is added. Automation commands are added for Linux environment.

## Update Date : 29/04/2023
- GUI is divided into tabs such as parse, dataset, train, evaluate, generate.
- Parse tab has the functionality of the parser which is translating prompts and parsing Markdown files.
- In the dataset tab, you can create prompt datasets to use in other tabs.
- In the train tab, you can train your prompt transformer such as GPT2.
- In the evaluate tab, you can get loss score of your model for the given dataset.
- In the generate tab, you can use your model to generate texts. You can enter seed text and configure recursive level.

## Update Date : 28/04/2023
- Virtual environment is using bat files to activate and deactivate.
- GUI appearance can be changed between light and dark mode.
- New translators are added but Google is the only one working without errors.

## Update Date : 27/04/2023
- Translator is added with deep-translator
- Modern GUI style is added with customtkinter
- Virtual environment automation is added. No need to configure manually. Just run ```python start.py``` command.
- Progress bar is added.
- Parsing and translation is done in threads so no freezing when parsing.

# Requirements
- Tested in Windows OS environment.
- Venv, deep-translator, customtkinter, happytransformer, Pillow, beautifulsoup4, tqdm, lxml and Tkinter packages are used.
- Tested with Python 3.10.6. As a note for Python 3.10.6 version Tkinter comes as default. You can easily test it with these commands:

## Check Tkinter Module
- From command line enter ```python``` command and press Enter button.
- Write ```import tkinter``` command and press Enter button. If there are no errors. You are ready to go.
- Write ```exit()``` command and press Enter button to exit.

# Usage
## Parser Tab
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
## Train Tab
- Enter your model name. You can found the [model names](https://huggingface.co/models?pipeline_tag=text-generation)
- Enter epochs, batch size.
- Enter folder name for your model. Your model is going to be saved into 'dataset' folder.
- Choose dataset to train with model.
- Click ***Train*** button and wait for ***Done!!!*** text to appear above the button.
## Evaluate Tab
- Choose your dataset which is used for training.
- Enter your model name that you used for training. DO NOT enter the folder name of your model.
- Choose your model's saved folder.
- Click ***Evaluate*** button and wait for a ***Evaluation score*** output above the button.
## Generate Tab
- Enter your model name that you used for training. DO NOT enter the folder name of your model.
- Choose your model's saved folder.
- Enter min length that model can generate.
- Enter max length that model can generate.
- Tick the checkboxes if you want these features.
- Set recursive level with slider. It is going to give model the previous result in each step.
- Select if you want self recursive.
- Enter your seed and click ***Generate Text*** button and wait for text to be appeared in the textbox.
### How Recursive Works?
- Let's say we give ```a, ``` as seed and recursive level is 2. I am going to use the same outputs for this example to understand the functionality more accurately.
- With self recursive, let's say generator's output is ```b```. So next seed is going to be 'b', generator's output is ```c```. Final output is ```a, c```. It can be used for generating random outputs.
- Without self recursive, let's say generator's output is ```b```. So next seed is going to be ```a, b```, generator's output is ```a, b, c```. Final output is ```a, b, c```. It can be used for more accurate prompts.

# Examples
## Parser Example
- You can access the [Markdown file](https://github.com/alpertunga-bile/prompt-markdown-parser/blob/master/example/example.md) that is used for the below image.
- Image is upscaled with [AIUpscaleGUI](https://github.com/alpertunga-bile/AIUpscaleGUI) project.

![00069-3749032177_out](https://user-images.githubusercontent.com/76731692/233834377-0b2b717b-5301-4672-93d4-0d8a56d68a88.png)

## Generator Examples
- Some typo fixes are done in generated prompts.
- female_positive_gpt2-75_model is used for generator examples. Used model can be found [here](https://drive.google.com/drive/folders/1c21kMH6FTaia5C8239okL3Q0wJnnWc1N?usp=share_link).
- Model is trained with 75 epochs and 1 batch size.

### Example 1
- Model Name : gpt2
- Min Length : 10
- Max Length : 50
- Features are off
- Recursive Level : 0
- Self Recursive : Off
- Seed : mature woman, mechanical halo
- Generated Prompt : mature woman, mechanical halo, (blue hair:1.2), intricate, high detail, sharp focus, dramatic, beautiful girl, RAW photo, 8k uhd, film grain, caustics, subsurface scattering, reflections, (cowboy shot:1)

![00000-1602665147](https://user-images.githubusercontent.com/76731692/235329481-ae4017cd-4a9a-4d26-8993-a5515a43bdc9.jpg)

### Example 2
- Model Name : gpt2
- Min Length : 10
- Max Length : 50
- Features are off
- Recursive Level : 1
- Seed : goddess
- Self Recursive : Off
- Generated Prompt : goddess, (intricate detailed skin texture:1.2), (electric spark, broken machine:1.1), (machine body:1.2), looking at the viewer, (smart sharpen:1.2), medium breasts, (Ghost in the Shell), depth of field, gradient background, backlit, rim lighting, dramatic lighting, ambient occlusion, volumetric lighting, professional studio lighting, closed mouth, insanely detailed,, ((masterpiece)), absurdres, HDR

![00001-1760621993](https://user-images.githubusercontent.com/76731692/235329508-e33b0d29-c72f-4b12-8e1b-11b35e45dedc.png)
