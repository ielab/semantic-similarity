from similarity import *
from models import *


def fromFile(document, column1, column2, method, collection):
    """Compares pairs of words in a file"""
    filein = open(document, "r")
    fileout = open("similarity", "w+")
    for line in filein:
        items = line.strip().split("\t")
        similarity = collection.similarity(method, items[column1], items[column2])
        fileout.write(items[column1] + "\t" + items[column2] + "\t" + str(similarity) + "\n")


def main():
    pass


if __name__ == "__main__" :
    main()
