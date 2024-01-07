from forms.article_form import ArticleForm, CategoryForm, LoginForm, RegistrationForm
from models import db, Article, Category, User, Role
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from datetime import datetime, timedelta
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = '1234AAA'
db.init_app(app)
migrate = Migrate(app, db)


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_id == 2

    def inaccessible_callback(self, name, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login', next=request.url))
        else:
            flash('Доступ запрещен')
            return redirect(url_for('index'))


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_id == 2

    def inaccessible_callback(self, name, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login', next=request.url))
        else:
            flash('Доступ запрещен')
            return redirect(url_for('index'))


# Инициализируем админ-панель
admin = Admin(app, index_view=MyAdminIndexView())


# Создаем наследованный класс от ModelView для пользователей
class UserAdmin(ModelView):
    column_list = ('username', 'email', 'role')
    column_searchable_list = ('username', 'email')
    column_filters = ('role.name',)
    form_columns = ('username', 'email', 'role')


# Регистрируем нашу настроенную вьюху в админ-панели

admin.add_view(UserAdmin(User, db.session))
admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(Category, db.session))




with app.app_context():
    db.create_all()


def trim_article_content(content, max_length=1500):
    if len(content) <= max_length:
        return content, False  # Нет необходимости в кнопке "Читать далее"

    # Разделяем контент на блоки по тегам <pre> и <img>
    parts = re.split('(<pre.*?>.*?</pre>)', content, flags=re.DOTALL)
    trimmed_content = ""
    current_length = 0
    more_link_needed = False  # Флаг для определения необходимости кнопки "Читать далее"

    for part in parts:
        if '<pre' in part or '<img' in part:
            # Если блок кода или изображение начинается до лимита, добавляем целиком
            if current_length + len(part) <= max_length:
                trimmed_content += part
                current_length += len(part)
            else:
                # Если блок кода или изображение начинается внутри лимита, но заканчивается за его пределами,
                # добавляем его целиком и прекращаем дальнейшее добавление
                trimmed_content += part
                more_link_needed = True
                break
        else:
            # Добавляем текст до достижения лимита
            if current_length + len(part) <= max_length:
                trimmed_content += part
                current_length += len(part)
            else:
                trimmed_content += part[:max_length - current_length]
                more_link_needed = True
                break

    if more_link_needed:
        trimmed_content += '...'  # Добавляем многоточие только если контент обрезан

    return trimmed_content, more_link_needed


@app.route('/')
def index():
    query = request.args.get('query')
    if query:
        articles = Article.query.filter(
            Article.title.contains(query) | Article.content.contains(query)
        ).order_by(Article.date_posted.desc()).all()
    else:
        articles = Article.query.order_by(Article.date_posted.desc()).all()

    # Применяем функцию обрезки содержимого для каждой статьи
    for article in articles:
        article.trimmed_content, article.need_more_link = trim_article_content(article.content)

    return render_template('index.html', articles=articles)



@app.route('/create_article', methods=['GET', 'POST'])
@login_required
def create_article():
    form = ArticleForm()
    if form.validate_on_submit():
        new_article = Article(title=form.title.data, content=form.content.data, category_id=form.category.data,
                              author_id=current_user.id)
        db.session.add(new_article)
        db.session.commit()
        flash('Статья успешно создана.')
        return redirect(url_for('index'))
    return render_template('article_create.html', form=form)


@app.route('/edit-article/<int:article_id>', methods=['GET', 'POST'])
@login_required
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
@login_required
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('index'))


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
@login_required
def add_category():
    form = CategoryForm()

    # Получить URL предыдущей страницы из сессии, если он был сохранен
    previous_page = session.get('previous_page')

    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()

        # Если URL предыдущей страницы был сохранен в сессии, перенаправить на него
        if previous_page:
            return redirect(previous_page)
        else:
            # Если URL предыдущей страницы не найден, перенаправить на главную страницу, например
            return redirect(url_for('index'))

    # Сохранить текущий URL в сессии как предыдущий перед отображением формы
    session['previous_page'] = request.url

    return render_template('add_category.html', form=form)


@app.route('/filter_by_date', methods=['GET'])
def filter_by_date():
    date_str = request.args.get('date')
    if date_str:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        next_day = date + timedelta(days=1)
        articles = Article.query.filter(Article.date_posted >= date, Article.date_posted < next_day).all()
    else:
        articles = Article.query.all()
    return render_template('search_results.html', articles=articles)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Получаем роль пользователя по умолчанию (например, "Пользователь")
        default_role = Role.query.filter_by(name='Пользователь').first()
        if not default_role:
            # Если такой роли нет, создаем ее
            default_role = Role(name='Пользователь')
            db.session.add(default_role)
            db.session.commit()

        # Создаем нового пользователя с ролью по умолчанию
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.role = default_role  # Присваиваем роль
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/category/<category_name>')
def category(category_name):
    category = Category.query.filter_by(name=category_name).first_or_404()
    articles = Article.query.filter_by(category=category).all()
    return render_template('index.html', articles=articles)


@app.context_processor
def inject_categories():
    categories = Category.query.all()
    return dict(categories=categories)


if __name__ == "__main__":
    app.run(debug=True)
