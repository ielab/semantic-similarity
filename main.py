from similarity import *
def main():

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

if __name__ == "__main__" :
    main()
