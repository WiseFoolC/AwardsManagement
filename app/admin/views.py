# coding=utf-8
from flask import render_template, redirect, url_for, flash, request, \
    current_app, jsonify
from flask.ext.login import login_required, login_user, logout_user, current_user
from . import admin
from .forms import LoginForm, AddUserForm, EditUserForm, ContestSeriesForm, \
    TeacherForm, ContestForm, AwardsForm
from app.models import User, ContestSeries, Teacher, Contest, Awards


@admin.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
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
    pagination = User.get_list_pageable(page, per_page)
    user_list = pagination.items
    return render_template('admin/user.html',
                           title = u'用户管理',
                           user_list = user_list,
                           pagination = pagination)


@admin.route('/user/del', methods=['POST'])
@login_required
def user_del():
    id = request.form.get('id', type=int)
    ret = User.delete_by_id(id)
    return jsonify(ret)


@admin.route('/user/add', methods=['GET', 'POST'])
@login_required
def user_add():
    user_form = AddUserForm()
    if request.method == 'POST' and user_form.validate():
        ret = User.create_user(user_form)
        if ret == 'OK':
            return redirect(url_for('admin.user'))
    return render_template('admin/user_form.html',
                           title = u'添加用户', add = True,
                           action = url_for('admin.user_add'),
                           user_form = user_form)


@admin.route('/user/edit/<id>', methods=['GET', 'POST'])
@login_required
def user_edit(id):
    user = User.get_by_id(int(id))
    user_form = EditUserForm()
    if request.method == 'GET':
        user_form.username.data = user.username
        user_form.department.data = user.department
        user_form.permission.data = user.permission
    if request.method == 'POST' and user_form.validate():
        ret = User.update_user(user, user_form)
        if ret == 'OK':
            return redirect(url_for('admin.user'))
    return render_template('admin/user_form.html',
                           title = u'修改用户',
                           action = url_for('admin.user_edit', id = id),
                           user_form = user_form)


