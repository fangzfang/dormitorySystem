#encoding: utf-8
#第三方文件

from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

#创建一个SQLAlchemy对象
db = SQLAlchemy()

#创建一个Mail对象
mail= Mail()