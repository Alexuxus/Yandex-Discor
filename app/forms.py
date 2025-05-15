from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Optional

class RegistrationForm(FlaskForm):
    username = StringField(label="Имя пользователя", validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField(label="Пароль", validators=[DataRequired(), Length(min=8, max=20)])
    submit = SubmitField('Регистрация')


class LoginForm(FlaskForm):
    username = StringField(label="Имя пользователя", validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField(label="Пароль", validators=[DataRequired(), Length(min=8, max=20)])
    submit = SubmitField('Войти')


class AddUserForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=4, max=20)])
    user_id = IntegerField('ID пользователя', validators=[DataRequired()])
    submit = SubmitField('Добавить друга')


class ChatForm(FlaskForm):
    message = TextAreaField('Сообщение', validators=[DataRequired()])
    submit = SubmitField('Отправить')
