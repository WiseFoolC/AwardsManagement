# coding=utf-8
from flask import render_template, redirect, url_for, flash, request, \
    current_app, jsonify
from flask.ext.login import login_required, login_user, logout_user, current_user
from . import admin
from .forms import LoginForm, AddUserForm, EditUserForm, ContestSeriesForm, \
    TeacherForm, ContestForm, AwardsForm, StudentForm
from app.models import User, ContestSeries, Teacher, Contest, Awards, Student, \
    Resource


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
            return redirect(url_for('admin.contest'))
    return render_template('login.html',
                           login_form = login_form)


@admin.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash(u'你已下线本系统')
    return redirect(url_for('admin.login'))


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
    user_id = request.form.get('user_id', type=int)
    if current_user.id == user_id:
        ret = u'不能删除本人账号'
    else:
        ret = User.delete_by_id(user_id)
    return jsonify(ret = ret)


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
    series_id = request.form.get('series_id', -1, type=int)
    if series_id != -1:
        series = ContestSeries.get_by_id(series_id)
        ret = ContestSeries.delete_series(series)
    else:
        ret = u'删除失败'
    return jsonify(ret = ret)


@admin.route('/series/add', methods=['GET', 'POST'])
@login_required
def series_add():
    series_form = ContestSeriesForm()
    if request.method == 'POST' and series_form.validate():
        ret = ContestSeries.create_series(series_form)
        if ret == 'OK':
            return redirect(url_for('admin.series'))
        elif ret == 'FAIL':
            flash(u'提交失败')
        else:
            flash(ret)
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
        elif ret == 'FAIL':
            flash(u'提交失败')
        else:
            flash(ret)
    return render_template('admin/series_form.html',
                           title = u'竞赛系列修改',
                           action = url_for('admin.series_edit', id=id),
                           series_form = series_form)


