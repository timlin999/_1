from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf.file import FileRequired, FileAllowed, FileField

class LoginForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember = BooleanField("Запомнить меня")
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired()])
    name = StringField("Имя", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email(message='Некорректный email')])
    password = PasswordField("Пароль", validators=[DataRequired()])
    password2 = PasswordField("Повторите пароль",
                              validators=[DataRequired(), EqualTo('password', message='Пароли не совпадают')])
    submit = SubmitField('Зарегистрироваться')

class ReviewForm(FlaskForm):
    name = StringField('Ваше имя',
                       validators=[DataRequired(message="Поле не должно быть пустым")])
    text = TextAreaField('Текст отзыва',
                         validators=[DataRequired(message="Поле не должно быть пустым")])
    score = SelectField('Оценка',
                        choices=[(i, i) for i in range(1, 11)])
    submit = SubmitField('Добавить отзыв')


class MovieForm(FlaskForm):
    title = StringField('Название',
                        validators=[DataRequired(message="Поле не должно быть пустым")])
    description = TextAreaField('Описание',
                                validators=[DataRequired(message="Поле не должно быть пустым")])
    image = FileField('Постер фильма',
                      validators=[FileRequired(message="Поле не должно быть пустым"),
                                  FileAllowed(['jpg', 'jpeg', 'png'], message="Неверный формат файла")])
    submit = SubmitField('Добавить фильм')
