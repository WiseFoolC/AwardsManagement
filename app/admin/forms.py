# coding=utf-8
from flask.ext.wtf import Form
from wtforms import Field, StringField, PasswordField, BooleanField, \
    SubmitField, SelectField, RadioField, DateField
from wtforms.validators import Length
from ..utils.validators import MyDataRequired
from wtforms.widgets import TextInput
from app import DepartmentList
from app.models import User, Contest, ContestSeries
from datetime import date


class LoginForm(Form):
    username = StringField(u'用户名', validators=[MyDataRequired(), Length(2, 64, message=u'用户名长度在2到64之间')])
    password = PasswordField(u'密码', validators=[MyDataRequired()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')


class AddUserForm(Form):
    username = StringField(u'用户名', validators=[MyDataRequired(), Length(2, 64, message=u'用户名长度在2到64之间')])
    password = PasswordField(u'密码', validators=[MyDataRequired()])
    department = StringField(u'部门', validators=[MyDataRequired()])
    permission = RadioField(u'权限', choices=[(permission, permission) for permission in User.PermissionList],
                            default=User.Permission.NORMAL)

class EditUserForm(Form):
    username = StringField(u'用户名', validators=[MyDataRequired(), Length(2, 64, message=u'用户名长度在2到64之间')])
    department = StringField(u'部门', validators=[MyDataRequired()])
    permission = RadioField(u'权限', choices=[(permission, permission) for permission in User.PermissionList],
                            default=User.Permission.NORMAL)


class TeacherForm(Form):
    name = StringField(u'教师姓名', validators=[MyDataRequired()])
    department = SelectField(u'学院', validators=[MyDataRequired()],
                             choices=[(department, department) for department in DepartmentList])


class ContestSeriesForm(Form):
    name = StringField(u'竞赛系列名', validators=[MyDataRequired()])


class DateRangeField(Field):
    widget = TextInput()

    def _value(self):
        if self.data:
            return self.data[0] + ' - ' + self.data[1]
        else:
            return ''

    def process_formdata(self, value_list):
        if value_list:
            self.data = [d.strip() for d in value_list[0].split('-')]
        else:
            self.data = []


class ContestForm(Form):
    name_cn = StringField(u'竞赛中文名', validators=[MyDataRequired()])
    name_en = StringField(u'竞赛英文名', validators=[MyDataRequired()])
    level = SelectField(u'竞赛等级', validators=[MyDataRequired()],
                        choices=[item for item in Contest.ContestLevel.items()])
    organizer = StringField(u'主办方', validators=[MyDataRequired()])
    co_organizer = StringField(u'承办方')
    year = SelectField(u'年份', coerce=int, default=date.today().year)
    date_range = DateRangeField(u'起止日期', validators=[MyDataRequired()],
                                default=[date.today().strftime('%Y/%m/%d'), date.today().strftime('%Y/%m/%d')])
    place = StringField(u'地点', validators=[MyDataRequired()])
    series_id = SelectField(u'所属竞赛系列', coerce=int)


    def __init__(self, *args, **kwargs):
        super(ContestForm, self).__init__(*args, **kwargs)
        cur_year = date.today().year
        self.year.choices = [(year, year) for year in range(cur_year - 1, cur_year + 2)]
        series_list = ContestSeries.get_all()
        self.series_id.choices = [(series.id, series.name) for series in series_list]





