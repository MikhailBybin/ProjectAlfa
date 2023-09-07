from flask import Flask, render_template, redirect, url_for
from flask import Markup
from forms.article_form import ArticleForm, CategoryForm
from models import db, Article, Category
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from flask import request
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'some_secret_key'
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
    query = request.args.get('query')

    if query:
        articles = Article.query.filter(Article.title.contains(query) | Article.content.contains(query)).all()
    else:
        articles = Article.query.all()

    return render_template('index.html', articles=articles)


@app.route('/create_article', methods=['GET', 'POST'])
def create_article():
    form = ArticleForm()
    if form.validate_on_submit():
        new_article = Article(title=form.title.data, content=form.content.data, category_id=form.category.data)
        db.session.add(new_article)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('article_create.html', form=form)


@app.route('/edit-article/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    article = Article.query.get_or_404(article_id)
    form = ArticleForm(obj=article)

    if form.validate_on_submit():
        article.title = form.title.data
        article.content = form.content.data
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('article_edit.html', form=form, article=article)


@app.route('/delete-article/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('index'))


@app.template_filter('md')
def md_to_html(txt):
    exts = ['fenced_code', CodeHiliteExtension(linenums=True)]
    return Markup(markdown(txt, extensions=exts))


@app.route('/search')
def search():
    query = request.args.get('query')
    articles = Article.query.filter(Article.title.contains(query) | Article.content.contains(query)).all()
    return render_template('search_results.html', articles=articles)


@app.route('/article/<int:article_id>')
def article_detail(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template('article_detail.html', article=article)


@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('index'))  # или другой маршрут
    return render_template('add_category.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
