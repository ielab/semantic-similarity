import unittest
from similarity import Term, Document, Similarity, DocCos, Index, PMI
import math

class TestTerm(unittest.TestCase):

    def testTfidf(self):
        term = Term("example", 2, 35)
        self.assertAlmostEqual(term.calculateTfidf(70000), 6.60205999)

    def testUpdate(self):
        term = Term("example", 2, 35)
        term.update(1, 5)
        self.assertEqual(term.termFreq, 3)
        self.assertEqual(term.docFreq, 40)


class TestDocuments(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.vec = {'_index': 'med', '_type': '_doc', '_id': '25', '_version': 1, 'found': True, 'took': 1,
                    'term_vectors': {
                        'title': {'field_statistics': {'sum_doc_freq': 66088, 'doc_count': 5934, 'sum_ttf': 70822},
                                  'terms': {'compounds': {'doc_freq': 31, 'ttf': 31, 'term_freq': 1},
                                            'neuroleptic': {'doc_freq': 17, 'ttf': 18, 'term_freq': 1},
                                            'agents': {'doc_freq': 122, 'ttf': 122, 'term_freq': 1},
                                            'of': {'doc_freq': 4358, 'ttf': 6273, 'term_freq': 1},
                                            'pharmacological': {'doc_freq': 20, 'ttf': 20, 'term_freq': 1},
                                            'blood': {'doc_freq': 236, 'ttf': 237, 'term_freq': 1}}},
                        'mesh_headings': {
                            'field_statistics': {'sum_doc_freq': 99053, 'doc_count': 5934, 'sum_ttf': 105020},
                            'terms': {
                                'activity': {'doc_freq': 208, 'ttf': 208, 'term_freq': 1},
                                'agents': {'doc_freq': 693, 'ttf': 803, 'term_freq': 1},
                                'aggression': {'doc_freq': 13, 'ttf': 13, 'term_freq': 1},
                                'amphetamine': {'doc_freq': 6, 'ttf': 6, 'term_freq': 1},
                                'animal': {'doc_freq': 119, 'ttf': 129, 'term_freq': 1},
                                'animals': {'doc_freq': 2477, 'ttf': 2517, 'term_freq': 1},
                                'antagonists': {'doc_freq': 479, 'ttf': 529, 'term_freq': 1},
                                'apomorphine': {'doc_freq': 25, 'ttf': 25, 'term_freq': 1},
                                'avoidance': {'doc_freq': 13, 'ttf': 13, 'term_freq': 1},
                                'behavior': {'doc_freq': 150, 'ttf': 180, 'term_freq': 1},
                                'blood': {'doc_freq': 462, 'ttf': 592, 'term_freq': 1},
                                'chlordiazepoxide': {'doc_freq': 2, 'ttf': 2, 'term_freq': 1},
                                'chlorpromazine': {'doc_freq': 29, 'ttf': 29, 'term_freq': 1},
                                'contraction': {'doc_freq': 139, 'ttf': 147, 'term_freq': 1}}}}}
        doc = Document(self.vec, ['title', 'mesh_headings'], 25)
        doc = Document(self.vec, ['title', 'mesh_headings'], 25)
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
                    'chlorpromazine',
                    'contraction']
        self.assertEqual(termList, termComp)

    def testTerms(self):
        term = self.terms['compounds']
        self.assertEqual(term, Term('compounds', 1, 31))
        term = self.terms['blood']
        self.assertEqual(term, Term('blood', 1 + 1, 236 + 462))


