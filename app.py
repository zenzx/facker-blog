from flask import Flask, render_template
from flask_flatpages import FlatPages

app = Flask(__name__)
app.config.from_pyfile('settings.py')
pages = FlatPages(app)


@app.route('/index/<int:types>', methods=['GET', 'POST'])
@app.route('/<int:types>', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def home(types=10):
    posts = [page for page in pages if 'date' in page.meta and 'top' not in page.meta]
    # Sort pages by date
    sorted_posts = sorted(posts, reverse=True,
                          key=lambda page: page.meta['date'])

    top_articles = [page for page in pages if 'date' in page.meta]

    def top_article(articles):
        for article in articles:
            if 'top' in article.meta:
                return article
    
    if types < 10:
        types = 10
    page_article = types - 10
    post = sorted_posts[page_article:types]

    return render_template('index.html', top_page=top_article(top_articles), pages=post, type=types)


@app.route('/about')
def about():
    facker_about = pages.get('about')
    return render_template('page.html', page=facker_about)


@app.route('/article/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    return render_template('page.html', page=page)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
