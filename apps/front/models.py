#encoding: utf-8

from exts import db

class FrontUser(db.Model):
    __tablename__ = 'front_user'
    #考虑到安全性，不用自增id做主键，这里使用随机的字符串表示id
    id = db.Column()