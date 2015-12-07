from flask import render_template, redirect, url_for, abort
from . import main


@main.route('/')
def index():
    #return render_template('main/base.html')
    return redirect(url_for('admin.login'))
