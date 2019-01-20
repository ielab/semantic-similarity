# semantic-similarity
This project calculates the semantic similarity using several methods between a pair of words from an ElasticSearch index. 
Currently there is only Document Cosine Similarity. Other measures such as +PMI and NLP will be added.

## usage
Download the similarity.py file and run the program. It will prompt the user for the link to the index, the words to compare,
and the comparison method. 
Some modules may need to be installed before running.

### requirements
- An elasticsearch index with the documents to be used must first be created
- The following python modules are needed:
  scipy
  elasticsearch
  sklearn
  numpy
 
## testing
To be added
