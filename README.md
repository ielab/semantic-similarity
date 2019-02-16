# semantic-similarity
This project calculates the semantic similarity using several methods between a pair of words.
Elasticsearch indexes are supported with cosine similarity and +PMI and word2vec with cosine similarity.
It also evaluates the correlation between two sets of similarity measures.

## usage
The program can be used either as a library or run from the terminal.

### library
Instantiate the collection to be used, either from an elasticsearch index or word2vec binary file.
Instantiate the similarity class to be used. Pass this into the similarity method of the collection as well as the two strings to compare.
There is also a fromFile method that can be used to calculate the similarity for each pair of values in a file and writes the result to similarity.txt.

### terminal
Run main.py. It will prompt for various information, such as the collection and similarity class to use.
Follow the prompts and type in the information it requires.
The results will be written to a file the program creates, similarity.txt

### evaluation
evaluation.py calculates a pearson or spearman correlation between two sets of similarities.
The two files need to contain the same word pairs in the same order and have one similarity value on each line.

### requirements
- An elasticsearch index or word2vec binary file are needed.
- The following python modules are needed:
  scipy
  elasticsearch
  sklearn
  numpy
  gensim
 
## testing
Run TestMethods.py.
