# coding=utf-8
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, \
    SubmitField, SelectField, RadioField
from wtforms.validators import Length
from ..utils.validators import MyDataRequired
from app import DepartmentList
from app.models import User


class LoginForm(Form):
    username = StringField(u'用户名', validators=[MyDataRequired(), Length(2, 64, message=u'用户名长度在6到64之间')])
    password = PasswordField(u'密码', validators=[MyDataRequired()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')


class UserForm(Form):
    username = StringField(u'用户名', validators=[MyDataRequired(), Length(2, 64, message=u'用户名长度在6到64之间')])
    password = PasswordField(u'密码', validators=[MyDataRequired()])
    department = StringField(u'部门', validators=[MyDataRequired()])
    permission = RadioField(u'权限', choices=[(permission, permission) for permission in User.PermissionList],
                            default=User.Permission.NORMAL)


class AddContestSeriesForm(Form):
    name = StringField(u'竞赛系列名', validators=[MyDataRequired()])


class AddTeacherForm(Form):
    name = StringField(u'教师姓名', validators=[MyDataRequired()])
    department = SelectField(u'学院', validators=[MyDataRequired()],
                             choices=[(department, department) for department in DepartmentList])