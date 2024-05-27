import requests
from bs4 import BeautifulSoup
import re


# URLs of the websites
urls = ["https://www.otomoto.pl/osobowe/oferta/renault-megane-renault-megane-iii-ID6GoKCi.html", 
        "https://www.otomoto.pl/osobowe/oferta/renault-megane-renault-megane-rs-ID6FC1Nu.html",
        "https://www.otomoto.pl/osobowe/oferta/renault-megane-renault-megane-1-5-dci-110-km-stan-bardzo-dobry-ID6GrM6q.html"]

def get_text_files(url):

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the div with the specified class
    div_content = soup.find("div", class_="ooa-unlmzs e9na3zb2")

    # Extract the text content from the div
    if div_content:
        text_content = div_content.get_text(separator=' ')
        # Replace HTML tags with spaces
        text_content = ' '.join(text_content.split())
        text_content = re.sub(r'[^a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ\s]', '', text_content)
        return text_content
    else:
        print("Div not found or website structure changed.")


def licz_indeks_odwr():
    descriptors = []
    #   Getting docs 
    for url in urls:
        descriptors.append(get_text_files(url))
    tokens = []
    for desc in descriptors:
        tokens.append(desc.lower().split())

    # Flatten the list of lists into a single list
    flattened_tokens = [token for sublist in tokens for token in sublist]

    # Create a set to get unique terms
    unique_terms = set(flattened_tokens)

    # Convert the set back to a list
    terms = list(unique_terms)

    term_occurrences = {term: [] for term in terms}

    # Populate the dictionary with document occurrences
    for term in terms:
        # Iterate over tokens of each document
        for i, token_list in enumerate(tokens):
            # Check if term exists in tokens of current document
            if term in token_list:
                # If term exists, append document number and count repetitions
                term_occurrences[term].append((i+1, token_list.count(term)))

    # Print results
    for term, occurrences in term_occurrences.items():
        # Prepare the string for document occurrences
        doc_occurrences_str = ', '.join([f"Dokument {doc} ({urls[doc-1]}) --- {count}" for doc, count in occurrences])
        print(f"{term}: {doc_occurrences_str}")

def Add_Next(adres_strony_otomoto):
    urls.append(adres_strony_otomoto)
    licz_indeks_odwr()

licz_indeks_odwr()
Add_Next("https://www.otomoto.pl/osobowe/oferta/renault-megane-megane-1-4-tce-dynamique-130-km-navi-klima-serwis-bezwypadek-2012-ID6GicVS.html")