class TestIndex(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.index = Index('ielab:KVVjnWygjGJRQnYmgAd3CsWV@ielab-pubmed-index.uqcloud.net:80',
                           ['title', 'mesh_headings'])

    def testIds(self):
        self.assertEqual(self.index.getIds(), ['14',
                                               '19',
                                               '22',
                                               '24',
                                               '25',
                                               '26',
                                               '29',
                                               '40',
                                               '41',
                                               '44'])

    def testFields(self):
        self.assertEqual(self.index.getFields(), ['abstract',
  'title',
  'authors',
  'mesh_headings',
  'pubdate',
  'publication_types'])

    def testTermVectors(self):
        self.vec = {'_index': 'med', '_type': '_doc', '_id': '25', '_version': 1, 'found': True, 'took': 1,
                    'term_vectors': {
                        'title': {'field_statistics': {'sum_doc_freq': 66088, 'doc_count': 5934, 'sum_ttf': 70822},
                                  'terms': {'compounds': {'doc_freq': 31, 'ttf': 31, 'term_freq': 1},
                                            'neuroleptic': {'doc_freq': 17, 'ttf': 18, 'term_freq': 1},
                                            'blood': {'doc_freq': 236, 'ttf': 237, 'term_freq': 1}}},
                        'mesh_headings': {
                            'field_statistics': {'sum_doc_freq': 99053, 'doc_count': 5934, 'sum_ttf': 105020},
                            'terms': {
                                'blood': {'doc_freq': 462, 'ttf': 592, 'term_freq': 1},
                                'chlordiazepoxide': {'doc_freq': 2, 'ttf': 2, 'term_freq': 1},
                                'chlorpromazine': {'doc_freq': 29, 'ttf': 29, 'term_freq': 1},
                                'contraction': {'doc_freq': 139, 'ttf': 147, 'term_freq': 1}}}}}
        self.vec2 = {'_index': 'med', '_type': '_doc', '_id': '25', '_version': 1, 'found': True, 'took': 1,
                    'term_vectors': {
                        'title': {'field_statistics': {'sum_doc_freq': 66088, 'doc_count': 5934, 'sum_ttf': 70822},
                                  'terms': {'compounds': {'doc_freq': 31, 'ttf': 31, 'term_freq': 1},
                                            'neuroleptic': {'doc_freq': 17, 'ttf': 18, 'term_freq': 1},
                                            'agents': {'doc_freq': 122, 'ttf': 122, 'term_freq': 1},
                                            'of': {'doc_freq': 4358, 'ttf': 6273, 'term_freq': 1},
                                            'pharmacological': {'doc_freq': 20, 'ttf': 20, 'term_freq': 1}}}}}
        self.vec3 = {'_index': 'med', '_type': '_doc', '_id': '25', '_version': 1, 'found': True, 'took': 1,
                    'term_vectors': {
                        'title': {'field_statistics': {'sum_doc_freq': 66088, 'doc_count': 5934, 'sum_ttf': 70822},
                                  'terms': {'compounds': {'doc_freq': 31, 'ttf': 31, 'term_freq': 1},
                                            'neuroleptic': {'doc_freq': 17, 'ttf': 18, 'term_freq': 1},
                                            'agents': {'doc_freq': 122, 'ttf': 122, 'term_freq': 1},
                                            'of': {'doc_freq': 4358, 'ttf': 6273, 'term_freq': 1},
                                            'pharmacological': {'doc_freq': 20, 'ttf': 20, 'term_freq': 1},
                                            'blood': {'doc_freq': 124, 'ttf': 145, 'term_freq': 1}}},
                        'mesh_headings': {
                            'field_statistics': {'sum_doc_freq': 99053, 'doc_count': 5934, 'sum_ttf': 105020},
                            'terms': {
                                'chlordiazepoxide': {'doc_freq': 2, 'ttf': 2, 'term_freq': 1},
                                'chlorpromazine': {'doc_freq': 29, 'ttf': 29, 'term_freq': 1},
                                'contraction': {'doc_freq': 139, 'ttf': 147, 'term_freq': 1}}}}}
        docs = [Document(self.vec, ['title', 'mesh_headings'], 25), Document(self.vec2, ['title'], 13), Document(self.vec3, ['title', 'mesh_headings'], 11)]
        self.index.docs = docs
        self.assertAlmostEqual(self.index.getTermVector('blood')[0], 4.747998974970)
        self.assertEqual(self.index.getTermVector('blood')[1], 0)
        self.assertAlmostEqual(self.index.getTermVector('blood')[2], 3.12443322494)

class TestDocCos(unittest.TestCase):
    def testSimilarity(self):
        index = Index('ielab:KVVjnWygjGJRQnYmgAd3CsWV@ielab-pubmed-index.uqcloud.net:80',
                           ['title'])
        sim = DocCos("frog", "cat", index)
        sim.v1 = [3.4, 0, 2.8]
        sim.v2 = [1.9, 0.1, 3.5]
        sim.calculateSimilarity()
        self.assertAlmostEqual(sim.getSimilarity(), 0.9266830361753)

class TestPMI(unittest.TestCase):
    def testSimilarity(self):
        index = Index('ielab:KVVjnWygjGJRQnYmgAd3CsWV@ielab-pubmed-index.uqcloud.net:80',
                           ['title', 'mesh_headings'])
        self.vec = {'_index': 'med', '_type': '_doc', '_id': '25', '_version': 1, 'found': True, 'took': 1,
                    'term_vectors': {
                        'title': {'field_statistics': {'sum_doc_freq': 66088, 'doc_count': 5934, 'sum_ttf': 70822},
                                  'terms': {'compounds': {'doc_freq': 31, 'ttf': 31, 'term_freq': 1},
                                            'neuroleptic': {'doc_freq': 17, 'ttf': 18, 'term_freq': 1},
                                            'blood': {'doc_freq': 236, 'ttf': 237, 'term_freq': 1}}},
                        'mesh_headings': {
                            'field_statistics': {'sum_doc_freq': 99053, 'doc_count': 5934, 'sum_ttf': 105020},
                            'terms': {
                                'blood': {'doc_freq': 462, 'ttf': 592, 'term_freq': 1},
                                'chlordiazepoxide': {'doc_freq': 2, 'ttf': 2, 'term_freq': 1},
                                'chlorpromazine': {'doc_freq': 29, 'ttf': 29, 'term_freq': 1},
                                'contraction': {'doc_freq': 139, 'ttf': 147, 'term_freq': 1}}}}}
        self.vec2 = {'_index': 'med', '_type': '_doc', '_id': '25', '_version': 1, 'found': True, 'took': 1,
                     'term_vectors': {
                         'title': {'field_statistics': {'sum_doc_freq': 66088, 'doc_count': 5934, 'sum_ttf': 70822},
                                   'terms': {'compounds': {'doc_freq': 31, 'ttf': 31, 'term_freq': 1},
                                             'neuroleptic': {'doc_freq': 17, 'ttf': 18, 'term_freq': 1},
                                             'agents': {'doc_freq': 122, 'ttf': 122, 'term_freq': 1},
                                             'of': {'doc_freq': 4358, 'ttf': 6273, 'term_freq': 1},
                                             'pharmacological': {'doc_freq': 20, 'ttf': 20, 'term_freq': 1},
                                             'blood': {'doc_freq': 462, 'ttf': 592, 'term_freq': 1},}}}}
        self.vec3 = {'_index': 'med', '_type': '_doc', '_id': '25', '_version': 1, 'found': True, 'took': 1,
                     'term_vectors': {
                         'title': {'field_statistics': {'sum_doc_freq': 66088, 'doc_count': 5934, 'sum_ttf': 70822},
                                   'terms': {'compounds': {'doc_freq': 31, 'ttf': 31, 'term_freq': 1},
                                             'chlordiazepoxide': {'doc_freq': 2, 'ttf': 2, 'term_freq': 1},
                                             'chlorpromazine': {'doc_freq': 29, 'ttf': 29, 'term_freq': 1},
                                             'neuroleptic': {'doc_freq': 17, 'ttf': 18, 'term_freq': 1},
                                             'agents': {'doc_freq': 122, 'ttf': 122, 'term_freq': 1},
                                             'of': {'doc_freq': 4358, 'ttf': 6273, 'term_freq': 1},
                                             'pharmacological': {'doc_freq': 20, 'ttf': 20, 'term_freq': 1},
                                             'blood': {'doc_freq': 124, 'ttf': 145, 'term_freq': 1}}},
                         'mesh_headings': {
                             'field_statistics': {'sum_doc_freq': 99053, 'doc_count': 5934, 'sum_ttf': 105020},
                             'terms': {
                                 'chlordiazepoxide': {'doc_freq': 2, 'ttf': 2, 'term_freq': 1},
                                 'chlorpromazine': {'doc_freq': 29, 'ttf': 29, 'term_freq': 1},
                                 'contraction': {'doc_freq': 139, 'ttf': 147, 'term_freq': 1}}}}}
        self.vec4 = {'_index': 'med', '_type': '_doc', '_id': '25', '_version': 1, 'found': True, 'took': 1,
                     'term_vectors': {
                         'title': {'field_statistics': {'sum_doc_freq': 66088, 'doc_count': 5934, 'sum_ttf': 70822},
                                   'terms': {'compounds': {'doc_freq': 31, 'ttf': 31, 'term_freq': 1},
                                             }},
                         'mesh_headings': {
                             'field_statistics': {'sum_doc_freq': 99053, 'doc_count': 5934, 'sum_ttf': 105020},
                             'terms': {
                                 'contraction': {'doc_freq': 139, 'ttf': 147, 'term_freq': 1}}}}}
        self.vec5 = {'_index': 'med', '_type': '_doc', '_id': '25', '_version': 1, 'found': True, 'took': 1,
                     'term_vectors': {
                         'title': {'field_statistics': {'sum_doc_freq': 66088, 'doc_count': 5934, 'sum_ttf': 70822},
                                   'terms': {'compounds': {'doc_freq': 31, 'ttf': 31, 'term_freq': 1},
                                             }},
                         'mesh_headings': {
                             'field_statistics': {'sum_doc_freq': 99053, 'doc_count': 5934, 'sum_ttf': 105020},
                             'terms': {
                                 'contraction': {'doc_freq': 139, 'ttf': 147, 'term_freq': 1}}}}}
        docs = [Document(self.vec, ['title', 'mesh_headings'], 25), Document(self.vec2, ['title'], 12),
                Document(self.vec3, ['title', 'mesh_headings'], 11), Document(self.vec4, ['title', 'mesh_headings'], 14), Document(self.vec5, ['title', 'mesh_headings'], 31)]
        index.docs = docs
        sim = PMI('blood', 'contraction', index)
        self.assertAlmostEqual(sim.getSimilarity(), 0)
        sim = PMI('chlordiazepoxide', 'chlorpromazine', index)
        self.assertAlmostEqual(sim.getSimilarity(), 1.3219280948873)
if __name__ == '__main__':
    unittest.main()
