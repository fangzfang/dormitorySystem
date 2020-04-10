#encoding: utf-8

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from main import app
from exts import db
from apps.cms import models as cms_models

#创建一个Python模板运行命令脚本，可起名为manage.py；

#在该文件中，必须有一个Manager实例，Manager类追踪所有在命令行中调用的命令和处理过程的调用运行情况；

#Manager只有一个参数——Flask实例，也可以是一个函数或其他的返回Flask实例；
#声称一个全局变量
CMSUser = cms_models.CMSUser
CMSRole = cms_models.CMSRole
CMSPermission = cms_models.CMSPermission


manager = Manager(app)
#绑定db, app
Migrate(app, db)


manager.add_command('db', MigrateCommand)

#添加用户
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
def create_cms_user(username, password, email):
    user = CMSUser(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print('cms用户添加成功')

'''
    在终端直接执行python manage.py create_role 就能生成表中的信息
'''
@manager.command
def create_role():
    # 1、访问者
    visitor = CMSRole(name = '访问者', desc = '只能访问相关数据，不能修改')
    visitor.permissions = CMSPermission.VISITOR

    # 2、运营角色（修改个人信息，管理帖子，管理评论）
    operator = CMSRole(name = '运营', desc = '管理帖子， 管理评论，管理前台用户')
    operator.permissions = CMSPermission.VISITOR | CMSPermission.POSTER \
                           | CMSPermission.CMSUSER | CMSPermission.COMMENTER \
                           | CMSPermission.FRONTUSER

    # 3、管理员（拥有绝大部分权限）
    admin = CMSRole(name = '管理员', desc = '拥有本系统所有权限')
    admin.permissions = CMSPermission.VISITOR | CMSPermission.POSTER \
                        | CMSPermission.CMSUSER | CMSPermission.COMMENTER \
                        | CMSPermission.FRONTUSER | CMSPermission.BOARDER


    # 4、开发者（拥有所有权限）
    developer = CMSRole(name = '开发者', desc = '开发人员专用角色')
    developer.permissions = CMSPermission.All_PERMISSION
    db.session.add_all([visitor, operator, admin, developer])
    db.session.commit()

#将用户添加到某个组当中
#@manager.option('-简写参数名','--全写参数名',dest='函数中的参数')
@manager.option('-e', '--email', dest = 'email') #用邮箱指定用户
@manager.option('-n', '--name', dest = 'name') #角色名字
def add_user_to_role(email, name):
    user = CMSUser.query.filter_by(email=email).first()
    #判断是否有这个用户
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print('用户添加到角色成功！')
        else:
            print('没有这个角色：%s' % role)
    else:
        print('%s邮箱没有这个用户：' % email)


#测试用户是否有相应的权限
@manager.command
def test_permission():
    user = CMSUser.query.first() #获取该用户
    if user.has_permission(CMSPermission.VISITOR):
        print('这个用户有访问者的权限')
    else:
        print('这个用户没有访问者的权限')

    if user.is_developer:
        print('这个用户是开发者')
    else:
        print('这个用户不是开发者')


db.init_app(app)
if __name__ == '__main__':
    manager.run()
