from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', name='fk_article_category'), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref='articles')


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    articles = db.relationship('Article', backref='category', lazy=True)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref='users')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def register_user(username, email, password):
        user_role = Role.query.filter_by(name='Пользователь').first()
        print(f'User Role: {user_role}')  # Debug print
        if user_role is None:
            print('User role "Пользователь" not found. Creating it.')
            user_role = Role(name='Пользователь')
            db.session.add(user_role)
            db.session.commit()
            user_role = Role.query.filter_by(name='Пользователь').first()  # Fetch again after commit
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        new_user.role = user_role
        db.session.add(new_user)
        db.session.commit()
        print(f'New User: {new_user.username}, Role: {new_user.role.name}')  # Debug print


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
