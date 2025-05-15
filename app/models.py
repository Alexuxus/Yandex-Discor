from app import db
from flask_login import UserMixin
import re
import datetime

class Register(UserMixin, db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, unique=True, nullable=True)
    friends = db.Column(db.String(255), default='')
    avatar_color = db.Column(db.String(7), default='#CCCCCC')

    def __repr__(self):
        return f"Register('{self.username}')"

    def добавить_друга(self, friend_id):
        if not self.является_другом(friend_id):
            self.friends = (self.friends + '///#///' + str(friend_id)).strip('///#///')
            return True
        return False

    def удалить_друга(self, friend_id):
        friend_id_str = str(friend_id)
        friends_list = self.получить_id_друзей()
        if friend_id in friends_list:
            friends_list.remove(friend_id)
            self.friends = '///#///'.join(map(str, friends_list))
            return True
        return False

    def получить_id_друзей(self):
        if self.friends:
            return [int(friend_id) for friend_id in re.split(r'///#///', self.friends)]
        return []

    def является_другом(self, friend_id):
        return friend_id in self.получить_id_друзей()


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    chat_db_name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return (f"Message(from_user_id={self.from_user_id}, message='{self.message}', timestamp={self.timestamp},"
                f" chat_db_name='{self.chat_db_name}')")
