from abc import ABC, abstractmethod
from scipy import spatial
from elasticsearch import Elasticsearch,helpers
import math
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
import numpy as np

class Index():
    def __init__(self, url, fields, ids = None):
        self.es = Elasticsearch([url])
        self.res = self.es.search()
        self.fields = fields
        if fields == None:
            self.fields = ['*']
        self.ids = self.getIds()
        self.docs = []
        self.createDocuments()

    def getIds(self):
        matches = helpers.scan(self.es, query={"query": {"match_all": {}}}, scroll='1m', index="med")  # like others so far
        ids = []
        for match in matches:
            ids.append(match['_id'])
        return ids

    def getFields(self):
        fields = []
        for doc in self.res.get("hits").get("hits"):
            for field in doc.get("_source"):
                if field not in fields:
                    fields.append(field)
        return fields

    def createDocuments(self):
        c = 0
        for doc in self.ids:
            vector = self.es.termvectors(index="med", doc_type='_doc', id=doc, fields=self.fields, term_statistics="true",
                    offsets = 'false', payloads = 'false')
            c = c + 1
            self.docs.append(Document(vector, self.fields, doc))

    def getTermVector(self, word):
        vector = []
        for doc in self.docs:
            if word in doc.terms:
                vector.append(doc.terms.get(word).calculateTfidf(doc.sumDocFreq))
            else:
                vector.append(0)
        return vector

class Document():
    def __init__(self, vector, fields, doc):
        self.vector = vector
        self.id = doc
        self.sumDocFreq = 0
        for field in fields:
            if field in self.vector.get("term_vectors"):
                self.sumDocFreq += self.vector.get("term_vectors").get(field).get("field_statistics").get("sum_doc_freq")
        self.terms = {}
        self.generateTerms(fields)

    def generateTerms(self, fields):
        for field in fields:
            if field in self.vector.get("term_vectors"):
                allTerms = self.vector.get("term_vectors").get(field).get("terms")
                for name in allTerms:
                    if name not in self.terms:
                        self.terms[name] = Term(name, allTerms[name].get("term_freq"), allTerms[name].get("doc_freq"), allTerms[name].get("tokens"), field)
                    else:
                        self.terms[name].update(allTerms[name].get("term_freq"), allTerms[name].get("doc_freq"), allTerms[name].get("tokens"), field)

    def getTerms(self):
        return self.terms

class Term():

    def __init__(self, name, termFreq, docFreq, tokens, field):
        self.name = name
        self.termFreq = termFreq
        self.docFreq = docFreq
        self.positions = {field: tokens}

    def calculateTfidf(self, sumDocFreq):
        return self.termFreq * math.log(sumDocFreq/self.docFreq, 10)

    def update(self, termFreq, docFreq, tokens, field):
        self.termFreq += termFreq
        self.docFreq += docFreq
        self.positions[field] = tokens
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Term):
            return self.name == other.name and self.termFreq == other.termFreq and self.docFreq == other.docFreq
        return False

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
        array = np.array([self.v1, self.v2])
        array_sparse = sparse.csr_matrix(array)
        self.similarity = cosine_similarity(array_sparse)

    def getSimilarity(self):
        return self.similarity[0][1]

class PMI(Similarity):
    def __init__(self, s1, s2, index, radius = 0):
        super().__init__(s1, s2, index)
        self.similarity = 0
        self.calculateSimilarity()

    def calculateSimilarity(self):
        d1 = self.getDocumentFrequency(self.s1)
        d2 = self.getDocumentFrequency(self.s2)
        d12 = self.getMutualDocuments(d1, d2)
        D = len(self.index.docs)
        f1 = len(d1)
        f2 = len(d2)
        f12 = len(d12)
        try:
            self.similarity = max(0, math.log((f12 * D )/ (f1 * f2), 2))
        except:
            print("error: one of the words does not exist in index")
        #self.similarity = math.log(f12 / (f1 * (f2 / D) + (math.sqrt(f1 * 0.23))))
    def calculateSimilarityRange(self):
        pass

    def getTermFrequency(self, word):
        count = 0
        for doc in self.index.docs:
            if word in doc.getTerms:
                for positions in doc.getTerms.get(word).positions.values():
                    count += len(positions)
        return count

    def getDocumentFrequency(self, word):
        docs = []
        for doc in self.index.docs:
            if word in doc.getTerms():
                docs.append(doc.id)
        return docs

    def getMutualDocuments(self, d1, d2):
        return list(set(d1).intersection(d2))

    def getSimilarity(self):
        return self.similarity
def main():
    #link = input("Link to index: ")
    link = "ielab:KVVjnWygjGJRQnYmgAd3CsWV@ielab-pubmed-index.uqcloud.net"
    input_fields = input("Fields to use (space separated):")
    if input_fields == "":
        fields = None
    else:
        fields = input_fields.split(" ")
    index = Index(link + ":80", fields)
    s1 = input("String to compare: ")
    s2 = input("Compare with: ")
    methods = {"1": DocCos, "2": PMI}
    print("Comparison Methods:")
    for key, value in methods.items():
        print(key + ": " + value.__name__)
    method = input()
    print(methods.get(method)(s1, s2, index).getSimilarity())

if __name__ == "__main__" :
    main()
