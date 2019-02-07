
import numpy as np
from scipy import spatial
from elasticsearch import Elasticsearch,helpers
import math
from scipy import sparse
from gensim.test.utils import datapath
from gensim.models import Word2Vec
from gensim.models import KeyedVectors


class Index():
    """An index of the documents used. Stores information about documents and terms"""
    def __init__(self, url, fields, ids = None):
        """Constructs an index

        :param url: the url for the Elasticsearch index
        :param fields: list of fields in the documents to be used for comparison
        :param ids: list of ids used for comparison
        """
        self.es = Elasticsearch([url])
        self.res = self.es.search()
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

    def createDocuments(selfc):
        """Generates all documents in the index"""
        vectors = self.es.mtermvectors(index='med', doc_type='_doc',
                            body=dict(ids=self.ids, parameters=dict(offsets = 'false', payloads = 'false', fields=self.fields)))
        for doc in vectors['docs']:
            self.docs.append(Document(doc, self.fields))

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

class Document():
    """A single document in the index"""
    def __init__(self, vector, fields):
        """
        Constructs a document
        :param vector: The termvector for the document
        :param fields: the fields used in the document
        """
        self.vector = vector
        self.id = vector.get('_id')
        self.terms = {}
        self.generateTerms(fields)

    def generateTerms(self, fields):
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
                for positions in doc.terms[word].positions.values():
                    count += len(positions)
        return count
    def getMutualFrequency(self, s1, s2):
        """Returns the number of times s1 and s2 appear together"""
        count = 0
        for doc in self.docs:
            if s1 in doc.terms:
                for field in doc.terms.get(s1).positions:
                    for position1 in doc.terms.get(s1).positions[field]:
                        if s2 in doc.terms and field in doc.terms.get(s2).positions:
                            for position2 in doc.terms.get(s2).positions[field]:
                                print(position2['position'], position1['position'])
                                if position2['position'] > position1['position'] - self.radius \
                                        and position2['position'] < position1['position'] + self.radius:
                                    count = count + 1
                                    break
        return count

    def getDocumentFrequency(self, word):
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

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Term):
            return self.name == other.name and self.termFreq == other.termFreq and self.docFreq == other.docFreq
        return False


class WordVector():
    """A word2vec model of the documents"""
    def __init__(self, file):
        self.wv = KeyedVectors.load_word2vec_format(datapath(file), binary=True)