@admin.route('/series', methods=['GET'])
@login_required
def series():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ADMIN_SERIES_PER_PAGE']
    if page == -1:
        page = ((ContestSeries.get_count() - 1) // per_page) + 1
    pagination = ContestSeries.get_list_pageable(page, per_page)
    series_list = pagination.items
    return render_template('admin/series.html',
                           title = u'竞赛系列管理',
                           series_list = series_list,
                           pagination = pagination)


@admin.route('/series/del', methods=['POST'])
@login_required
def series_del():
    pass


@admin.route('/series/add', methods=['GET', 'POST'])
@login_required
def series_add():
    series_form = ContestSeriesForm()
    if request.method == 'POST' and series_form.validate():
        ret = ContestSeries.create_series(series_form)
        if ret == 'OK':
            return redirect(url_for('admin.series'))
    return render_template('admin/series_form.html',
                           title = u'竞赛系列录入',
                           action = url_for('admin.series_add'),
                           series_form = series_form)


@admin.route('/series/edit/<id>', methods=['GET', 'POST'])
@login_required
def series_edit(id):
    series = ContestSeries.get_by_id(id)
    series_form = ContestSeriesForm()
    if request.method == 'GET':
        series_form.name.data = series.name
    if request.method == 'POST' and series_form.validate():
        ret = ContestSeries.update_series(series, series_form)
        if ret == 'OK':
            return redirect(url_for('admin.series'))
    return render_template('admin/series_form.html',
                           title = u'竞赛系列修改',
                           action = url_for('admin.series_edit', id=id),
                           series_form = series_form)


@admin.route('/teacher', methods=['GET', 'POST'])
@login_required
def teacher():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ADMIN_TEACHER_PER_PAGE']
    if page == -1:
        page = ((Teacher.get_count() - 1) // per_page) + 1
    pagination = Teacher.get_list_pageable(page, per_page)
    teacher_list = pagination.items
    return render_template('admin/teacher.html',
                           title = u'教师管理',
                           teacher_list = teacher_list,
                           pagination = pagination)


@admin.route('/teacher/add', methods=['GET', 'POST'])
@login_required
def teacher_add():
    teacher_form = TeacherForm()
    if request.method == 'POST' and teacher_form.validate():
        ret = Teacher.create_teacher(teacher_form)
        if ret == 'OK':
            return redirect(url_for('admin.teacher'))
    return render_template('admin/teacher_form.html',
                           title = u'添加教师',
                           action = url_for('admin.teacher_add'),
                           teacher_form = teacher_form)


@admin.route('/teacher/edit/<id>', methods=['GET', 'POST'])
@login_required
def teacher_edit(id):
    teacher = Teacher.get_by_id(id)
    teacher_form = TeacherForm()
    if request.method == 'GET':
        teacher_form.name.data = teacher.name
        teacher_form.department.data = teacher.department
    if request.method == 'POST' and teacher_form.validate():
        ret = Teacher.update_teacher(teacher, teacher_form)
        if ret == 'OK':
            return redirect(url_for('admin.teacher'))
    return render_template('admin/teacher_form.html',
                           title = u'修改教师',
                           action = url_for('admin.teacher_edit', id=id),
                           teacher_form = teacher_form)


@admin.route('/contest', methods=['GET', 'POST'])
@login_required
def contest():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ADMIN_CONTEST_PER_PAGE']
    if page == -1:
        page = ((Contest.get_count() - 1) // per_page) + 1
    pagination = Contest.get_list_pageable(page, per_page)
    contest_list = pagination.items
    return render_template('admin/contest.html',
                           title = u'竞赛管理',
                           contest_list = contest_list,
                           pagination = pagination)


@admin.route('/contest/add', methods=['GET', 'POST'])
@login_required
def contest_add():
    contest_form = ContestForm()
    if request.method == 'POST' and contest_form.validate():
        ret = Contest.create_contest(contest_form)
        if ret == 'OK':
            return redirect(url_for('admin.contest'))
    return render_template('admin/contest_form.html',
                           title = u'添加竞赛',
                           action = url_for('admin.contest_add'),
                           contest_form = contest_form)


@admin.route('/contest/edit/<id>', methods=['GET', 'POST'])
@login_required
def contest_edit(id):
    contest = Contest.get_by_id(id)
    contest_form = ContestForm()
    if request.method == 'GET':
        contest_form.name_cn.data = contest.name_cn
        contest_form.name_en.data = contest.name_en
        contest_form.level.data = contest.level
        contest_form.series_id.data = contest.series.id
        contest_form.year.data = contest.year
        contest_form.date_range.data = [contest.start_date.strftime('%Y/%m/%d'),
                                        contest.end_date.strftime('%Y/%m/%d')]
        contest_form.organizer.data = contest.organizer
        contest_form.co_organizer.data = contest.co_organizer
        contest_form.place.data = contest.place
    if request.method == 'POST' and contest_form.validate():
        ret = Contest.update_contest(contest, contest_form)
        if ret == 'OK':
            return redirect(url_for('admin.contest'))
    return render_template('admin/contest_form.html',
                           title = u'修改竞赛',
                           action = url_for('admin.contest_edit', id=id),
                           contest_form = contest_form)


@admin.route('/contest/<id>/awards', methods=['GET'])
def awards(id):
    contest = Contest.get_by_id(id)
    awards_list = contest.awards.all()
    return render_template('admin/awards.html',
                           title = u'奖项管理',
                           contest = contest,
                           awards_list = awards_list)


@admin.route('/contest/<id>/awards/add', methods=['GET'])
def awards_add(id):
    contest = Contest.get_by_id(id)
    awards_form = AwardsForm()
    return render_template('admin/awards_form.html',
                           title = u'奖项录入',
                           contest = contest,
                           awards_form = awards_form)


@admin.route('/contest/<id>/awards/edit/<awards_id>', methods=['GET'])
def awards_edit(id, awards_id):
    contest = Contest.get_by_id(id)
    awards = Awards.get_by_id(awards_id)
    awards_form = AwardsForm()
    return render_template('admin/awards_form.html',
                           title = u'奖项录入',
                           contest = contest,
                           awards_form = awards_form)