import codecs
import re
import string

import requests

from zemberek import zemberek

zemberek = zemberek()

def tokenize_stem(doc):

    cleaned_doc = remove_punctuation(doc)
    tokens = cleaned_doc.split()
    stemmed_tokens = []
    tr_stopwords = turkish_stopwords()

    for token in tokens:
        stem_token = stemmer(token)
        if (stem_token not in tr_stopwords) and (len(stem_token) > 1):
            stemmed_tokens.append(stem_token)

    return stemmed_tokens


def token_stem_merge(doc):
    tokenized_doc = tokenize_stem(doc)
    merged_token = ""

    for token in tokenized_doc:
         merged_token += token + " "

    return merged_token.strip()


def stemmer(word):
    """
    stemmer = TurkishStemmer()
    stem = stemmer.stem(word)
    if stem not in turkish_stopwords():
        return stem
    return ""
    """
    if zemberek.kelime_tip(word) == "ISIM":
        return zemberek.kelime_kok(word)
    else:
        return ""


    #return zemberek.kelime_kok(word)


def remove_punctuation(doc):
    delete_chars = string.digits + string.punctuation
    doc = remove_html_tags(doc).lower()
    doc = str(doc).translate(str.maketrans('', '', delete_chars))\
            .replace("\r", " ").replace("\n", " ").replace("“", " ").replace("’", " ")\
            .replace("", " ").replace("", " ").replace("", " ").replace("", " ").replace("‘", " ")\
            .replace("…", " ").replace("'", " ")

    doc = " ".join(doc.split())
    return doc


def remove_html_tags(doc):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', doc)
    return cleantext


def turkish_stopwords():
    doc_path = "resources/turkish_stopwords"

    with codecs.open(doc_path, 'r', encoding='utf8') as file:
        file_content = file.read()  # dosya oku
    stop_words = file_content.split()

    return set(set(stop_words))