from similarity import *
from models import *
def individualWords():
    """Compares two words"""
    s1 = input("String to compare: ")
    s2 = input("Compare with: ")
    methods = {"1": CosineSimilarity, "2": PMI, "3": WordEmbedding}
    print("Comparison Methods:")
    for key, value in methods.items():
        print(key + ": " + value.__name__)
    method = input()
    if method == '1' or method == '2':
        # link = input("Link to index: ")
        link = "ielab:KVVjnWygjGJRQnYmgAd3CsWV@ielab-pubmed-index.uqcloud.net"
        input_fields = input("Fields to use (space separated): ")
        if input_fields == "":
            fields = None
        else:
            fields = input_fields.split(" ")
        index = Index(link + ":80", fields)
    if method == '1':
        print(index.similarity(method, s1, s2))
    if method == '2':
        radius = input("Radius? (press enter for whole doc)")
        print(index.similarity(method, s1, s2, radius))
    if method == '3':
        wv = Word2Vec("PubMed.bin")
        print(index.similarity(method, s1, s2))

def fromFile(document, column1, column2):
    """Compares pairs of words in a file"""
    filein = open(document, "r")
    fileout = open("similarity", "w+")

    methods = {"1": CosineSimilarity, "2": PMI, "3": WordEmbedding}
    print("Comparison Methods:")
    for key, value in methods.items():
        print(key + ": " + value.__name__)
    methodInput = input()
    method = methods.get(methodInput)
    if methodInput == '1' or methodInput == '2':
        # link = input("Link to index: ")
        link = "ielab:KVVjnWygjGJRQnYmgAd3CsWV@ielab-pubmed-index.uqcloud.net"
        input_fields = input("Fields to use (space separated): ")
        if input_fields == "":
            fields = None
        else:
            fields = input_fields.split(" ")
        index = Index(link + ":80", fields)
    if methodInput == '1':
        for line in filein:
            items = line.strip().split("\t")
            similarity = index.similarity(method, items[column1], items[column2])
            fileout.write(items[column1] + "\t" + items[column2] + "\t" + str(similarity) + "\n")

    if methodInput == '2':
        radius = input("Radius? (press enter for whole doc)")
        for line in filein:
            items = line.strip().split("\t")
            similarity = index.similarity(method, items[column1], items[column2], radius)
            fileout.write(items[column1] + "\t" + items[column2] + "\t" + str(similarity) + "\n")

    if methodInput == '3':
        wv = Word2Vec("PubMed.bin")
        for line in filein:
            items = line.strip().split("\t")
            similarity = index.similarity(method, items[column1], items[column2])
            fileout.write(items[column1] + "\t" + items[column2] + "\t" + str(similarity) + "\n")


def main():
    fromFile("caviedes_removed.txt", 0, 1)


if __name__ == "__main__" :
    main()
