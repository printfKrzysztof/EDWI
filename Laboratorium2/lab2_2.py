import math
import os
import re
import matplotlib.pyplot as plt

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
documents_folder = "./Laboratorium2/zad2"
documents = []
for filename in os.listdir(documents_folder):
    with open(os.path.join(documents_folder, filename), 'r', encoding='utf-8') as file:
        document = file.read()
        document = re.sub(r'[^a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ\s]', '', document) 
        documents.append(document)


# Selecting a document
selected_document_index = 0
selected_documents = []
# print(documents)
for document in documents:
    selected_documents.append(preprocess_document(document))


all_words = set()
for document in selected_documents:
    all_words.update(document)
# print(all_words)
# Calculate TF-IDF for each word in the selected document
tfidf_scores = {}
for word in all_words:
    tfidf_scores[word] = [tfidf(word, selected_documents[0], selected_documents)]
for selected_document_index in range(1, len(selected_documents)):
    for word in all_words:
        tfidf_scores[word].append(tfidf(word, selected_documents[selected_document_index], selected_documents))
# Print TF-IDF scores for the selected document

# print(tfidf_scores)

    


# Calculate word frequencies
word_frequencies = {}
for word, tfidf_scores_list in tfidf_scores.items():
    word_frequencies[word] = sum(tfidf_scores_list)  # Sum of TF-IDF scores across all documents

# Sort word frequencies in descending order
sorted_word_frequencies = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)

# Plot word frequencies
plt.figure(figsize=(10, 6))
top_words = 20  # You can adjust the number of words to display
words, frequencies = zip(*sorted_word_frequencies[:top_words])
plt.bar(words, frequencies)
plt.xticks(rotation=45, ha='right')
plt.xlabel('Words')
plt.ylabel('Frequency')
plt.title('Word Frequencies')
plt.tight_layout()
plt.show()

# Plot the most popular word
most_popular_word, most_popular_frequency = sorted_word_frequencies[0]
plt.figure(figsize=(6, 4))
plt.bar(most_popular_word, most_popular_frequency)
plt.xlabel('Word')
plt.ylabel('Frequency')
plt.title('Most Popular Word')
plt.tight_layout()
plt.show()