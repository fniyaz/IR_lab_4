"""
Basicly the engine from the previous labs
"""
import re
from pathlib import Path
from typing import Set

import nltk
import requests
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords

from common.data import Story

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')


def normalize(text, keep_asterisk=False):
    text = text.lower()
    if keep_asterisk:
        return re.sub(' +', ' ', re.sub('[^a-z *]', ' ', text))
    else:
        return re.sub(' +', ' ', re.sub('[^a-z ]', ' ', text))


def tokenize(text):
    return nltk.word_tokenize(text)


def lemmatization(tokens):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens]


def remove_stop_word(tokens):
    stop_words = stopwords.words('english')
    return [token for token in tokens if token not in stop_words]


def preprocess(text, lemm=True):
    if lemm:
        return remove_stop_word(lemmatization(tokenize(normalize(text))))
    return remove_stop_word(tokenize(normalize(text)))


def index(word: str) -> Set[str]:
    """
    Retrieves the index by the word
    :param word: the word
    :return: the index
    """
    return {i for i in requests.get(f'http://127.0.0.1:9000?word={word}').text.split('\n') if len(i) != 0}


def collection(id_: str) -> Story:
    """
    Retrieves the document by id from the FS
    :param id_: the doc id
    :return: the document loaded from the FS
    """
    return Story.parse(Path(f'static/documents/{id_}.json'))


def search(query: str) -> Set[Story]:
    q_tokens = preprocess(query)

    if len(q_tokens) == 0:
        return set()

    docs = {i for i in index(q_tokens[0])}  # copying the set
    if docs is None:
        docs = set()

    for i in [index(token) for token in q_tokens]:
        if i is not None:
            docs = docs & i

    return {collection(i) for i in docs}
