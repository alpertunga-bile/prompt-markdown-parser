# prompt-markdown-parser

<p align="center">
  <img src=https://user-images.githubusercontent.com/76731692/234883310-86fceaa3-45b3-4870-83ca-3642b98ccf20.gif alt="animated" />
</p>

- Markdown is a lightweight markup language for creating formatted text using a plain-text editor. You can easily format your texts with Markdown format. Prompts can be difficult to organize. So with this GUI and CLI based solution you can easily structure your prompts with Markdown file format and get positive and negative prompts as seperate txt files. 
- Now you can create datasets, train your prompt generator model, evaluate your model and generate prompts with it.

# Contents

- [Updates](https://github.com/alpertunga-bile/prompt-markdown-parser#updates)
- [Requirements](https://github.com/alpertunga-bile/prompt-markdown-parser#requirements)
- [Usage](https://github.com/alpertunga-bile/prompt-markdown-parser#usage)
    - [CLI Application](https://github.com/alpertunga-bile/prompt-markdown-parser#cli-application)
      - [Parse Menu](https://github.com/alpertunga-bile/prompt-markdown-parser#parse-menu)
      - [Civitai Menu](https://github.com/alpertunga-bile/prompt-markdown-parser#civitai-menu)
      - [Create Menu](https://github.com/alpertunga-bile/prompt-markdown-parser#create-menu)
      - [Train Menu](https://github.com/alpertunga-bile/prompt-markdown-parser#train-menu)
      - [Evaluate Menu](https://github.com/alpertunga-bile/prompt-markdown-parser#evaluate-menu)
      - [Generate Menu](https://github.com/alpertunga-bile/prompt-markdown-parser#generate-menu)
        - [Generate Menu](https://github.com/alpertunga-bile/prompt-markdown-parser#generate-menu-1)
        - [Set Menu](https://github.com/alpertunga-bile/prompt-markdown-parser#set-menu)
        - [Print Menu](https://github.com/alpertunga-bile/prompt-markdown-parser#print-menu)
    - [GUI Application](https://github.com/alpertunga-bile/prompt-markdown-parser#gui-application)
      - [Parser Tab](https://github.com/alpertunga-bile/prompt-markdown-parser#parser-tab)
      - [Dataset Tab](https://github.com/alpertunga-bile/prompt-markdown-parser#dataset-tab)
      - [Civitai Tab](https://github.com/alpertunga-bile/prompt-markdown-parser#civitai-tab)
      - [Train Tab](https://github.com/alpertunga-bile/prompt-markdown-parser#train-tab)
      - [Evaluate Tab](https://github.com/alpertunga-bile/prompt-markdown-parser#evaluate-tab)
      - [Generate Tab](https://github.com/alpertunga-bile/prompt-markdown-parser#generate-tab)
    - [WebUI Application](https://github.com/alpertunga-bile/prompt-tools-webui)
    - [Prompt Generator Custom Node for ComfyUI](https://github.com/alpertunga-bile/prompt-generator-comfyui)
- [Examples](https://github.com/alpertunga-bile/prompt-markdown-parser#examples)
    - [Parser Example](https://github.com/alpertunga-bile/prompt-markdown-parser#parser-example)
    - [Generator Examples](https://github.com/alpertunga-bile/prompt-markdown-parser#generator-examples)

# Updates 
- See the updates.md file.

# Requirements
- Tested in Windows OS environment.
- Minimum 3.7 Python version is required for the GUI application.
- Tested with Python 3.10.6 and 3.11.3. As a note for Python 3.10.6 and newer versions Tkinter comes as default. You can easily test it with these commands:

## Check Tkinter Module
- From command line enter ```python``` command and press Enter button.
- Write ```import tkinter``` command and press Enter button. If there are no errors. You are ready to go.
- Write ```exit()``` command and press Enter button to exit.

# Usage
- Clone the repository with ```git clone https://github.com/alpertunga-bile/prompt-markdown-parser.git``` command.
- Get into folder with ```cd prompt-markdown-parser``` command.

## Windows
- Run ```python start.py``` command.

https://github.com/alpertunga-bile/prompt-markdown-parser/assets/76731692/ec9826bf-509e-4c62-8e78-952fe24db44f

## Linux
- Try ```python start.py``` command. If it fails, run these commands
```bash
python -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

# CLI Application

- Start the application with ```python start.py --cli``` command. This command is going to look for 'venv' file for virtual environment. It is going to setup the dependencies and start the application. After the first setup, it is just going to start the CLI application.
- There are 8 commands in the main menu. These are parse, create, train, evaluate, generate, clear, cls and exit. With first 5 commands you can access to different menus. With clear and cls commands you can clear the terminal. With exit command you can terminate the application.
- You do not have to write all the commands you can write first 2 or 3 letters and press ```TAB``` button for auto complete.

## Parse Menu
- In parse section there are 3 commands, allParse, parse and exit. You can use ```TAB``` button here.
- You have to have ```prompts``` folder to continue with allParse command. It will found all .md files under ```prompts``` folder and print the total files it can found. After that it is going to ask you to want to translate. You can use auto complete functionality here. Then it is going to parse all files and write them under ```prompts``` folder.
- In parse command. You specify a filepath to parse and it is going to ask translation and after that it is going to parsed and saved to the same folder with .md file.

https://github.com/alpertunga-bile/prompt-markdown-parser/assets/76731692/90fd1ef2-4626-43eb-ab2d-9a14f24b8445

## Civitai Menu
- There are three functionalities you can use.
- [x] Files have to be in ```dataset``` folder and just write the filename not path.
- Enhance functionality is for creating dataset. You can specify positive and negative filenames. Then you can specify image limit in [1, 200] range. Then specify image cursor to start, when to finish as hour and minute. Specify wanted and unwanted prompts with comma seperated. You can use default prompts. Select sort, period and nsfw parameters.
- Prune functionality is for clearing duplicates in files. Enter your filenames and wait for "Done!!!" text to show.
- Frequency functionality is for looking how many times a word is used. Specify filename and when it is done look for ```dataset/frequency.txt``` file.

https://github.com/alpertunga-bile/prompt-markdown-parser/assets/76731692/bea3a31a-70c7-4712-ada2-8533ad2fb27f

## Create Menu
- In the create menu, you have to give dataset path. So how to create dataset file? It is quite easy actually, go to CivitAi site and find images you like. Then copy their link and paste in a txt file. 
- Then specify positive filename. If you have already positive dataset you can specify it too but it has to be under the dataset folder.
- Then specify negative filename. If you have already negative dataset you can specify it too but it has to be under the dataset folder.
- You can write with or without file extensions.
- Aftert that wait for progress bar to finish and ```DONE !!!``` text on the terminal.

https://github.com/alpertunga-bile/prompt-markdown-parser/assets/76731692/9088dcd5-f83f-4cca-922e-3bf1e5023ebc

## Train Menu
- Give your dataset path. Which can be your positive or negative datasets. Not the links dataset.
- Enter your model name for example ```gpt2```. You can found the [model names](https://huggingface.co/models?pipeline_tag=text-generation). If you are going to use this site, write all the model names for example ```bigscience/bloom-560m```.
- Enter epochs.
- Enter batch size.
- Enter model save folder name. The model is going to save under dataset folder. So just right the name of the folder you want to save.
- Wait for ```DONE!!!``` text on the terminal.

https://github.com/alpertunga-bile/prompt-markdown-parser/assets/76731692/fccdcf1a-d9cc-4def-ad06-ee0f6901102d

## Evaluate Menu
- Give your dataset path. Which can be your positive or negative datasets. Not the links dataset.
- Enter your model name for example ```gpt2```. You can found the [model names](https://huggingface.co/models?pipeline_tag=text-generation). If you are going to use this site, write all the model names for example ```bigscience/bloom-560m```.
- Enter the model path.
- Wait for ```Evaluation Score (Loss)``` text on the terminal.

https://github.com/alpertunga-bile/prompt-markdown-parser/assets/76731692/74bad6c4-6122-464c-9825-3afed7266301

## Generate Menu
- Enter your model name for example ```gpt2```. You can found the [model names](https://huggingface.co/models?pipeline_tag=text-generation). If you are going to use this site, write all the model names for example ```bigscience/bloom-560m```.
- Enter the model path.
- Enter the minimum length that your generator can generate.
- Enter the maximum length that your generator can generate.
- Choose if you want do sample functionality.
- Choose if you want early stopping functionality.
- Specify recursive level.
- Choose if you want self recursive functionality.

### How Recursive Works?
- Let's say we give ```a, ``` as seed and recursive level is 1. I am going to use the same outputs for this example to understand the functionality more accurately.
- With self recursive, let's say generator's output is ```b```. So next seed is going to be ```b``` and generator's output is ```c```. Final output is ```a, c```. It can be used for generating random outputs.
- Without self recursive, let's say generator's output is ```b```. So next seed is going to be ```a, b``` and generator's output is ```a, b, c```. Final output is ```a, b, c```. It can be used for more accurate prompts.

- Now there are 6 commands you can use. These are generate, set, print, clear, cls and exit commands. clear and cls commands are clearing the terminal and exit command is return you to CLI applications main menu.

### Generate Menu
- In the generate menu, you can enter seed and get the generated text.

### Set Menu
- You can choose a variable to set its value. You can choose the variables that you specify before except model name and model path.

### Print Menu
- Print the current variables values.

https://github.com/alpertunga-bile/prompt-markdown-parser/assets/76731692/e63ea356-cc34-4ddf-99f3-a19e953374d4

# GUI Application

- Start the application with ```python start.py --gui``` command. This command is going to look for 'venv' file for virtual environment. It is going to setup the dependencies and start the application. After the first setup, it is just going to start the GUI application.

## Parser Tab
- You can choose ***Translate Prompts*** checkbox to translate your prompts to English. You can write prompts in a mixture of English and your native language. GoogleTranslator is used for translation. This checkbox works with ***Parse All Files In 'prompts' Folder*** and ***Parse And Save*** functionalities.
- ***Parse All Files In 'prompts' Folder*** button is getting all markdown files under 'prompts' folder which is located in repo directory and parse and save them.
- ***Select Prompt Files*** button is going to show a window to let you select your Markdown files. You can choose multiple files.
- After the selection press ***Parse And Save*** button and it's done. You can find your text files in the folder where are your selected Markdown files. You can see that it seperates negative and positive prompts with ***_negative*** and ***_positive*** names.
- DO NOT EDIT ***Positive Prompts*** and ***Negative Prompts*** strings in Markdown files. These are used to seperate prompts. You can add or reduce # symbol but do not edit the strings.
- DO NOT ADD comma "," at the end of your rows. Parser is adding for you.

https://github.com/alpertunga-bile/prompt-markdown-parser/assets/76731692/0312764a-17bf-417a-a0d1-fee876f37129

## Dataset Tab
- Save prompt links in a txt file. Just select image from CivitAi and copy and paste its link into a txt file. 
- Choose your link dataset which is provided in txt file.
- Write positive and negative filenames as you want to name them.
- Click ***Create Dataset*** button and wait. You can watch the progress with progressbar in GUI and in terminal.

https://github.com/alpertunga-bile/prompt-markdown-parser/assets/76731692/d157c9fe-18fa-49e6-ad04-ac0e7a16be79

## Civitai Tab
- Locate ```wantedPrompts.txt``` and ```unwantedPrompts.txt``` files under dataset folder and change for wanted and unwanted prompts. Seperate your prompts with comma.
- Give positive and negative filenames for dataset. Do not give path. Files are going to be created in dataset folder.
- Select attributes.
- Select ```All``` for NSFW if you want to get all images.
- Click ```Enhance``` button and wait for loading bar to complete in terminal then check dataset folder.

https://github.com/alpertunga-bile/prompt-markdown-parser/assets/76731692/2cd21df4-b886-43ea-9d32-2cb8988c2dad

## Train Tab
- Enter your model name. You can found the [model names](https://huggingface.co/models?pipeline_tag=text-generation).
- Enter epochs, batch size.
- Enter folder name for your model. Your model is going to be saved into 'dataset' folder.
- Choose dataset to train with model.
- Click ***Train*** button and wait for ***Done!!!*** text to appear above the button.

https://github.com/alpertunga-bile/prompt-markdown-parser/assets/76731692/d7540867-3799-4782-a95e-c3dec0a17b32

## Evaluate Tab
- Choose your dataset which is used for training.
- Enter your model name that you used for training. DO NOT enter the folder name of your model.
- Choose your model's saved folder.
- Click ***Evaluate*** button and wait for a ***Evaluation score*** output above the button.

https://github.com/alpertunga-bile/prompt-markdown-parser/assets/76731692/5fae56b9-7bdd-48f0-b618-5591319b62ab

## Generate Tab
- Enter your model name that you used for training. DO NOT enter the folder name of your model.
- Choose your model's saved folder.
- Enter min length that model can generate.
- Enter max length that model can generate.
- Tick the checkboxes if you want these features.
- Set recursive level with slider. It is going to give model the previous result in each step.
- Select if you want self recursive.
- Enter your seed and click ***Generate Text*** button and wait for text to be appeared in the textbox.

https://github.com/alpertunga-bile/prompt-markdown-parser/assets/76731692/05bfd9ab-4624-4a39-bc21-d129edf2e06b

### How Recursive Works?
- Let's say we give ```a, ``` as seed and recursive level is 1. I am going to use the same outputs for this example to understand the functionality more accurately.
- With self recursive, let's say generator's output is ```b```. So next seed is going to be ```b``` and generator's output is ```c```. Final output is ```a, c```. It can be used for generating random outputs.
- Without self recursive, let's say generator's output is ```b```. So next seed is going to be ```a, b``` and generator's output is ```a, b, c```. Final output is ```a, b, c```. It can be used for more accurate prompts.

# Examples
## Parser Example
- You can access the [Markdown file](https://github.com/alpertunga-bile/prompt-markdown-parser/blob/master/example/example.md) that is used for the below image.
- Image is upscaled with [AIUpscaleGUI](https://github.com/alpertunga-bile/AIUpscaleGUI) project.

![00069-3749032177_out](https://user-images.githubusercontent.com/76731692/233834377-0b2b717b-5301-4672-93d4-0d8a56d68a88.png)

## Generator Examples
- Some typo fixes are done for the generated prompts.
- female_positive_gpt2-75_model is used for generator examples. Pretrained generator models can be found [here](https://drive.google.com/drive/folders/1c21kMH6FTaia5C8239okL3Q0wJnnWc1N?usp=share_link).
- The model is trained with 75 epochs and 1 batch size.

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
