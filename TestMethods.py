import unittest
from models import *
from similarity import *
import math


class TestTerm(unittest.TestCase):

    def testTfidf(self):
        term = Term("example", 2, 35, "title")
        self.assertAlmostEqual(term.calculateTfidf(70000, 400), 4.48607609737)

    def testUpdate(self):
        term = Term("example", 1, [{'position': 6}], "title")
        term.update(2, [{'position': 6}, {'position': 10}], "abstract")
        self.assertEqual(term.termFreq, 3)
        self.assertEqual(term.positions.get("abstract"), [{'position': 6}, {'position': 10}])


class TestDocuments(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.vec = {'_index': 'med', '_type': '_doc', '_id': '25', '_version': 1, 'found': True, 'took': 1,
                    'term_vectors': {
                        'title': {'field_statistics': {'sum_doc_freq': 66088, 'doc_count': 5934, 'sum_ttf': 70822},
                                  'terms': {'compounds': {'term_freq': 2, 'tokens': [{'position': 1}, {'position': 7}]},
                                            'neuroleptic': {'term_freq': 1, 'tokens': [{'position': 2}]},
                                            'agents': {'term_freq': 1, 'tokens': [{'position': 3}]},
                                            'of': {'term_freq': 1, 'tokens': [{'position': 4}]},
                                            'pharmacological': {'term_freq': 1, 'tokens': [{'position': 5}]},
                                            'blood': {'term_freq': 1, 'tokens': [{'position': 6}]}}},
                        'mesh_headings': {
                            'field_statistics': {'sum_doc_freq': 99053, 'doc_count': 5934, 'sum_ttf': 105020},
                            'terms': {
                                'activity': {'term_freq': 1, 'tokens': [{'position': 1}]},
                                'agents': {'term_freq': 1, 'tokens': [{'position': 2}]},
                                'aggression': {'term_freq': 1, 'tokens': [{'position': 3}]},
                                'amphetamine': {'term_freq': 1, 'tokens': [{'position': 4}]},
                                'animal': {'term_freq': 1, 'tokens': [{'position': 5}]},
                                'animals': {'term_freq': 1, 'tokens': [{'position': 6}]},
                                'antagonists': {'term_freq': 1, 'tokens': [{'position': 7}]},
                                'apomorphine': {'term_freq': 1, 'tokens': [{'position': 8}]},
                                'avoidance': {'term_freq': 1, 'tokens': [{'position': 9}]},
                                'behavior': {'term_freq': 1, 'tokens': [{'position': 10}]},
                                'blood': {'term_freq': 1, 'tokens': [{'position': 11}]},
                                'chlordiazepoxide': {'term_freq': 1, 'tokens': [{'position': 12}]},
                                'chlorpromazine': {'term_freq': 1, 'tokens': [{'position': 13}]}}}}}
        doc = Document(self.vec)
        self.terms = doc.getTerms()

    def testGenerateTerms(self):
        termList = []
        for term in self.terms:
            termList.append(term)
        termComp = ['compounds',
                    'neuroleptic',
                    'agents',
                    'of',
                    'pharmacological',
                    'blood',
                    'activity',
                    'aggression',
                    'amphetamine',
                    'animal',
                    'animals',
                    'antagonists',
                    'apomorphine',
                    'avoidance',
                    'behavior',
                    'chlordiazepoxide',
                    'chlorpromazine']
        self.assertEqual(termList, termComp)

    def testTerms(self):
        term = self.terms['compounds']
        self.assertEqual(term, Term('compounds', 2, [{'position': 1}, {'position': 7}], "title"))
        term = self.terms['blood']
        temp = Term('blood', 1, [{'position': 6}], 'title')
        temp.update(1, [{'position': 11}], 'mesh_headings')
        self.assertEqual(term, temp)
        term = self.terms['blood']


class TestIndex(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.index = Index()
        self.vec = {'_index': 'med', '_type': '_doc', '_id': '1', '_version': 1, 'found': True, 'took': 1,
                    'term_vectors': {
                        'title': {'field_statistics': {'sum_doc_freq': 3, 'doc_count': 3, 'sum_ttf': 3},
                                  'terms': {'compounds': {'term_freq': 1, 'tokens': [{'position': 7}]},
                                            'neuroleptic': {'term_freq': 1, 'tokens': [{'position': 2}]},
                                            'blood': {'term_freq': 1, 'tokens': [{'position': 4}]}}},
                        'mesh_headings': {
                            'field_statistics': {'sum_doc_freq': 2, 'doc_count': 3, 'sum_ttf': 7},
                            'terms': {
                                'animals': {'term_freq': 1, 'tokens': [{'position': 6}]},
                                'antagonists': {'term_freq': 1, 'tokens': [{'position': 7}]},
                                'apomorphine': {'term_freq': 1, 'tokens': [{'position': 8}]},
                                'avoidance': {'term_freq': 1, 'tokens': [{'position': 9}]},
                                'behavior': {'term_freq': 1, 'tokens': [{'position': 10}]},
                                'blood': {'term_freq': 1, 'tokens': [{'position': 11}]},
                                'chlordiazepoxide': {'term_freq': 1, 'tokens': [{'position': 12}]}}}}}
        self.vec2 = {'_index': 'med', '_type': '_doc', '_id': '2', '_version': 1, 'found': True, 'took': 1,
                     'term_vectors': {
                         'title': {'field_statistics': {'sum_doc_freq': 3, 'doc_count': 3, 'sum_ttf': 6},
                                   'terms': {'activity': {'term_freq': 1, 'tokens': [{'position': 1}]},
                                             'agents': {'term_freq': 1, 'tokens': [{'position': 2}]},
                                             'aggression': {'term_freq': 1, 'tokens': [{'position': 3}]},
                                             'amphetamine': {'term_freq': 1, 'tokens': [{'position': 4}]},
                                             'animal': {'term_freq': 1, 'tokens': [{'position': 5}]},
                                             'animals': {'term_freq': 1, 'tokens': [{'position': 6}]}}}}}
        self.vec3 = {'_index': 'med', '_type': '_doc', '_id': '3', '_version': 1, 'found': True, 'took': 1,
                     'term_vectors': {
                         'title': {'field_statistics': {'sum_doc_freq': 3, 'doc_count': 3, 'sum_ttf': 7},
                                   'terms': {
                                       'compounds': {'term_freq': 2, 'tokens': [{'position': 1}, {'position': 7}]},
                                       'neuroleptic': {'term_freq': 1, 'tokens': [{'position': 2}]},
                                       'agents': {'term_freq': 1, 'tokens': [{'position': 3}]},
                                       'of': {'term_freq': 1, 'tokens': [{'position': 4}]},
                                       'pharmacological': {'term_freq': 1, 'tokens': [{'position': 5}]},
                                       'blood': {'term_freq': 1, 'tokens': [{'position': 6}]}}},
                         'mesh_headings': {'field_statistics': {'sum_doc_freq': 2, 'doc_count': 3, 'sum_ttf': 13},
                                           'terms': {
                                               'activity': {'term_freq': 1, 'tokens': [{'position': 1}]},
                                               'agents': {'term_freq': 1, 'tokens': [{'position': 2}]},
                                               'aggression': {'term_freq': 1, 'tokens': [{'position': 3}]},
                                               'amphetamine': {'term_freq': 1, 'tokens': [{'position': 4}]},
                                               'animal': {'term_freq': 1, 'tokens': [{'position': 5}]},
                                               'animals': {'term_freq': 1, 'tokens': [{'position': 6}]},
                                               'antagonists': {'term_freq': 1, 'tokens': [{'position': 7}]},
                                               'apomorphine': {'term_freq': 1, 'tokens': [{'position': 8}]},
                                               'avoidance': {'term_freq': 1, 'tokens': [{'position': 9}]},
                                               'behavior': {'term_freq': 1, 'tokens': [{'position': 10}]},
                                               'blood': {'term_freq': 1, 'tokens': [{'position': 11}]},
                                               'chlordiazepoxide': {'term_freq': 1, 'tokens': [{'position': 12}]},
                                               'chlorpromazine': {'term_freq': 1, 'tokens': [{'position': 13}]}}}}}
        docs = [Document(self.vec), Document(self.vec2), Document(self.vec3)]
        self.index.docs = docs

    def testTermVectors(self):
        self.assertAlmostEqual(self.index.getTermVector('blood')[0], 0.352182518111)
        self.assertEqual(self.index.getTermVector('blood')[1], 0)
        self.assertAlmostEqual(self.index.getTermVector('blood')[2], 0.352182518111)

    def testSumFrequency(self):
        self.assertEqual(self.index.getSumFrequency(), 36)

    def testTermFrequency(self):
        self.assertEqual(self.index.getTermFrequency('compounds'), 3)

    def testMutualFrequency(self):
        self.assertEqual(self.index.getMutualFrequency('compounds', 'of', 5), 2)
        self.assertEqual(self.index.getMutualFrequency('animals', 'antagonists', 2), 2)

    def testDocuments(self):
        self.assertEqual(self.index.getDocuments('animal'), ['2', '3'])

    def testMutualDocuments(self):
        d1 = ['1', '3', '5', '7']
        d2 = ['1', '2', '3']
        self.assertEqual(set(self.index.getMutualDocuments(d1, d2)), set(['3', '1']))

    def testSimilarity(self):
        cos = CosineSimilarity()
        self.assertAlmostEqual(self.index.similarity(cos, 'animal', 'agents'), 0.94868329805)
        pmi = PMI()
        self.assertAlmostEqual(self.index.similarity(pmi, 'animal', 'agents'), 0.58496250072)
        pmiRadius = PMI(5)
        self.assertAlmostEqual(self.index.similarity(pmiRadius, 'animal', 'agents'), 3.58496250072)


class TestCosineSimlarity(unittest.TestCase):
    def testSimilarity(self):
        v1 = [3.4, 0, 2.8]
        v2 = [1.9, 0.1, 3.5]
        sim = CosineSimilarity()
        self.assertAlmostEqual(sim.calculateSimilarity(v1, v2), 0.9266830361753)


class TestPMI(unittest.TestCase):
    def testSimilarity(self):
        sim = PMI()
        self.assertAlmostEqual(sim.calculateSimilarity(300, 200, 150, 130), 0.378511623253)

    def testSimilarityNeg(self):
        sim = PMI()
        self.assertEqual(sim.calculateSimilarity(300, 200, 120, 2), 0)


if __name__ == '__main__':
    unittest.main()
