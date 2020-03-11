from queue import Queue
from threading import Thread

from flask import Flask, request

from index import dbtools
from index.indexer import aux_index, aux_lock, indexer, index_flusher, flush_index
from index.crawler import crawl

app = Flask(__name__)
queue = Queue(maxsize=100)
crawling_flag = True


@app.route('/')
def root():
    """
    Serves the index
    :return: the index records by the word
    """
    word = request.args.get('word')

    # retrieve the index from the local index
    aux_lock.acquire()
    aux_res = aux_index.get('word')
    aux_lock.release()

    if aux_res is None:
        aux_res = set()

    # retrieve the index from the db and combine with the local index entry
    return '\n'.join(dbtools.retrieve(word) | aux_res)


if __name__ == '__main__':
    # Start the workers
    Thread(target=crawl, args=(queue,), daemon=True).start()
    Thread(target=indexer, args=(queue,), daemon=True).start()
    Thread(target=index_flusher, daemon=True).start()
    # And start the server
    app.run('127.0.0.1', 9000)

    # Flush the local index at the exit
    flush_index()
