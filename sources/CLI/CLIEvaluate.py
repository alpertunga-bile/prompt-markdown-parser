from os.path import exists


class CLIEvaluate:
    def Start(self):
        datasetPath = input("Evaluate> Dataset Path : ")
        while exists(datasetPath) is False:
            print(f"Evaluate> {datasetPath} is not exists. Please enter a valid path!")
            datasetPath = input("Evaluate> Dataset Path : ")

        modelName = input("Evaluate> Model Name (E.g. gpt2) : ")
        modelPath = input("Evaluate> Model Folder Path : ")

        while exists(modelPath) is False:
            print(f"Evaluate> {modelPath} is not exists. Please enter a valid path!")
            modelPath = input("Evaluate> Model Folder Path : ")

        self.Evaluate(datasetPath, modelPath, modelName)

    def Evaluate(self, datasetPath: str, modelPath: str, modelName: str):
        upperModelName = modelName.upper()

        if modelName.find("/") != -1:
            upperModelName = modelName.split("/")[1].upper()

        from happytransformer import HappyGeneration

        model = HappyGeneration(upperModelName, modelName, load_path=modelPath)
        result = model.eval(datasetPath)

        print(f"Evaluate> Evaluation Score (Loss) : {result.loss}")
