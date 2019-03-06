
from . import web
from flask_login import login_required


@web.route('/my/gifts')
@login_required # 插件flask_login插件提供的验证是否登陆的装饰器
def my_gifts():
    return "my gifts"


@web.route('/gifts/book/<isbn>')
def save_to_gifts(isbn):
    pass


@web.route('/gifts/<gid>/redraw')
def redraw_from_gifts(gid):
    pass



