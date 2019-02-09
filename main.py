from similarity import *
def individualWords():
    s1 = input("String to compare: ")
    s2 = input("Compare with: ")
    methods = {"1": DocCos, "2": PMI, "3": WordEmbedding}
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
        print(methods.get(method)(s1, s2, index).getSimilarity())
    if method == '2':
        radius = input("Radius? (press enter for whole doc)")
        print(methods.get(method)(s1, s2, index, radius).getSimilarity())
    if method == '3':
        wv = WordVector("PubMed.bin")
        print(methods.get(method)(s1, s2, wv).getSimilarlity())

def fromFile(document, column1, column2):
    filein = open(document, "r")
    fileout = open("similarity", "w+")

    methods = {"1": DocCos, "2": PMI, "3": WordEmbedding}
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
        for line in filein:
            items = line.strip().split("\t")
            similarity = methods.get(method)(items[column1], items[column2], index).getSimilarity()
            fileout.write(items[column1] + "\t" + items[column2] + "\t" + str(similarity) + "\n")

    if method == '2':
        radius = input("Radius? (press enter for whole doc)")
        for line in filein:
            items = line.strip().split("\t")
            similarity = methods.get(method)(items[column1], items[column2], index, radius).getSimilarity()
            fileout.write(items[column1] + "\t" + items[column2] + "\t" + str(similarity) + "\n")

    if method == '3':
        wv = WordVector("PubMed.bin")
        for line in filein:
            items = line.strip().split("\t")
            similarity = methods.get(method)(items[column1], items[column2], wv).getSimilarlity()
            fileout.write(items[column1] + "\t" + items[column2] + "\t" + str(similarity) + "\n")


def main():
    fromFile("caviedes_removed.txt", 0, 1)


if __name__ == "__main__" :
    main()
