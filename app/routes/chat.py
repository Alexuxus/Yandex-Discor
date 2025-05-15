from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.forms import AddUserForm, ChatForm
from app.models import Register
from app import db, socketio
from app.utils import create_avatar, create_chat_db, add_message_to_chat, get_chat_messages, add_string_segregation
import datetime

bp = Blueprint('chat', __name__, url_prefix='/chat')

@bp.route("/", methods=["GET", "POST"])
@login_required
def chat():
    add_user_form = AddUserForm()
    chat_form = ChatForm()

    if add_user_form.validate_on_submit():
        friend_username = add_user_form.username.data
        friend_user_id = add_user_form.user_id.data

        friend_to_add = Register.query.filter_by(username=friend_username, user_id=friend_user_id).first()

        if friend_to_add:
            if not current_user.является_другом(friend_to_add.user_id):
                current_user.добавить_друга(friend_to_add.user_id)
                friend_to_add.добавить_друга(current_user.user_id)

                db.session.commit()
                flash(f"Пользователь {friend_username} добавлен в друзья!", "success")
                chat_db_name = create_chat_db(current_user.user_id, friend_to_add.user_id)
            else:
                flash(f"Пользователь {friend_username} уже ваш друг.", "info")
        else:
            flash("Пользователь не найден.", "error")

        return redirect(url_for('chat.chat'))

    friend_ids = current_user.получить_id_друзей()
    friends = Register.query.filter(Register.user_id.in_(friend_ids)).all()

    selected_friend_id = request.args.get('friend_id')
    selected_friend = None
    messages = []

    if selected_friend_id:
        selected_friend = Register.query.filter_by(user_id=selected_friend_id).first()
        if selected_friend:
            chat_db_name = f"{min(current_user.user_id, int(selected_friend_id))}-{max(current_user.user_id,
                                                                                       int(selected_friend_id))}.db"
            messages_data = get_chat_messages(chat_db_name)
            for message_obj in messages_data:
                user = Register.query.filter_by(user_id=message_obj.from_user_id).first()
                if user:
                    formatted_time = message_obj.timestamp.strftime('%H:%M')
                    formatted_date = message_obj.timestamp.strftime('%d.%m.%Y')
                    formatted_message = add_string_segregation(message_obj.message)

                    messages.append({
                        'username': user.username,
                        'message': formatted_message,
                        'time': formatted_time,
                        'date': formatted_date,
                        'avatar': create_avatar(user.username, user.avatar_color)
                    })

        if chat_form.validate_on_submit() and selected_friend_id:
            message = chat_form.message.data
            to_user_id = int(selected_friend_id)
            chat_db_name = f"{min(current_user.user_id, to_user_id)}-{max(current_user.user_id, to_user_id)}.db"
            add_message_to_chat(chat_db_name, current_user.user_id, message)
            user = Register.query.filter_by(user_id=current_user.user_id).first()
            if user:
                avatar = create_avatar(user.username, user.avatar_color)
                formatted_message = add_string_segregation(message)
                socketio.emit('new_message', {
                    'username': current_user.username,
                    'message': formatted_message,
                    'friend_id': to_user_id,
                    'avatar': avatar,
                    'time': datetime.datetime.now().strftime('%H:%M'),
                    'date': datetime.datetime.now().strftime('%d.%m.%Y')
                }, room=f"chat_{min(current_user.user_id, to_user_id)}-{max(current_user.user_id, to_user_id)}")
            return redirect(url_for('chat.chat', friend_id=selected_friend_id))

    return render_template("base_chat.html",
                           add_user_form=add_user_form,
                           friends=friends,
                           chat_form=chat_form,
                           selected_friend=selected_friend,
                           messages=messages,
                           create_avatar=create_avatar
                           )

@bp.route('/start_chat', methods=['POST'])
def start_chat():
    friend_id = request.get_json()['friend_id']
    return jsonify({'redirect': url_for('chat.chat', friend_id=friend_id)})
