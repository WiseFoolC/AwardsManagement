import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__name__))


class Constant:
    DEPARTMENT_CONFIG_DEST = basedir + '/department.ini'


class Config:
    SSL_DISABLE = True
    CSRF_ENABLED = True
    SECRET_KEY = 'a hard guess string'
    ''' sql '''
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    ''' session, cookie '''
    PERMANENT_SESSION_LIFETIME = timedelta(days=3)
    REMEMBER_COOKIE_DURATION = timedelta(days=3)
    ''' file '''
    UPLOADED_RESOURCE_DEST = basedir + '/uploads/'
    ''' admin '''
    ADMIN_USER_PER_PAGE = 10



class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://sa:rayn2015@localhost:1433/demo?charset=utf8'


class DeployConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://dxy:Dxyrjgcxy2015@210.41.228.124:1433/ACMS?charset=utf8'


config = {
    'dev': DevConfig,
    'deploy': DeployConfig,

    'default': DevConfig
}