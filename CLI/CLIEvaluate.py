from os.path import exists

class CLIEvaluate:
    modelName = ""
    modelPath = ""
    datasetPath = ""

    def Start(self):
        self.datasetPath = input("Evaluate> Dataset Path : ")
        while exists(self.datasetPath) is False:
            print(f"Evaluate> {self.datasetPath} is not exists. Please enter a valid path!")
            self.datasetPath = input("Evaluate> Dataset Path : ")
        self.modelName = input("Evaluate> Model Name (E.g. gpt2) : ")
        self.modelPath = input("Evaluate> Model Folder Path : ")
        while exists(self.modelPath) is False:
            print(f"Evaluate> {self.modelPath} is not exists. Please enter a valid path!")
            self.modelPath = input("Evaluate> Model Folder Path : ")
        self.Evaluate()

    def Evaluate(self):
        upperModelName = self.modelName.upper()

        if self.modelName.find("/") != -1:
            upperModelName = self.modelName.split("/")[1].upper()

        from happytransformer import HappyGeneration

        model = HappyGeneration(upperModelName, self.modelName, load_path=self.modelPath)
        result = model.eval(self.datasetPath)
        print(f"Evaluate> Evaluation Score (Loss) : {result.loss}")