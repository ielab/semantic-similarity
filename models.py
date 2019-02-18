from abc import ABC, abstractmethod
from elasticsearch import Elasticsearch,helpers
import math
from gensim.test.utils import datapath
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from similarity import VecSim, WordSim, CosineSimilarity, PMI

class Collection(ABC):
    @abstractmethod
    def similarity(self, method, s1, s2):
        pass

class Index(Collection):
    """An index of the documents used. Stores information about documents and terms"""
    def __init__(self, url = None, fields = None, ids = None):
        """Constructs an index
        :param url: the url for the Elasticsearch index
        :param fields: list of fields in the documents to be used for comparison
        :param ids: list of ids used for comparison
        """
        try:
            self.es = Elasticsearch([url])
            self.res = self.es.search()
        except:
            print("Please use another url")
            return

        self.fields = fields
        if fields == None:
            self.fields = ['*']
        if ids == None:
            self.ids = self.getIds()
        else:
            self.ids = ids
        self.docs = []
        self.createDocuments()
    def getIds(self):
        """Returns the ids of all documents in the index"""
        matches = helpers.scan(self.es, query={"query": {"match_all": {}}}, scroll='1m', index="med")
        ids = []
        # i = 0
        for match in matches:
            ids.append(match['_id'])
            # i += 1
            # if i == 100:
            #     break
        return ids

    def getFields(self):
        """Returns all fields that exist in the index"""
        fields = []
        for doc in self.res.get("hits").get("hits"):
            for field in doc.get("_source"):
                if field not in fields:
                    fields.append(field)
        return fields

    def createDocuments(self):
        """Generates all documents in the index"""
        vectors = self.es.mtermvectors(index='med', doc_type='_doc',
                            body=dict(ids=self.ids, parameters=dict(offsets = 'false', payloads = 'false', fields=self.fields)))
        for doc in vectors['docs']:
            self.docs.append(Document(doc))

    def getTermVector(self, word):
        """
        Creates a term vector for the input word
        :param word: the word to get the term vector for
        :return: the vector, as a list of numbers
        """
        vector = []
        docCount = 0
        for doc in self.docs:
            if word in doc.terms:
                docCount += 1
        for doc in self.docs:
            if word in doc.terms:
                vector.append(doc.terms.get(word).calculateTfidf(len(self.docs), docCount))
            else:
                vector.append(0)
        return vector
    def getSumFrequency(self):
        """Returns the total number of words in the index"""
        count = 0
        for doc in self.docs:
            for term in doc.terms.values():
                count += term.termFreq
        return count

    def getTermFrequency(self, word):
        """Returns the number of times the word appears in the index"""
        count = 0
        for doc in self.docs:
            if word in doc.terms:
                count += doc.terms[word].termFreq
        return count
    def getMutualFrequency(self, s1, s2, radius):
        """Returns the number of times s1 and s2 appear together"""
        count = 0
        for doc in self.docs:
            if s1 in doc.terms:
                for field in doc.terms.get(s1).positions:
                    for position1 in doc.terms.get(s1).positions[field]:
                        if s2 in doc.terms and field in doc.terms.get(s2).positions:
                            for position2 in doc.terms.get(s2).positions[field]:
                                if position2['position'] > position1['position'] - radius \
                                        and position2['position'] < position1['position'] + radius:
                                    count = count + 1
        return count

    def getDocuments(self, word):
        """Returns a list of documents in which the word appears"""
        docs = []
        for doc in self.docs:
            if word in doc.getTerms():
                docs.append(doc.id)
        return docs

    def getMutualDocuments(self, d1, d2):
        """
        returns a list of doc ids that are in both d1 and d2
        :param d1: List containing documents containing the first word
        :param d2: List containing documents containing the second word
        :return: list of doc ids that are in both d1 and d2
        """
        return list(set(d1).intersection(d2))

    def similarity(self, method, s1, s2):
        """
        calculates the similarity of two words in the collection
        :param method: the similarity method to use
        :param s1: the first string to compare
        :param s2: the second string to compare
        :return: the similarity
        """
        if(isinstance(method, VecSim)):
            return method.calculateSimilarity(self.getTermVector(s1), self.getTermVector(s2))
        if(isinstance(method, WordSim)):
            if method.radius == None:
                d1 = self.getDocuments(s1)
                d2 = self.getDocuments(s2)
                d12 = self.getMutualDocuments(d1, d2)
                D = len(self.docs)
                f1 = len(d1)
                f2 = len(d2)
                f12 = len(d12)

            else:
                f1 = self.getTermFrequency(s1)
                f2 = self.getTermFrequency(s2)
                D = self.getSumFrequency()
                f12 = self.getMutualFrequency(s1, s2, method.radius)
            return method.calculateSimilarity(D, f1, f2, f12)

class Document():
    """A single document in the index"""
    def __init__(self, vector):
        """
        Constructs a document
        :param vector: The termvector for the document
        :param fields: the fields used in the document
        """
        self.vector = vector
        self.id = vector.get('_id')
        self.terms = {}
        self.generateTerms()

    def generateTerms(self):
        """Generates Terms for the terms in the specified fields"""
        for field in self.vector.get("term_vectors"):
            allTerms = self.vector.get("term_vectors").get(field).get("terms")
            for name in allTerms:
                if name not in self.terms:
                    self.terms[name] = Term(name, allTerms[name].get("term_freq"), allTerms[name].get("tokens"), field)
                else:
                    self.terms[name].update(allTerms[name].get("term_freq"), allTerms[name].get("tokens"), field)

    def getTerms(self):
        """returns the dictionary of terms in the document"""
        return self.terms

class Term():
    """A single term in a Document"""

    def __init__(self, name, termFreq, tokens, field):
        """
        Constructs a term
        :param name: the word
        :param termFreq: how many times the term appears in the field
        :param tokens: the positions of the term
        :param field: the field the term is in
        """
        self.name = name
        self.termFreq = termFreq
        self.positions = {field: tokens}

    def calculateTfidf(self, sumDocFreq, docCount):
        """
        Calculates the tf-idf of the term
        :param sumDocFreq: The number of docs the term appears in
        :param docCount: the total number of docs
        :return: the tf-idf
        """
        return self.termFreq * math.log(sumDocFreq/docCount, 10)

    def update(self, termFreq, tokens, field):
        """updates the statistics for the term if the term already exists"""
        self.termFreq += termFreq
        self.positions[field] = tokens

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Term):
            return self.name == other.name and self.termFreq == other.termFreq and self.positions == other.positions
        return False

class WordVector(Collection):
    """A word2vec model of the documents"""
    def __init__(self, file):
        """creates a word2vec model from a binary file"""
        self.wv = KeyedVectors.load_word2vec_format(file, binary=True)

    def similarity(self, method, s1, s2):
        """
        calculates the similarity of two words in the collection
        :param method: the similarity method to use
        :param s1: the first string to compare
        :param s2: the second string to compare
        :return: the similarity
        """
        if(isinstance(method, VecSim)):
            return method.calculateSimilarity(self.wv.wv[s1].tolist(), self.wv.wv[s2].tolist())