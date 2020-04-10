#encoding: utf-8
#和cms的模型相关的视图文件

from flask import (
    Blueprint,
    views,
    render_template,
    request,
    session,
    redirect,
    url_for,
    g,
    jsonify
)
from .forms import LoginForm, ResetpwdForm, ResetEmailForm
from .models import CMSUser, CMSPermission
from .decorators import login_required, permission_required
import config
from exts import db, mail
from flask_mail import Message
from utils import restful, dmcache
import string, random




#创建蓝图对象，三个参数：蓝图名称、__name__、url前缀
bp = Blueprint('cms', __name__, url_prefix='/cms')

#用装饰器进行登录验证
@bp.route('/')
@login_required #注意装饰器必须直接写在函数上面，不能写在路由上面
def index():
    return render_template('cms/cms_index.html')

#退出登录，从session中删除用户数据，并重定向到登录页面
@bp.route('/logout/')
def logout():
    # session.clear()
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))

#个人信息
@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')

@bp.route('/email_captcha/')
def email_captcha():
    #用查询字符串的形式
    #email_captcha/?email=xxx@qq.com
    email = request.args.get('email')


    #如果没有获取到邮箱
    if not email:
        return restful.params_error('请传递邮箱参数')

    #如果有，就给这个邮箱发送邮件
    #string.ascii_letters会返回小写的a-z以及大写的A-Z的字符串
    #因为字符串是不可以更改的，此处将字符串转化为列表形式
    source = list(string.ascii_letters)
    #两个列表，用extend可以将一个列表存入到另一个列表当中。此处把0-9存入到原来的英文字母列表中
    # source.extend(['0','1','2','3','4','5','6','7','8','9'])

    #利用map函数，其中有两个参数，第一个是func，第二个是迭代的函数的参数
    #此处map中的func采用了匿名函数Lambda的形式
    source.extend(map(lambda x:str(x), range(0, 10)))
    # 随机采样, 在source列表中随机抽取6位做为验证码,此时的captcha为列表形式random.sample(source,6),然后再转化为字符串格式
    captcha = ''.join(random.sample(source,6))

    '''
        验证码有实效性，验证码并不太重要
        可以采用memcache的方法存取
    '''
    #给指定的邮箱发送邮件
    message = Message('Python论坛邮箱验证码', recipients=[email], body= '您的验证码是: %s' % captcha)
    #在发送的时候可能会出现异常，这时用try， except进行捕获
    try :
        mail.send(message)
    except:
        #如果有异常，就返回服务器错误
        return restful.server_error()
    #如果没有异常，就返回成功信息
    #用memcache进行存储邮箱和验证码
    dmcache.set(email, captcha)
    return restful.success()

# @bp.route('/email/')
# def send_email():
#     message = Message('邮件发送', ['zflove2011@126.com'], body='测试')
#     mail.send(message)
#     return 'success'


#后台验证限制
#先登录，再验证是否有权限
@bp.route('/posts/')
@login_required
@permission_required(CMSPermission.POSTER)
def posts():
    return render_template('/cms/cms_posts.html')

@bp.route('/comments/')
@login_required
@permission_required(CMSPermission.COMMENTER)
def comments():
    return render_template('/cms/cms_comments.html')

@bp.route('/boards')
@login_required
@permission_required(CMSPermission.BOARDER)
def boards():
    return render_template('/cms/cms_boards.html')

@bp.route('/fusers/')
@login_required
@permission_required(CMSPermission.FRONTUSER)
def fusers():
    return render_template('/cms/cms_fusers.html')

@bp.route('/cusers')
@login_required
@permission_required(CMSPermission.CMSUSER)
def cusers():
    return render_template('/cms/cms_cusers.html')

@bp.route('/croles/')
@login_required
@permission_required(CMSPermission.All_PERMISSION)
def croles():
    return render_template('/cms/cms_croles.html')







class LoginView(views.MethodView):
    #调用get方式，message设置了默认值，这时不传message也是可以的
    def get(self, message = None):
        #message = message 把消息传递给模版
        return render_template('cms/cms_login.html', message = message)

    def post(self):
        #对用户提交的数据进行处理验证
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            #通过email验证是否在数据库中
            user = CMSUser.query.filter_by(email = email).first()
            #如果用户存在，并且用户密码正确
            if user and user.check_password(password):
                #保存用户id，为了进行区分，可以改为
                session[config.CMS_USER_ID] = user.id
                #如果用户提交了remember
                if remember:
                    #如果设置为True，session信息默认为31天
                    session.permanent = True
                #如果没选remember，提交后会跳转到index页面
                #重定向
                return redirect(url_for('cms.index'))
            #如果不正常
            else:
                #如果输入的邮箱或密码错误就跳转到登录页面
                # return render_template('cms/cms_login.html') #这种方式会造成代码冗余
                return self.get(message = '邮箱或密码错误')

        else:
            print(form.errors)
            #errors是字典格式,{'email': ['邮箱格式错误'], 'password': ['请输入正确格式的密码']}
            #输出任意一个元组，popitem()返回的是任意一项的元组
            message = form.errors.popitem()[1][0] #('password', ['请输入正确格式的密码'])
            print(message)
            # 如果验证错误
            return self.get(message=message)
            # return form.get_error

class ResetPwdView(views.MethodView):
    #在类视图中定义装饰器，通过类属性获取
    decorators = [login_required]
    #首先获取模板，用get请求
    def get(self):
        return render_template('cms/cms_resetpwd.html')

    #确认更改的时候，发送请求，用post
    def post(self):
        form = ResetpwdForm(request.form)
        # 如果表单验证成功
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            #从锥对象中获取用户名
            user = g.cms_user
            # 如果验证成功，将新的密码设置给原来的账户
            if user.check_password(oldpwd):
                #将密码设置为新密码
                user.password = newpwd
                #提交到数据库中
                db.session.commit()
                #返回json数据给前端
                # ('code':200, 'mesaage':修改成功 )
                return restful.success()
            else:
                return restful.params_error('旧密码错误')
        else:
            return restful.params_error(form.get_error())

class ResetEmailView(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        #获取邮箱和验证码
        #此处没有确认验证码与邮箱是否匹配，就把二者绑定在一起
        #表单验证
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            #提交信息到数据库
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())


#把登录的视图添加到url中
bp.add_url_rule('/login/', view_func = LoginView.as_view('login'))
#将修改密码的视图加入到url中
bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))
#将修改邮箱的视图加入到url中
bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))

#wiki，记录网站对应的接口
#url: http://www.zlkt.com/resetpwd/
#params: [XX]
#methods: post/ get
