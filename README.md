# Semantic-Similarity
This project calculates the semantic similarity using several methods between a pair of words.
Elasticsearch indexes are supported with cosine similarity and +PMI and word2vec with cosine similarity.
It also evaluates the correlation between two sets of similarity measures.

## Usage
The program can be used either as a library or run from the terminal.

### Library
Instantiate the collection to be used, either from an elasticsearch index or word2vec binary file.

The Index takes an url to the elasticsearch index, the fields to be used, and the ids to be used. All fields and ids are used if field and id are left blank.
For example,
```
index1 = Index('ielab:KVVjnWygjGJRQnYmgAd3CsWV@ielab-pubmed-index.uqcloud.net:80')
index2 = Index('ielab:KVVjnWygjGJRQnYmgAd3CsWV@ielab-pubmed-index.uqcloud.net:80', ["title", "abstract"], ["1", "2", "134"])
```

The WordVector takes the filename of a binary file of a word2vec model. The file should be put in the same folder as the source code.
For example,
```
wv = WordVector("word2vec.bin")
```

To calculate the simiarity, a similarity object is also needed. Instantiate the similarity class to be used. 
For vector similarities (i.e. cosine similarity), no parameters are required.
```
sim = CosineSimilarity()
```

For Word Similarities (i.e. +PMI), an optional radius can be passed in. If no radius is specified, the radius is the entire document.
```
sim1 = PMI()
sim2 = PMI(10)
```

Pass this into the similarity method as well as the two strings to compare when calling the similarity method.
```
sim = CosineSimilarity()
index = Index('ielab:KVVjnWygjGJRQnYmgAd3CsWV@ielab-pubmed-index.uqcloud.net:80')
index.similarity(sim, "heart", "cardio")
```

There is also a fromFile method that can be used to calculate the similarity for each pair of values in a file and writes the result to similarity.txt.
This method takes the document containing pairs of words to be compared. It should be tab separated with each pair on a new line.
It also takes two column indexes, which are the index of the columns of words to be compared. Indexing starts at 0. A method and collection will also need to be passed in.
```
fromFile("wordpairs.txt", 0, 1, PMI(5), WordVector("vec.bin")
```

### Terminal
Run main.py. It will prompt for various information, such as the collection and similarity class to use.
Follow the prompts and type in the information it requires.
The results will be written to a file the program creates, similarity.txt

### Evaluation
evaluation.py calculates a pearson or spearman correlation between two sets of similarities.
The two files need to contain the same word pairs in the same order and have one similarity value on each line.
It takes two documents and the columns the similarity values are in (starting index is 0). If there is more than one column, it should be tab separated. Then by calling the calculatePearson or calculateSpearman methods, the correlation will be printed to terminal.
```
correlation = Correlation("sim1.txt", 0, "sim2.txt", 3)
correlation.calculatePearson()
correlation.calculateSpearman()
```
### requirements
- An elasticsearch index or word2vec binary file are needed.
- The following python modules are needed:
  scipy,
  elasticsearch,
  sklearn,
  numpy,
  gensim
 
## Testing
Run 
```
TestMethods.py.
```
