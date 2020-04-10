from flask import Flask
app = Flask(__name__)
from apps.cms import bp as cms_bp
from apps.front import bp as front_bp
from apps.common import bp as common_bp
import config as config
from exts import db, mail
from flask_wtf import CSRFProtect

#需要进行功能上的划分
#前台、后台、公共的,成为蓝图
#apps包里存放所有的功能模块
# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(config)
#     app.register_blueprint(cms_bp)
#     app.register_blueprint(front_bp)
#     app.register_blueprint(common_bp)
#
#     db.init_app(app)
#     mail.init_app(app)
#     CSRFProtect(app)
#     return app

app = Flask(__name__)

app.config.from_object(config)
app.register_blueprint(cms_bp)
app.register_blueprint(front_bp)
app.register_blueprint(common_bp)

db.init_app(app)
#对mail进行初始化
mail.init_app(app)
#app开始有CSRF的保护
CSRFProtect(app)

if __name__ == '__main__':
    # app = create_app()
    app.run()