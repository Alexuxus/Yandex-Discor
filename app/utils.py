import random

def gen_unique_id():
    from app.models import Register  # Import here to avoid circular import
    while True:
        user_id = random.randint(10000, 99999)
        if not Register.query.filter_by(user_id=user_id).first():
            return user_id

def gen_avatar_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

def create_avatar(username, color):
    initial = username[0].upper()
    return f'<div class="avatar" style="background-color: {color};">{initial}</div>'

def create_chat_db(user1_id, user2_id):
    db_name = f"{min(user1_id, user2_id)}-{max(user1_id, user2_id)}.db"
    return db_name

def add_message_to_chat(db_name, from_user_id, message_text):
    from app.models import Message
    from app import db
    new_message = Message(
        from_user_id=from_user_id,
        message=message_text,
        chat_db_name=db_name
    )
    db.session.add(new_message)
    db.session.commit()

def get_chat_messages(db_name):
    from app.models import Message
    messages = Message.query.filter_by(chat_db_name=db_name).order_by(Message.timestamp).all()
    return messages

def add_string_segregation(text, max_length=50):
    return '<br>'.join(text[i:i + max_length] for i in range(0, len(text), max_length))
