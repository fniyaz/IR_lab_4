from queue import Queue
from threading import Lock
from time import sleep

from common.data import Story
from common.engine import preprocess
from index import dbtools


aux_index = {}

# Lock for safe index modification from different threads
aux_lock = Lock()


def indexer(queue: 'Queue[Story]'):
    """
    Index all the incoming data from the queue
    :param queue: the communication queue
    """
    while True:
        data = queue.get()
        update_index(data)


def update_index(story: Story):
    """
    Updates the local index with new Story
    :param story: the new story
    """
    # preprocess the tokens
    tokens = preprocess(story.body)

    for token in tokens:
        aux_lock.acquire()

        if token in aux_index:
            aux_index[token].add(story.id_)
        else:
            aux_index[token] = {story.id_}

        aux_lock.release()


def flush_index():
    """
    Flushes the local index to the DB
    """
    aux_lock.acquire()

    dbtools.put(aux_index)
    aux_index.clear()

    aux_lock.release()


def index_flusher():
    """
    Periodically flushes the data to the DB
    """
    while True:
        flush_index()
        sleep(10)
