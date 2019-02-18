from app import create_app






if __name__ == '__main__':
    app = create_app()


    # 仅供测试
    @app.route('/')
    def hello():
        return 'Hello World 啊哈哈'  # return时flask会自动封装成一个response对象。

    app.run(
        host = app.config['HOST'],
        port = app.config['PORT'],
        debug = app.config['DEBUG']
    )