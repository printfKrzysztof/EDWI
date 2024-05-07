import math


def tf(word, document):

    # Computes term frequency (TF) for a word in a document.
    # TF = (Number of times the word appears in the document) / (Total number of words in the document)
    
    word_count = document.count(word)
    total_words = len(document)
    return word_count / total_words

def idf(word, documents):
    
    # Computes inverse document frequency (IDF) for a word across all documents.
    # IDF = log((Total number of documents) / (Number of documents containing the word))
    
    num_documents_with_word = sum(1 for doc in documents if word in doc)
    return math.log10(len(documents) / (num_documents_with_word)) 
def tfidf(word, document, documents):
    
    #Computes TF-IDF for a word in a document.
    return tf(word, document) * idf(word, documents)

def preprocess_document(document):
   
   # Preprocesses a document by splitting it into words and converting them to lowercase.
    
    return document.lower().split()

# Example documents
documents = [
    "the man went out for a walk with his children",
    "the children sat around the fire"
]

# Selecting a document
selected_document_index = 0
selected_document = []
for document in documents:
    selected_document.append(preprocess_document(document))
print(selected_document)

all_words = list(set(selected_document[0]+ selected_document[1]))
print(all_words)
# Calculate TF-IDF for each word in the selected document
tfidf_scores = {}
for word in all_words:
    tfidf_scores[word] = [tfidf(word, selected_document[selected_document_index], selected_document)]

selected_document_index = 1
for word in all_words:
    tfidf_scores[word].append(tfidf(word, selected_document[selected_document_index], selected_document))
# Print TF-IDF scores for the selected document

for word, score in sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True):
    print(f"{word}: {score[0]}, {score[1]}")
