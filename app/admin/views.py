# coding=utf-8
from flask import render_template, redirect, url_for, flash, request
from flask.ext.login import login_required, login_user, logout_user
from . import admin
from .forms import LoginForm, AddContestSeriesForm, AddTeacherForm
from app.models import User


@admin.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if request.method == 'POST' and login_form.validate():
        user = User.get_by_username(login_form.username.data)
        if user is None:
            flash(u'用户不存在')
        elif not user.verify_password(login_form.password.data):
            flash(u'密码错误')
        else:
            login_user(user, remember=login_form.remember_me.data)
            return url_for('admin.index')
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
def index():
    return render_template('admin/base.html')


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

