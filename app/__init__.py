from flask import Flask
from flask.ext.login import LoginManager
from config import config, Constant
from app.models import db, load_department_config
from flask.ext.uploads import patch_request_class, configure_uploads
from app.utils.upload import resource_uploader


app = Flask(__name__)
login_manager = LoginManager()
DepartmentList = load_department_config(Constant.DEPARTMENT_CONFIG_DEST)


def create_app(config_name):
    app.config.from_object(config[config_name])
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'admin.login'

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    patch_request_class(app, size=16*1024*1024) # 16MB
    configure_uploads(app, resource_uploader)

    return app
