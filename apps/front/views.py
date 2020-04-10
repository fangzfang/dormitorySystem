from flask import Blueprint
#创建蓝图对象，三个参数：蓝图名称、__name__
bp = Blueprint('front', __name__)
@bp.route('/')
def index():
    return 'front index'