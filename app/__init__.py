from flask import Flask
from flask.ext.login import LoginManager
from config import config, Constant
from app.models import db
from flask.ext.uploads import patch_request_class, configure_uploads
from app.utils.upload import resource_uploader


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'admin.login'


def load_department_config():
    from codecs import open as codecs_open
    cfg = codecs_open(Constant.DEPARTMENT_CONFIG_DEST, 'r', 'utf-8')
    department_list = [line.strip('\r\n') for line in cfg]
    cfg.close()
    return department_list


DepartmentList = load_department_config()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    login_manager.init_app(app)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from ajax import ajax as ajax_blueprint
    app.register_blueprint(ajax_blueprint, url_prefix='/ajax')

    patch_request_class(app, size=16*1024*1024) # 16MB
    configure_uploads(app, resource_uploader)

    return app
