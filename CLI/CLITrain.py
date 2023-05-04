from os.path import exists

class CLITrain:
    modelName = ""
    epochs = 10
    batchSize = 1
    modelFolder = ""
    datasetPath = ""

    def Start(self):
        self.datasetPath = input("Dataset Path : ")
        while exists(self.datasetPath) is False:
            print(f"{self.datasetPath} is not exists. Please enter a valid path!")
            self.datasetPath = input("Dataset Path : ")
        self.modelName = input("Model Name (E.g. gpt2) : ")
        self.epochs = int(input("Epochs : "))
        self.batchSize = int(input("Batch Size : "))
        self.modelFolder = input("Model Save Folder : ")
        self.Train()

    def Train(self):
        upperModelName = self.modelName.upper()

        if self.modelName.find("/") != -1:
            upperModelName = self.modelName.split("/")[1].upper()

        model = None

        from happytransformer import HappyGeneration, GENTrainArgs

        if exists(self.modelFolder):
            model = HappyGeneration(upperModelName, self.modelName, load_path=self.modelFolder)
        else:
            model = HappyGeneration(upperModelName, self.modelName)

        args = GENTrainArgs(num_train_epochs=self.epochs, batch_size=self.batchSize)
        model.train(self.datasetPath, args=args)
        model.save(f"dataset/{self.modelFolder}")
        
        print("DONE!!!")