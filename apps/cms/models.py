#encoding
#cms管理系统
#与cms相关的所有模型

from exts import db
from datetime import  datetime
#利用flask框架的生成哈希密码和查看哈希密码是否一致
from werkzeug.security import  generate_password_hash, check_password_hash

#权限部分
class CMSPermission(object):
    #255的二进制表示方式：1111 1111，其中的每一位代表一个权限
    All_PERMISSION = 0b11111111  #代表拥有所有权限
    #1、访问者权限
    VISITOR = 0b00000001
    #2、管理帖子权限
    POSTER = 0b00000010
    #3、管理评论的权限
    COMMENTER = 0b00000100
    #4、管理板块的权限
    BOARDER = 0b00001000
    #5、管理前台用户的权限
    FRONTUSER = 0b00010000
    #6、管理后台用户的权限
    CMSUSER = 0b00100000
    #7、管理后台管理员的权限
    ADMINER = 0b01000000


#用中间表表示用户与角色之间的关系
cms_role_user = db.Table(
    'cms_role_user',
    db.Column('cms_role_id', db.Integer, db.ForeignKey('cms_role.id'),
              primary_key=True),
    db.Column('cms_user_id', db.Integer, db.ForeignKey('cms_user.id'),
              primary_key=True),
)

#让权限与用户发生关系，就需要定义一个角色类
class CMSRole(db.Model):
    managed = True
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False) #部门
    #描述定义这个角色的时候有哪些权限的相关信息
    desc = db.Column(db.String(100), nullable=True) #描述信息
    creat_time = db.Column(db.DateTime, default=datetime.now)
    #保存权限， 默认保存为浏览者权限
    permissions = db.Column(db.Integer, default=CMSPermission.VISITOR)
    #使用中间表让role可以访问user， 引用CMSUser模型，secondary代表中间表，此处的中间表是cms_role_user
    #backref代表反向绑定，可以通过user访问role
    users = db.relationship('CMSUser', secondary = cms_role_user, backref = 'roles')

class CMSUser(db.Model):
    managed = True
    __tablename__= 'cms_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable= False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)

    #构造函数
    def __init__(self, username, password, email):
        self.username = username
        #此处的password是一个方法
        self.password = password
        self.email = email

   #property装饰器，能将类中的一个方法定义成一个属性
    @property
    def password(self):
        return self._password

    #变成设置方法,对密码加密
    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        #检查用户名输入的密码与数据库密码是否一致，返回结果
        result = check_password_hash(self.password, raw_password)
        return result

    #把permission定义为属性，可以获取到用户拥有的所有权限
    @property
    def permissions(self):
        #用户的权限是保存在用户的角色下面
        #首先判断该用户是否有这个角色
        if not self.roles:
            return 0 #0代表不拥有任何权限
        all_permissions = 0 #默认该用户所有的权限为0
        for role in self.roles:
            permissions = role.permissions #取到该角色的权限
            all_permissions |= permissions #用这个变量来保存这个角色的所有权限
        return all_permissions

    def has_permission(self, permisssion):
        #首先获取该用户的所有权限
        all_permission = self.permissions
        #将all_permission与permission进行与操作，判断其结果是否与permission相一致
        #如果与操作的结果为True，则该用户确定有此权限
        result = all_permission & permisssion == permisssion
        return result
        # return self.permissions & permisssion == permisssion

    #将是否为开发者定义为一个属性
    @property
    def is_developer(self):
        # 开发者拥有所有的权限，此处将self.permissions和All_PERMISSION进行与操作
        return self.has_permission(CMSPermission.All_PERMISSION)









# user = CMSUser
# print(user.password)   #此时相当于直接访问该属性
# user.password = 'abc'



#密码对外的字段名叫password
#密码对内的字段名叫_password，带下划线该属性为受保护对象
