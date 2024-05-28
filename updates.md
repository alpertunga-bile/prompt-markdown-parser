# Updates (DD/MM/YY)

## Update Date : 28/05/2024
- Codebase is refactored
- Preprocess algorithms are updated

## Update Date : 28/01/2024
- The cursor updates in the CivitAITab and CLICivitai files are changed. If the nextCursor is not available in the json file, it adds to itself the total image count in the json file. The nextCursor is not available error may be occured if you do not use Newest for the sort variable so this update was made to fix this bug.

## Update Date : 18/11/2023
- CivitAI tab and CLI functionality is updated based on the update of the CivitAI REST API.
- Refactoring code base is done.

## Update Date : 17/07/2023
- Custom prompt generator node for ComfyUI is added. You can access the repository with [this link](https://github.com/alpertunga-bile/prompt-generator-comfyui).

## Update Date : 08/06/2023
- female_positive-gpt2-141972-5-1 prompt generator is added to Drive. Trained with gpt2 model, 141972 unique prompts, 5 epochs and 1 batch size.
- Improvements and bug fixes.
- [WebUI](https://github.com/alpertunga-bile/prompt-tools-webui) is added. You can use the same functionalities with upscale image functionality by [AIUpscale](https://github.com/alpertunga-bile/AIUpscaleGUI).

## Update Date : 19/05/2023
- Civitai Tab is added for GUI application.

## Update Date : 13/05/2023
- Civitai functionality is added.
- New texts have been added to understand what action is currently being taken.

## Update Date : 11/05/2023
- Virtual environment is gathered into one "venv" folder.

## Update Date : 04/05/2023
- CLI application is added.
- Auto-complete with ```TAB``` button functionality is added.
- Reinstalling environment, updating packages in the virtual environment and passing virtual environment check functionalities are added.
- Virtual environments are seperated.
- Importing module optimizations are done.

## Update Date : 03/05/2023
- Update packages inside virtual environment functionality is added with command line argument.
- Reinstalling virtual environment functionality is added with command line argument.
- Optimization is done for importing modules.

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