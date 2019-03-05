from flask import render_template, flash

from app import create_app



if __name__ == '__main__':
    app = create_app()


    # 仅供测试
    @app.route('/')
    def hello():
        return 'Hello World 啊哈哈'  # return时flask会自动封装成一个response对象。

    @app.route('/test')
    def test():
        data = {
            "age":18,
            "name":"layman"
        }
        flash("hello layman") # 消息闪现是需要用到session的，故需要配置密钥
        flash("hello layman again")
        return render_template("test1.html", data = data)

    app.run(
        host = app.config['HOST'],
        port = app.config['PORT'],
        debug = app.config['DEBUG'],
        threaded = True # 多线程选项，默认True开启
    )