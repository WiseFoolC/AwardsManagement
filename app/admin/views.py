# coding=utf-8
from flask import render_template, redirect, url_for, flash, request, \
    current_app
from flask.ext.login import login_required, login_user, logout_user, current_user
from . import admin
from .forms import LoginForm, UserForm, AddContestSeriesForm, AddTeacherForm
from app.models import User


@admin.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('admin.index'))
    login_form = LoginForm()
    if request.method == 'POST' and login_form.validate():
        user = User.get_by_username(login_form.username.data)
        if user is None:
            flash(u'用户不存在')
        elif not user.verify_password(login_form.password.data):
            flash(u'密码错误')
        else:
            login_user(user, remember=login_form.remember_me.data)
            return redirect(url_for('admin.index'))
    return render_template('login.html',
                           login_form = login_form)


@admin.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    #flash(u'你已下线本系统')
    return redirect(url_for('main.index'))


@admin.route('/')
@admin.route('/index')
@login_required
def index():
    return render_template('admin/base.html')


@admin.route('/user', methods=['GET'])
@login_required
def user():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ADMIN_USER_PER_PAGE']
    if page == -1:
        page = ((User.get_count() - 1) // per_page) + 1
    pagination = User.get_list_with_page(page, per_page)
    user_list = pagination.items
    return render_template('admin/user.html',
                           title = u'用户管理',
                           user_list = user_list,
                           pagination = pagination)


@admin.route('/user/del', methods=['POST'])
def user_del():
    id = request.form.get('id', type=int)
    user = User.get_by_id(id)


@admin.route('/user/add', methods=['GET', 'POST'])
@login_required
def user_add():
    user_form = UserForm()
    if request.method == 'POST' and user_form.validate():
        pass
    return render_template('admin/user_form.html',
                           title = u'添加用户',
                           edit = False,
                           action = url_for('admin.user_add'),
                           user_form = user_form)


@admin.route('/user/edit/<id>', methods=['GET', 'POST'])
@login_required
def user_edit(id):
    user = User.get_by_id(int(id))
    user_form = UserForm()
    user_form.username.data = user.username
    user_form.department.data = user.department
    user_form.permission.data = user.permission
    if request.method == 'POST' and user_form.validate():
        pass
    return render_template('admin/user_form.html',
                           title = u'修改用户',
                           edit = True,
                           action = url_for('admin.user_edit', id = id),
                           user_form = user_form)


@admin.route('/series/add', methods=['GET', 'POST'])
def series_add():
    series_add_form = AddContestSeriesForm()
    if request.method == 'POST' and series_add_form.validate():
        pass
    return render_template('admin/series_add.html',
                           series_add_form = series_add_form)


@admin.route('/teacher/add', methods=['GET', 'POST'])
def teacher_add():
    teacher_add_form = AddTeacherForm()
    if request.method == 'POST' and teacher_add_form.validate():
        pass
    return render_template('admin/teacher_add.html',
                           teacher_add_form = teacher_add_form)

