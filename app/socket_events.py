from flask_socketio import emit, join_room
from flask_login import current_user
from app import socketio

@socketio.on('connect')
#@login_required
def handle_connect():
    print(f"User {current_user.user_id} connected")
    friend_ids = current_user.получить_id_друзей()
    for friend_id in friend_ids:
        room = f"chat_{min(current_user.user_id, friend_id)}-{max(current_user.user_id, friend_id)}"
        join_room(room)
        print(f"User {current_user.user_id} joined room {room}")

@socketio.on('join')
def on_join(data):
    user_id = data['user_id']
    friend_id = data['friend_id']
    room = f"chat_{min(user_id, friend_id)}-{max(user_id, friend_id)}"
    join_room(room)
    print(f"User {user_id} joined room {room}")

@socketio.on('new_message')
def handle_new_message(data):
    room = f"chat_{min(int(data['friend_id']), current_user.user_id)}-{max(int(data['friend_id']), current_user.user_id)}"
    emit('new_message', data, room=room)
