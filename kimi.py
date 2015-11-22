# coding: utf-8

import sys
from flask import Flask, render_template
from flask.ext.flatpages import FlatPages
from flask.ext.frozen import Freezer


DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'


app = Flask(__name__)
app.config.from_object(__name__)
# the collection of my blog posts
pages = FlatPages(app)
freezer = Freezer(app)


@app.route('/index')
def index():
	# this is index.html, I will write it
    return render_template('index_b.html', pages=pages)


@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    return render_template('page.html', page=page)


@app.route('/tag/<string:tag>/')
def tag(tag):
	# for p in pages:
	#	if tag in p.meta.get('tags', [])
	#		tagged.append(tag)
    tagged = [p for p in pages if tag in p.meta.get('tags', [])]
    return render_template('tag.html', pages=tagged, tag=tag)


@app.route('/about')
def about():
	return render_template("about.html")


if __name__ == "__main__":
    if len(sys.argv) > 1  and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run()
