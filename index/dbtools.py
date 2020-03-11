"""
Tools for the local DB for the indexes
"""
import sqlite3
from typing import Set, Dict


def init():
    """
    Init the local DB
    """
    with sqlite3.connect('static/index/index.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS ind
                (word text, docid text);
               """)
        cursor.execute("""CREATE INDEX IF NOT EXISTS word_index 
                ON ind(word);""")


def put(ind: Dict[str, Set[str]]):
    """
    Flushes the index records to the DB
    :param ind: the aux index
    """
    with sqlite3.connect('static/index/index.db') as connection:
        cursor = connection.cursor()
        for (word, docs) in ind.items():
            for doc in docs:
                cursor.execute("""INSERT INTO ind (word, docid)
                      VALUES (?, ?);""", (word, doc))


def retrieve(word: str) -> Set[str]:
    """
    Retrieve the index of a word
    :param word: word to retrieve
    :return: the index
    """
    with sqlite3.connect('static/index/index.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""SELECT docid 
                            FROM ind
                            where word = ?;""", (word,))
        return {i[0] for i in cursor.fetchall()}


def clear_index(docid: str):
    """
    Remove the index of a doc from the DB
    :param docid: doc to clear
    """
    with sqlite3.connect('static/index/index.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""DELETE FROM ind 
                            WHERE docid = ?;""", (docid,))


init()
