from pathlib import Path

from flask import Flask, render_template, request

from common import engine
from common.data import Story

app = Flask(__name__)


@app.route('/')
def root():
    return render_template("index.html")


@app.route('/index.html')
def index():
    return root()


@app.route('/search.html')
def search():
    relevant = engine.search(request.args.get('query'))

    if len(relevant) == 0:
        return render_template('search_empty.html')
    return render_template('search.html', sz=len(relevant), data=[(story.id_, story.title) for story in relevant])


@app.route('/document')
def document():
    id_ = request.args.get("id")
    doc = Story.parse(Path(f'static/documents/{id_}.json'))
    return render_template('doc.html', title=doc.title, text_body=doc.body)


if __name__ == '__main__':
    app.run('0.0.0.0', 80)
