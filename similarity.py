from abc import ABC, abstractmethod
from scipy import spatial
from elasticsearch import Elasticsearch
import math
class Index():
    def __init__(self, url):
        self.es = Elasticsearch([url])
        self.ids = self.getIds()
        self.createDocuments()

    def getIds(self):
        res = self.es.search()
        ids = []
        for doc in res.get("hits").get("hits"):
            ids.append(doc.get("_id"))
        return ids


    def createDocuments(self):
        self.docs = []
        for doc in self.ids:
            vector = self.es.termvectors(index="med", doc_type='_doc', id=doc, fields=["abstract"], term_statistics="true")
            self.docs.append(Document(doc, self.es))

    def getTermVector(self, word):
        vector = []
        for doc in self.docs:
            if word in doc.terms:
                vector.append(doc.terms.get(word).calculateTfidf(doc.sumDocFreq))
            else:
                vector.append(0)
        return vector

class Document():
    def __init__(self, doc, es):
        self.vector = es.termvectors(index="med", doc_type='_doc', id=doc, fields=["abstract"], term_statistics="true")
        self.sumDocFreq = self.vector.get("term_vectors").get("abstract").get("field_statistics").get("sum_doc_freq")
        self.terms = {}
        self.generateTerms()

    def generateTerms(self):
        allTerms = self.vector.get("term_vectors").get("abstract").get("terms")
        for name in allTerms:
            self.terms[name] = Term(name, allTerms[name].get("term_freq"), allTerms[name].get("doc_freq"))

class Term():

    def __init__(self, name, termFreq, docFreq):
        self.name = name
        self.termFreq = termFreq
        self.docFreq = docFreq

    def calculateTfidf(self, sumDocFreq):
        return self.termFreq * math.log(sumDocFreq/self.docFreq, 10)

class Similarity(ABC):


    @abstractmethod
    def __init__(self, s1, s2, index):
        self.s1 = s1
        self.s2 = s2
        self.index = index
        
    @abstractmethod
    def calculateSimilarity(self):
        pass


class DocCos(Similarity):

    def __init__(self, s1, s2, index):
        super().__init__(s1, s2, index)
        self.v1 = index.getTermVector(s1)
        self.v2 = index.getTermVector(s2)
        self.calculateSimilarity()

    def calculateSimilarity(self):
        self.similarity = 1 - spatial.distance.cosine(self.v1, self.v2)

    def getSimilarity(self):
        return self.similarity

class PMI(Similarity):
    def __init__(self, s1, s2, index):
        super().__init__(s1, s2, index)

    def calculateSimilarity(self):
        print("+PMI!")


def main():
    index = Index("ielab:KVVjnWygjGJRQnYmgAd3CsWV@ielab-pubmed-index.uqcloud.net:80")
    Cos = DocCos("the", "antiaggressive", index)
    print(Cos.getSimilarity())


if __name__ == "__main__" :
    main()
