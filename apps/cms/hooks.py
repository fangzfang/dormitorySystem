#encoding: utf-8
from .views import bp
import config
from flask import session, g
from .models import CMSUser, CMSPermission

"""
    钩子函数：处理上下文都会用到的信息
    请求进入视图函数之前判断用户是否登录，
    若已登录，则将当前用户的信息添加到g对象里面
"""
@bp.before_request
def before_request():
    if config.CMS_USER_ID in session:
        user_id = session.get(config.CMS_USER_ID)
        user = CMSUser.query.get(user_id)
        if user:
            #使用flask中的g对象
            g.cms_user = user

#在钩子函数中使用蓝图.context_processor
# 以后只要是此蓝图返回的模板，都会携带此数据
@bp.context_processor
def cms_context_processor():
    return {'CMSPermission':CMSPermission}