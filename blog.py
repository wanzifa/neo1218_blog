# coding: utf-8

"""
	neo1218_blog
	~~~~~~~~~~~~

		this is neo1218 ! ==>
		my personal blog
        yes, my personal blog wondelful
        just me and thinking
        blog is good
        make your heart
        follow your heart
        who you are and who I am!
        just neo1218 !
"""

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


@app.route('/index/')
def index():
	"""
	首页:
		1. 显示个人简介
		2. 显示最近发布的文章
		3. 显示文章类别标签(
			1. C&C++
			2. Python
			3. Vim
			4. Linux
			5. OSC
			6. Thoughts
		)
		4. 显示脚注(copyright, code)
	"""
	articals = (p for p in pages if 'date' in p.meta)
	latest = sorted(articals, reverse=True, key=lambda p: p.meta['date'])
	return render_template('index_b.html', pages=latest)


@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    return render_template('page.html', page=page)


if __name__ == "__main__":
    if len(sys.argv) > 1  and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run()
