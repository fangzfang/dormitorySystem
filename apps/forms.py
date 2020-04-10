from wtforms import Form

#获取表单返回的错误信息
class BaseForm(Form):
    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message