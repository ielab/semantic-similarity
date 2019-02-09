from abc import ABC, abstractmethod
from scipy.stats.stats import pearsonr, spearmanr
class Correlation():
    def __init__(self, document1, column1, document2, column2):
        self.vector1 = self.createVector(document1, column1)
        self.vector2 = self.createVector(document2, column2)

    def createVector(self, document, column):
        vec = []
        file = open(document, "r")
        for line in file:

            items = line.strip().split("\t")
            vec.append(float(items[column]))
        return vec
    def calculatePerson(self):
        return pearsonr(self.vector1, self.vector2)

    def calculateSpearman(self):
        return spearmanr(self.vector1, self.vector2)

def main():
    c = Correlation("caviedes_removed.txt", 4, "caviedes_removed.txt", 4)
    print(c.calculatePerson())


if __name__ == "__main__" :
    main()