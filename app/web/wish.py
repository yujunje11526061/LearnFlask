from flask import url_for, flash,  render_template
from flask_login import current_user, login_required
from werkzeug.utils import redirect

from app.models.base import db
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_model.wish import MyWishes
from . import web




@web.route('/my/wish')
@login_required
def my_wish():
    my_wishes_list = Wish.get_user_wishes(current_user.id)
    isbn_list = [wish.isbn for wish in my_wishes_list]
    gift_count_list = Gift.get_all_gifts(isbn_list)
    view_model_of_my_wishes = MyWishes(my_wishes_list=my_wishes_list, gift_count_list=gift_count_list)
    return render_template("my_wishes.html", wishes=view_model_of_my_wishes.wishes)


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_wish_list(isbn):
        with db.auto_commit(): # 由上下文管理函数来封装提交与回滚的 try  except  代码块。
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.id
            db.session.add(wish)
    else:
        flash("这本书已经添加了或在你的心愿列表中，请勿重复添加")
    # 视图函数必须有返回，此业务逻辑下可以重定向到某个页面，但更合适的是保留在当前页面，应使用ajax技术，涉及前端技术，此处先用普通重定向
    return redirect(url_for("web.book_detail", isbn = isbn))


@web.route('/satisfy/wish/<int:wid>')
def satisfy_wish(wid):
    pass


@web.route('/wish/book/<isbn>/redraw')
def redraw_from_wish(isbn):
    pass
