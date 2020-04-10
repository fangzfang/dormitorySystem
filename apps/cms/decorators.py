#encoding: utf-8
from flask import session, redirect, url_for, g
from functools import wraps
import config

'''
    装饰器的本质是一个闭包函数,作用在于不改变原函数功能和调用方法的基础上给它添加额外的功能.
    装饰器在装饰一个函数时,原函数就成了一个新的函数,也就是说其属性会发生变化,
    所以为了不改变原函数的属性,我们会调用functools中的wraps装饰器来保证原函数的属性不变.
'''

def login_required(func):
    #inner的参数要与func中的参数一致，此时并不知道func中的参数，可以使用*args，**kwargs代替
    #用@wraps装饰器可以保留func中的原有属性
    @wraps(func)
    def inner(*args, **kwargs):
        #判断session中是否存有user_id，如果有代表已经登录
        #session是字典格式，查看key值是否存在
        if config.CMS_USER_ID in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('cms.login'))
    return inner

# @login_required
# def index():
#     return 'cms.index'

#其实index就等价于inner了
# index = login_required(index) == inner
# index(username) = inner(username)

#让装饰器能够接受参数，这样对于不同的权限，传递不同的参数
def permission_required(permission):
    #真正的接收函数的
    def outter(func):
        @wraps(func)
        def inner(*args, **kwargs):
            #首先获取锥对象
            user = g.cms_user
            if user.has_permission(permission):
                return func(*args, **kwargs)
            else:
                return redirect(url_for('cms.index'))
        return inner
    return outter




