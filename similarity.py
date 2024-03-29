from abc import ABC, abstractmethod
import math
import numpy as np
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity

class Similarity(ABC):
    """Abstract class for calculating similarity"""
    pass

class VecSim(Similarity, ABC):
    """vector simlarities"""
    def calculateSimilarity(self, v1, v2):
        """implementation for the specific similarity method"""
        pass
class WordSim(Similarity, ABC):
    """word similarities"""
    def __init__(self, radius = None):
        self.radius = radius

    def calculateSimilarity(self, D, f1, f2, f12):
        pass

class CosineSimilarity(VecSim):
    """Document cosine similarity"""
    def __init__(self): #pass in vectors instead
        """Constructor for document cosine similarity"""
        pass

    def calculateSimilarity(self, v1, v2):
        """calculates the cosine similarity"""
        array = np.array([v1, v2])
        array_sparse = sparse.csr_matrix(array)
        return cosine_similarity(array_sparse)[0][1]

class PMI(WordSim):
    """Pointwise Mutual Information"""
    def __init__(self,  radius = None):
        """Constructor for PMI"""
        super().__init__(radius)


    def calculateSimilarity(self, D, f1, f2, f12):
        """
        calculates the +PMI similarity
        :param D: total number of documents/words
        :param f1: number of occurrences of first word
        :param f2: number of occurrences of second word
        :param f12: number of common occurrences of the two words
        :return: +PMI similarity
        """
        try:
            return max(0, math.log((f12 / D )/ ((f1/D) * (f2/D)), 2))
        except:
            print("error: one of the words does not exist in index")
        #self.similarity = math.log(f12 / (f1 * (f2 / D) + (math.sqrt(f1 * 0.23))))


