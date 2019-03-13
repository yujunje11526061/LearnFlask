from flask import current_app, flash, redirect, url_for, render_template

from app.models.base import db
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_model.gift import MyGifts
from . import web
from flask_login import login_required, current_user

# current_user如同flask的current_app，是当前用户的代理。由flask_login帮我们管理当前登录的用户。
# 通过@login_manager.user_loader装饰的get_uesr函数取到。函数参数为uid。此函数通常定义在user模型文件中。

@web.route('/my/gifts')
@login_required # 插件flask_login插件提供的验证是否登陆的装饰器
def my_gifts():
    my_gifts_list = Gift.get_user_gifts(current_user.id)
    isbn_list = [gift.isbn for gift in my_gifts_list]
    wish_count_list = Wish.get_all_wishes(isbn_list)
    view_model_of_my_gifts = MyGifts(my_gifts_list=my_gifts_list,wish_count_list=wish_count_list)
    return render_template("my_gifts.html", gifts = view_model_of_my_gifts.gifts)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_gift_list(isbn):
        with db.auto_commit(): # 由上下文管理函数来封装提交与回滚的 try  except  代码块。
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            current_user.beans += current_app.config["BEAN_GIVEN_BY_SYSTEM_PER_BOOK"]
            db.session.add(gift)
    else:
        flash("这本书已经添加了或在你的礼物列表中，请勿重复添加")
    # 视图函数必须有返回，此业务逻辑下可以重定向到某个页面，但更合适的是保留在当前页面，应使用ajax技术，涉及前端技术，此处先用普通重定向
    return redirect(url_for("web.book_detail", isbn = isbn))


@web.route('/gifts/<gid>/redraw')
def redraw_from_gifts(gid):
    pass