@admin.route('/student', methods=['GET', 'POST'])
@login_required
def student():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ADMIN_STUDENT_PER_PAGE']
    if page == -1:
        page = ((Student.get_count() - 1) // per_page) + 1
    pagination = Student.get_list_pageable(page, per_page)
    student_list = pagination.items
    return render_template('admin/student.html',
                           title = u'学生管理',
                           student_list = student_list,
                           pagination = pagination)


@admin.route('/student/del', methods=['POST'])
@login_required
def student_del():
    student_id = request.form.get('student_id', -1, type=int)
    if student_id != -1:
        student = Student.get_by_id(student_id)
        ret = Student.delete_student(student)
    else:
        ret = u'删除失败'
    return jsonify(ret = ret)


@admin.route('/student/add', methods=['GET', 'POST'])
@login_required
def student_add():
    student_form = StudentForm()
    if request.method == 'POST' and student_form.validate():
        ret = Student.create_student(student_form)
        if ret == 'OK':
            return redirect(url_for('admin.student'))
        elif ret == 'FAIL':
            flash(u'提交失败')
        else:
            flash(ret)
    return render_template('admin/student_form.html',
                           title = u'添加学生',
                           action = url_for('admin.student_add'),
                           student_form = student_form)


@admin.route('/student/edit/<id>', methods=['GET', 'POST'])
@login_required
def student_edit(id):
    student = Student.get_by_id(id)
    student_form = StudentForm()
    if request.method == 'GET':
        student_form.stu_no.data = student.stu_no
        student_form.name.data = student.name
        student_form.department.data = student.department
        student_form.major.data = student.major
        student_form.grade.data = student.grade
    if request.method == 'POST' and student_form.validate():
        ret = Student.update_student(student, student_form)
        if ret == 'OK':
            return redirect(url_for('admin.student'))
        elif ret == 'FAIL':
            flash(u'提交失败')
        else:
            flash(ret)
    return render_template('admin/student_form.html',
                           title = u'修改学生',
                           action = url_for('admin.student_edit', id=id),
                           student_form = student_form)


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


@admin.route('/teacher/del', methods=['POST'])
@login_required
def teacher_del():
    teacher_id = request.form.get('teacher_id', -1, type=int)
    if teacher_id != -1:
        teacher = Teacher.get_by_id(teacher_id)
        ret = Teacher.delete_teacher(teacher)
    else:
        ret = u'删除失败'
    return jsonify(ret = ret)


@admin.route('/teacher/add', methods=['GET', 'POST'])
@login_required
def teacher_add():
    teacher_form = TeacherForm()
    if request.method == 'POST' and teacher_form.validate():
        ret = Teacher.create_teacher(teacher_form)
        if ret == 'OK':
            return redirect(url_for('admin.teacher'))
        elif ret == 'FAIL':
            flash(u'提交失败')
        else:
            flash(ret)
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
        elif ret == 'FAIL':
            flash(u'提交失败')
        else:
            flash(ret)
    return render_template('admin/teacher_form.html',
                           title = u'修改教师',
                           action = url_for('admin.teacher_edit', id=id),
                           teacher_form = teacher_form)


@admin.route('/contest', methods=['GET', 'POST'])
@login_required
def contest():
    page = request.args.get('page', 1, type=int)
    filter_pass = request.args.get('filter_pass', 0, type=int)
    per_page = current_app.config['ADMIN_CONTEST_PER_PAGE']
    department = current_user.department if current_user.department != u'教务处' else None
    if page == -1:
        page = ((Contest.get_count(filter_pass, department) - 1) // per_page) + 1
    pagination = Contest.get_list_pageable(page, per_page, filter_pass,
                                           department)
    contest_list = pagination.items
    return render_template('admin/contest.html',
                           title = u'竞赛管理',
                           contest_list = contest_list,
                           pagination = pagination,
                           filter_pass = filter_pass)


@admin.route('/contest/del', methods=['POST'])
@login_required
def contest_del():
    contest_id = request.form.get('contest_id', -1, type=int)
    if contest_id != -1:
        contest = Contest.get_by_id(contest_id)
        ret = Contest.delete_contest(contest)
    else:
        ret = u'删除失败'
    return jsonify(ret = ret)


@admin.route('/contest/add', methods=['GET', 'POST'])
@login_required
def contest_add():
    contest_form = ContestForm()
    contest_form.department.data = current_user.department
    if request.method == 'POST' and contest_form.validate():
        ret = Contest.create_contest(contest_form, request)
        if ret == 'OK':
            return redirect(url_for('admin.contest'))
        elif ret == 'FAIL':
            flash(u'提交失败')
        else:
            flash(ret)
    current_app.logger.error(contest_form.errors)
    return render_template('admin/contest_form.html',
                           title = u'添加竞赛',
                           action = url_for('admin.contest_add'),
                           contest_form = contest_form)


@admin.route('/contest/edit/<id>', methods=['GET', 'POST'])
@login_required
def contest_edit(id):
    contest = Contest.get_by_id(id)
    contest_form = ContestForm()
    contest_form.department.data = current_user.department
    if request.method == 'GET':
        contest_form.name_cn.data = contest.name_cn
        contest_form.name_en.data = contest.name_en
        contest_form.level.data = contest.level
        contest_form.type.data = contest.type
        contest_form.department.data = contest.department
        contest.site = contest_form.site.data
        contest_form.organizer.data = contest.organizer
        contest_form.co_organizer.data = contest.co_organizer
        if contest.series:
            contest_form.series_id.data = contest.series.id
        contest_form.year.data = contest.year
        contest_form.date_range.data = [contest.start_date.strftime('%Y/%m/%d'),
                                        contest.end_date.strftime('%Y/%m/%d')]

    if request.method == 'POST' and contest_form.validate():
        ret = Contest.update_contest(contest, contest_form, request)
        if ret == 'OK':
            return redirect(url_for('admin.contest'))
        elif ret == 'FAIL':
            flash(u'提交失败')
        else:
            flash(ret)
        print ret
    current_app.logger.error(contest_form.errors)
    return render_template('admin/contest_form.html',
                           title = u'修改竞赛',
                           action = url_for('admin.contest_edit', id=id),
                           contest_form = contest_form)


@admin.route('/contest/<id>', methods=['GET'])
@login_required
def awards(id):
    contest = Contest.get_by_id(id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ADMIN_AWARDS_PER_PAGE']
    if page == -1:
        page = ((Awards.get_count(contest_id=contest.contest_id) - 1) // per_page) + 1
    pagination = Awards.get_list_pageable(page, per_page,
                                          contest_id=contest.contest_id)
    awards_list = pagination.items
    return render_template('admin/awards.html',
                           title = u'奖项管理',
                           contest = contest,
                           awards_list = awards_list,
                           pagination = pagination,
                           process = Awards.AwardsProcess)


@admin.route('/awards/del', methods=['POST'])
@login_required
def awards_del():
    awards_id = request.form.get('awards_id', -1)
    if awards_id != -1:
        awards = Awards.get_by_id(awards_id)
        ret = Awards.delete_awards(awards)
    else:
        ret = u'删除失败'
    return jsonify(ret = ret)


@admin.route('/contest/<id>/awards/add', methods=['GET', 'POST'])
@login_required
def awards_add(id):
    contest = Contest.get_by_id(id)
    awards_form = AwardsForm()
    if request.method == 'POST' and awards_form.validate():
        ret = Awards.create_awards(awards_form, contest, request.files)
        if ret == 'OK':
            return redirect(url_for('admin.awards', id=contest.id))
        elif ret == 'FAIL':
            flash(u'提交失败')
        else:
            flash(ret)
    return render_template('admin/awards_form.html',
                           title = u'奖项录入',
                           contest = contest,
                           awards_form = awards_form)


@admin.route('/contest/<id>/awards/edit/<awards_id>', methods=['GET', 'POST'])
@login_required
def awards_edit(id, awards_id):
    contest = Contest.get_by_id(id)
    awards = Awards.get_by_id(awards_id)
    exist_resources = awards.resources
    awards_form = AwardsForm()
    if request.method == 'GET':
        awards_form.honor.data = awards.honor
        awards_form.level.data = awards.level
        awards_form.title.data = awards.title
        awards_form.type.data = awards.type
        if awards.teachers:
            teacher = awards.teachers[0]
            awards_form.teachers.data = teacher.name
        awards_form.students.data = [s.stu_no for s in awards.students]
    if request.method == 'POST' and awards_form.validate():
        ret = Awards.update_awards(awards, awards_form, request.files)
        if ret == 'OK':
            return redirect(url_for('admin.awards', id=contest.id))
        elif ret == 'FAIL':
            flash(u'提交失败')
        else:
            flash(ret)
    return render_template('admin/awards_form.html',
                           title = u'奖项修改',
                           contest = contest,
                           awards_form = awards_form,
                           exist_resources = exist_resources)


@admin.route('/resource/del', methods=['POST'])
@login_required
def resource_del():
    res_id = request.form.get('res_id', -1)
    if res_id != -1:
        res = Resource.get_by_id(res_id)
        ret = Resource.delete_res(res)
    else:
        ret = u'删除失败'
    return jsonify(ret = ret)


@admin.route('/teachers.json', methods=['GET'])
@login_required
def teachers_json():
    query = request.args.get('query', None)
    teachers = Teacher.get_all(query)
    return jsonify(teachers = [t.to_json() for t in teachers])


@admin.route('/print/contest/<id>', methods=['GET'])
@login_required
def contest_print(id):
    contest = Contest.get_by_id(id)
    return render_template('print/contest.html',
                           contest = contest)