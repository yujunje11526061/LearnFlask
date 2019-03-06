from . import web





@web.route('/')
def index():
    return "11111"


@web.route('/personal')
def personal_center():
    pass
