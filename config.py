#encoding: utf-8
import os
#配置文件

DEBUG = True
#数据库的配置
DB_USERNAME = 'root'
DB_PASSWORD = '12345678'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'system'

SECRET_KEY = os.urandom(24)
#设置session的过期时间,默认设置为31天，此时可以更改过期时间

# permanent_session_lifetime =

DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=UTF8MB4' % \
         (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
#关闭跟踪
SQLALCHEMY_TRACK_MODIFICATIONS = False

CMS_USER_ID = 'cms_user_id'

#邮箱的配置

#发送者邮箱的服务器地址
MAIL_SERVER = 'smtp.qq.com'
#端口号：这里使用了加密的协议，
MAIL_PORT = '587'
MAIL_USE_TLS = True
# MAIL_USE_SSL = False
# MAIL_DEBUG : 默认为 app.debug
MAIL_USERNAME = '1580658679@qq.com'
MAIL_PASSWORD = 'psywybqfsacnffjh'
MAIL_DEFAULT_SENDER = '1580658679@qq.com'


# MAIL_USE_TLS : 端口号为587
# MAIL_USE_SSL :  端口号为465
# 非SSL协议端口号为25，但是QQ邮箱不支持非加密方式发送邮件
