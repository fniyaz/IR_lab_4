import json
from pathlib import Path
from typing import NamedTuple, Generator

from bs4 import BeautifulSoup


class Story(NamedTuple):
    """
    A class to store the stories
    """
    id_: str
    title: str
    body: str

    def dump(self, file: Path):
        """
        Save the Story to the FS
        :param file: path where to save
        """
        with file.open('w') as writer:
            writer.write(json.dumps(self._asdict()))

    @staticmethod
    def parse(file: Path):
        """
        Restore a story from the FS
        :param file: path of the file to parse
        :return: the freshly parsed story
        """
        with file.open('r') as reader:
            dict_ = json.loads(reader.read())
            return Story(**dict_)


def parse_story(file: Path) -> Generator[Story, None, None]:
    """
    Parses all the stories from a sgm file and feeds them through a generators
    :param file: file to parse stories from
    :return: the generator for the files
    """

    with file.open('rb') as reader:
        soup = BeautifulSoup(reader.read(), features="html.parser")

        for raw in soup('reuters', recursive=False):

            id_ = raw['newid']

            text = raw.find('text')
            body = '\n'.join(text.findAll(text=True))

            if text.title is None:
                title = None
            else:
                title = text.title.string

            yield Story(id_, title, body)


def main():
    """
    Just for testing
    :return:
    """
    file = Path('static/collection/reut2-000.sgm')
    print(next(parse_story(file)))


if __name__ == '__main__':
    main()
