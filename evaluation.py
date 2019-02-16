from abc import ABC, abstractmethod
from scipy.stats.stats import pearsonr, spearmanr
class Correlation():
    """Evaluates the correlation between two different sets of similarities"""
    def __init__(self, document1, column1, document2, column2):
        """
        constructor for correlation
        :param document1: file with a list of similarity values, one on each line all in the same column
        :param column1: the column number that the similarity values are in. First column is 0
        :param document2: the second file with list of similarities. Has to be in the same order as document1
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
    def calculatePearson(self):
        """calculates pearson coefficient between two vectors"""
        return pearsonr(self.vector1, self.vector2)

    def calculateSpearman(self):
        """calculate spearman coefficient between two vectors"""
        return spearmanr(self.vector1, self.vector2)[0]

def main():
    print("Evaluation method: ")
    print("1: Pearson" + "\n" + "2: Spearman")
    method = input("Enter number corresponding to desired method: ")
    d1 = input("File with the first list of similarities: ")
    c1 = input("Column index of similarities to evaluate (index starts at 0): ")
    d2 = input("File with the second list of similarities: ")
    c2 = input("Column index of similarities to evaluate (index starts at 0): ")
    try:
        correlation = Correlation(d1, c1, d2, c2)
        if method == "1":
            print("Correlation" + correlation.calculatePearson())
        elif method == "2":
            print("Correlation" + correlation.calculateSpearman())
    except:
        print("Something went wrong! Please try again with different files or columns")
if __name__ == "__main__" :
    main()