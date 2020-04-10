#encoding: utf-8

from wtforms import  StringField, IntegerField, ValidationError
from wtforms.validators import Email, InputRequired, Length, EqualTo
from ..forms import BaseForm
from utils import dmcache
from flask import g

class LoginForm(BaseForm):
    email = StringField(validators=[InputRequired(message='请输入邮箱'), Email(message='请输入正确的邮箱格式')])
    password = StringField(validators=[Length(6,20, message='请输入正确格式的密码')])
    #记住我的标记可传可不传，所以不需要验证
    remember = IntegerField()

class ResetpwdForm(BaseForm):
    # oldpwd = StringField(validators=[InputRequired(message='请输入正确格式的旧密码'), Length(6, 20, message='密码6~20位')])
    # newpwd = StringField(validators=[InputRequired(message='请输入正确格式的新密码'), Length(6, 20, message='密码6~20位')])
    # newpwd2 = StringField(validators=[EqualTo('newpwd', message='两次密码不一致')])

    oldpwd = StringField(validators=[Length(6, 20, message='密码6~20位')])
    newpwd = StringField(validators=[Length(6, 20, message='密码6~20位')])
    newpwd2 = StringField(validators=[EqualTo('newpwd', message='两次密码不一致')])

class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确格式的邮箱')])
    captcha = StringField(validators=[Length(min=6, max=6, message='请输入正确长度的验证码')])

    #验证邮箱和验证码是否一致
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        #从memcache中获取验证码
        captcha_cache = dmcache.get(email)
        #如果从memcache中能获取到验证码，而且不区分大小写
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            return  ValidationError('邮箱验证码错误！')

    def validate_email(self, field):
        email = field.data
        user = g.cms_user
        if user.email == email:
            return ValidationError('不能修改为相同的邮箱！')