from flask import redirect, url_for
from flask.ext.login import current_user
from . import main


@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('admin.contest'))
    return redirect(url_for('admin.login'))
