from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import RegistrationForm, LoginForm
from app.models import Register
from app import db
from app.utils import gen_unique_id, gen_avatar_color

bp = Blueprint('main', __name__)

@bp.route("/")
def главная():
    return redirect(url_for('main.register'))

@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == 'GET':
        username = request.args.get('username')
        if username:
            form.username.data = username

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = Register.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Вход выполнен успешно.")
            return redirect(url_for('chat.chat'))
        else:
            flash("Неверное имя пользователя или пароль", 'error')
    return render_template('login.html', form=form)

@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        existing_user = Register.query.filter_by(username=username).first()

        if existing_user:
            flash('Это имя пользователя уже занято. Пожалуйста, выберите другое.', 'error')
            return render_template('register.html', form=form)

        hashed_password = generate_password_hash(password)
        unique_user_id = gen_unique_id()
        avatar_color = gen_avatar_color()

        new_user = Register(
            username=form.username.data,
            password=hashed_password,
            user_id=unique_user_id,
            avatar_color=avatar_color
        )
        db.session.add(new_user)
        try:
            db.session.commit()
            flash("Аккаунт создан успешно! Теперь вы можете войти", "success")

            user = Register.query.filter_by(username=username).first()
            if user:
                login_user(user)
                return redirect(url_for('chat.chat'))

        except Exception as e:
            db.session.rollback()
            print(f"Ошибка базы данных: {e}")
            flash("Произошла ошибка во время регистрации. Пожалуйста, попробуйте еще раз.", "error")

    return render_template("register.html", form=form)

@bp.route("/logout")
#@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))
