import pandas as pd
import matplotlib.pyplot as plt

class pandaExercise:

    cancerData = pd.Series()

    def readFromFile(self, fileName):
        names = ["Class", "age", "menopause", "tumor-size", "inv-nodes", "node-caps", "deg-malig", "breast",
                 "breast-quad",
                 "irradiat"]
        self.cancerData = pd.read_csv('breast-cancer.data', header=None, names=names)


    def getCount (self, columnName):
        print("Here is result of column \""+columnName+"\".")
        result = self.cancerData.value_counts(columnName)
        print(str(result))


    def maximum(self, columnName):
        countResult = self.cancerData.value_counts(columnName)
        print("The most common "+columnName+" is \""+countResult.index[0]+"\".")
        print("It was found in "+str(countResult.array[0])+" cases.")

    def draw(self, columnName):
        result = self.cancerData.groupby(columnName).aggregate(sum)
        result.plot(kind='bar')
        plt.show()

if __name__ == '__main__':
    # problem a
    exercise1 = pandaExercise()
    exercise1.readFromFile("breast-cancer.data")

    # problem b
    exercise1.getCount("Class")
    exercise1.maximum("Class")

    # problem c
    exercise1.maximum("age")
    exercise1.maximum("menopause")

    # problem d
    exercise1.draw("age")




