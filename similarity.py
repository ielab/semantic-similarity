from abc import ABC, abstractmethod

import numpy as np
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity
from models import *

class Similarity(ABC):
    """Abstract class for calculating similarity"""

    @abstractmethod
    def __init__(self, s1, s2):
        """
        constructs a similarity method
        :param s1: the first string to compare
        :param s2: the second string to compare
        :param index: the index to use
        """
        self.s1 = s1
        self.s2 = s2

    @abstractmethod
    def calculateSimilarity(self):
        """implementation for the specific similarity method"""
        pass


class CosineSimilarity(Similarity):
    """Document cosine similarity"""
    def __init__(self, s1, s2, collection):
        """Constructor for document cosine similarity"""
        super().__init__(s1, s2)
        self.collection = collection
        if collection.instanceOf(Index):
            self.v1 = collection.getTermVector(s1)
            self.v2 = collection.getTermVector(s2)
            self.calculateSimilarity()
        elif collection.instanceOf(Word2Vec):
            self.similarity = collection.wv.similarity(s1, s2)

    def calculateSimilarity(self):
        """calculates the cosine similarity"""
        array = np.array([self.v1, self.v2])
        array_sparse = sparse.csr_matrix(array)
        self.similarity = cosine_similarity(array_sparse)[0][1]

    def getSimilarity(self):
        """returns the similarity"""
        return self.similarity

class PMI(Similarity):
    """Pointwise Mutual Information"""
    def __init__(self, s1, s2, index, radius = None):
        """Constructor for PMI"""
        super().__init__(s1, s2)
        self.index = index
        self.similarity = 0
        if radius == '':
            self.calculateSimilarity()
        else:
            self.radius = int(radius)
            self.calculateSimilarityRange()


    def calculateSimilarity(self):
        """calculates similarity with the radius being the entire document"""
        d1 = self.index.getDocumentFrequency(self.s1)
        d2 = self.index.getDocumentFrequency(self.s2)
        d12 = self.index.getMutualDocuments(d1, d2)
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
        """calculates similarity with a specified range"""
        f1 = self.index.getTermFrequency(self.s1)
        f2 = self.index.getTermFrequency(self.s2)
        D = self.index.getSumFrequency()
        f12 = self.index.getMutualFrequency(self.s1, self.s2)
        try:
            self.similarity = max(0, math.log((f12 * D )/ (f1 * f2), 2))
        except:
            print("error: one of the words does not exist in index")


    def getSimilarity(self):
        return self.similarity


