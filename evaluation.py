from abc import ABC, abstractmethod
from scipy.stats.stats import pearsonr, spearmanr
class Correlation():
    """Evaluates the correlation between two different sets of similarities"""
    def __init__(self, document1, column1, document2, column2):
        """
        constructor for correlation
        :param document1: file with a list of similarity values, one on each line all in the same column
        :param column1: the column number that the similarity values are in. First column is 0
        :param document2: the second file with list of similarities. Has to be in the same order as documnet1
        :param column2: column number for document2
        """
        self.vector1 = self.createVector(document1, column1)
        self.vector2 = self.createVector(document2, column2)

    def createVector(self, document, column):
        """reads the similarity values from a file and puts it in a vector"""
        vec = []
        file = open(document, "r")
        for line in file:
            items = line.strip().split("\t")
            vec.append(float(items[column]))
        return vec
    def calculatePerson(self):
        """calculates pearson coefficient between two vectors"""
        return pearsonr(self.vector1, self.vector2)

    def calculateSpearman(self):
        """calculate spearman coefficient between two vectors"""
        return spearmanr(self.vector1, self.vector2)

def main():
    c = Correlation("caviedes_removed.txt", 1, "caviedes_removed.txt", 1)
    print(c.calculateSpearman())


if __name__ == "__main__" :
    main()