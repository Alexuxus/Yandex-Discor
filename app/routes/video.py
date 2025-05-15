from flask import Blueprint, render_template, url_for
from flask_login import login_required, current_user

bp = Blueprint('video', __name__, url_prefix='/video')

@bp.route('/call/<friend_id>')
@login_required
def video_call(friend_id):
    room_id = f"{min(current_user.user_id, int(friend_id))}-{max(current_user.user_id, int(friend_id))}"
    return render_template('video_call.html', room_id=room_id, user_id=current_user.user_id,
                           username=current_user.username, friend_id=friend_id)
