from flask import flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import or_, desc

from app.models.base import db
from app.forms.book import DriftForm
from app.models.drift import Drift
from app.models.gift import Gift
from app.view_model.book import BookViewModel
from app.view_model.drift import DriftCollection
from utils import send_mail
from . import web



@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    current_gift = Gift.query.get_or_404(gid)
    if current_gift.is_own_gift(current_user.id):
        flash("这是你自己的书,不需要索要")
        return redirect(url_for("web.book_detail", isbn= current_gift.isbn))
    if Drift.query.filter_by(requester_id=current_user.id, gifter_id = current_gift.uid, isbn = current_gift.isbn).first():
        flash("你已向对方发送过请求了,请不要重复发送")
        return redirect(url_for("web.book_detail", isbn=current_gift.isbn))
    if not current_user.can_send_drift():
        return render_template("not_enough_beans.html", beans = current_user.beans)

    form = DriftForm(request.form)
    if request.method == "POST" and form.validate():
        save_drift(form, current_gift)
        send_mail(current_gift.user.email, "有人想要一本书", "email/get_gift.html", wisher= current_user, gift = current_gift)
        return redirect(url_for("web.pending"))

    gifterSummary = current_gift.user.summary
    return render_template("drift.html", gifter = gifterSummary, user_beans = current_user.beans, form=form)



@web.route('/pending')
@login_required
def pending():
    # 带有逻辑表达式的查询用filter, filter_by只能是默认的and
    drifts = Drift.query.filter(or_(Drift.requester_id==current_user.id, Drift.gifter_id==current_user.id)).order_by(desc(Drift.create_time)).all()

    views = DriftCollection(drifts, current_user.id)
    return render_template("pending.html", drifts = views.data)




@web.route('/drift/<int:did>/reject')
def reject_drift(did):
    pass


@web.route('/drift/<int:did>/redraw')
def redraw_drift(did):
    pass


@web.route('/drift/<int:did>/mailed')
def mailed_drift(did):
    pass

def save_drift(drift_form, current_gift):
    with db.auto_commit():
        drift= Drift()
        # wtforms提供了把表单数据复制到模型的方法,只要对应字段的名城都一致
        drift_form.populate_obj(drift)
        drift.gift_id = current_gift.id
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gifter_nickname = current_gift.user.nickname
        drift.gifter_id = current_gift.uid

        book = BookViewModel(current_gift.book)

        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image
        drift.isbn = book.isbn

        current_user.beans -= 1

        db.session.add(drift)
