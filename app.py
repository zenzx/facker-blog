from flask import Flask, render_template
from flask_flatpages import FlatPages

app = Flask(__name__)
app.config.from_pyfile('settings.py')
pages = FlatPages(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    posts = [page for page in pages if 'date' in page.meta and 'top' not in page.meta]
    # Sort pages by date
    sorted_posts = sorted(posts, reverse=True,
                          key=lambda page: page.meta['date'])


    top_articles = [page for page in pages if 'date' in page.meta]

    def top_article(articles):
        for article in articles:
            if 'top' in article.meta:
                return article

    return render_template('index.html', top_page=top_article(top_articles), pages=sorted_posts)

@app.route('/about.html')
def about():
    facker_about = pages.get('about')
    return render_template('page.html', page=facker_about)


@app.route('/article/<path:path>.html')
def page(path):
    page = pages.get_or_404(path)
    return render_template('page.html', page=page)


if __name__ == '__main__':
    app.run()
    #    app.run(host='0.0.0.0')
