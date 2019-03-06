
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user

from app.models.base import db
from app.forms.auth import RegisterForm, loginForm
from app.models.user import User
from . import web
from werkzeug.security import generate_password_hash



@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        user = User()
        user.set_attr(form.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("web.login"))
    return render_template("auth/register.html", form = form)



@web.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=form.data["email"]).first()
        if user and user.check_password(form.data["password"]):
            # 调用flask_login插件的login_user函数为用户生成加密的cookie。各种参数见源码。
            login_user(user, remember = False)
            # return redirect(request.referrer) 登录成功后重定向回上一个页面。由于referrer参数经常为空，故此法重定向到上一个页面经常失效。
            # 另一个方案，在重定向到登录页面的url链接后面加一个next参数，记录当前页面，以便登录成功后通过取next重定向回来。flask_login插件会自动在重定向回登录页面时在后面加一个参数next。利用好浏览器的开发者工具。
            next = request.args.get("next")
            # 防御编程，为空则给主页默认值。后一个判断用于防止重定向攻击。攻击者仿照自动生成的登录页面，手动构造一个next参数为别的网站地址的url。
            # 更好的防止重定向攻击的方法是检查目标域名是否属于本域名。利用urllib.parse来分析url。
            if next is None or not next.startswith("/"):
                next = url_for("web.index")
            return redirect(next)
        else:
            flash("不存在账号或用户名、密码不正确")
    return render_template("auth/login.html",form = form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    pass


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    pass


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    pass
