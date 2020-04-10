from flask import Blueprint
#创建蓝图对象，三个参数：蓝图名称、__name__、url前缀
bp = Blueprint('common', __name__, url_prefix='/common')
@bp.route('/')
def index():
    return 'common index'