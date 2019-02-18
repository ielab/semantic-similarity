from similarity import *
from models import *


def fromFile(document, column1, column2, method, collection):
    """Compares pairs of words in a file"""
    filein = open(document, "r")
    fileout = open("similarity.txt", "w+")
    for line in filein:
        items = line.strip().split("\t")
        similarity = collection.similarity(method, items[column1], items[column2])
        fileout.write(items[column1] + "\t" + items[column2] + "\t" + str(similarity) + "\n")


def main():

    methods = {"1": CosineSimilarity, "2": PMI}
    print("Comparison Methods:")
    for key, value in methods.items():
        print(key + ": " + value.__name__)
    methodNo = input("Enter number corresponding to desired method: ")
    if methodNo == '1':
        collections = {"1": Index, "2": WordVector}
        print("Collections:")
        for key, value in collections.items():
            print(key + ": " + value.__name__)
        collectionNo = input("Enter number corresponding to desired collection: ")
        if collectionNo == '1':
            link = input("Link to index: ")
            inputFields = input("Fields to use (space separated), leave blank for all: ")
            if inputFields == "":
                fields = None
            else:
                fields = inputFields.split(" ")
            ids = input("Ids to use (space separated), leave blank for all: ")
            collection = Index(link + ":80", fields, ids)
        elif collectionNo == '2':
            file = input("word2vec model to use (must be binary file): ")
            collection = WordVector(file)
        method = methods[methodNo]()

    if methodNo == '2':
        link = input("Link to index: ")
        inputFields = input("Fields to use (space separated), leave blank for all: ")
        if inputFields == "":
            fields = None
        else:
            fields = inputFields.split(" ")
        ids = input("Ids to use (space separated), leave blank for all: ")
        collection = Index(link + ":80", fields, ids)
        radius = input("Radius to use (space separated), leave blank for all: ")
        method = methods[methodNo](int(radius))
    file = input("Document with word pairs: ")
    c1 = input("Column index of words to compare (index starts at 0): ")
    c2 = input("Column index of words to compare to (index starts at 0): ")
    try:
        fromFile(file, int(c1), int(c2), method, collection)
        print("Done! Find results in similarity.txt")
    except:
        print("Something went wrong! Please try again with different inputs.")

if __name__ == "__main__" :
    main()
