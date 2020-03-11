import os
from pathlib import Path
from queue import Queue
from random import randint
from time import sleep

from common.data import parse_story, Story

sleeping_periods = [i for i in range(10)]


def crawl(queue: 'Queue[Story]'):
    """
    Simulates a crawler, saves the crawled documents to the FS
    and feeds them to the queue to be indexed
    :param queue: queue for communication of the crawler and indexing
    """
    while True:
        rd = Path('static/collection')

        # Just iterate over all the files in the collections directory
        for file in os.listdir(rd):
            if file.endswith(".sgm"):
                # Parse them
                for story in parse_story(rd / file):

                    # Random delay between feeding them to queue
                    sleep(sleeping_periods[randint(0, len(sleeping_periods) - 1)])

                    # Process the Story
                    story.dump(Path(f'static/documents/{story.id_}.json'))
                    queue.put(story)
