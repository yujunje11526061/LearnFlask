from flask import render_template
from flask_login import login_required, current_user

from app.models.gift import Gift
from app.models.user import User
from app.view_model.book import BookViewModel
from . import web





@web.route('/')
@login_required
def index():
    '''
    主页放最近添加且还在架的礼物
    :return:
    '''
    recent_gifts= Gift.recent()
    book_list = [BookViewModel(gift.book) for gift in recent_gifts]
    return render_template("index.html", recent = book_list)


@web.route('/personal')
@login_required
def personal_center():
    user = User.query.get(current_user.id)
    return render_template("personal.html", user = user.baseInfo)
