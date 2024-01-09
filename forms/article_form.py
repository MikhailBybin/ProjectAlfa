from flask_wtf import FlaskForm
from models import Category
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo


class ArticleForm(FlaskForm):
    title = StringField('Название статьи', validators=[DataRequired()])
    content = TextAreaField('Содержание')
    category = SelectField('Категория:', coerce=int)
    submit = SubmitField('Сохранить')

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.category.choices = [(c.id, c.name) for c in Category.query.all()]


class CategoryForm(FlaskForm):
    name = StringField('Название категории', validators=[DataRequired()])
    submit = SubmitField('Добавить категорию')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Никнейм', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm = PasswordField('Подтверждение пароля', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')
