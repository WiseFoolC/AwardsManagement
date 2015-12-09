# coding=utf-8
from flask import current_app
from flask.ext.uploads import UploadSet, DEFAULTS, ARCHIVES, UploadNotAllowed
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from . import db
import os


resource_uploader = UploadSet('resource', DEFAULTS + ARCHIVES,
                              default_dest=lambda app: app.instance_root)


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.Unicode(1024), nullable=False)
    upload_time = db.Column(db.DateTime)

    awards_id = db.Column(db.String(128),
                          db.ForeignKey('awards.awards_id', ondelete='CASCADE'),
                          nullable=False)

    awards = db.relationship('Awards',
                             backref=db.backref('resources',
                                                cascade="all, delete-orphan",
                                                passive_deletes=True,
                                                lazy='dynamic'))

    def __repr__(self):
        return '<Resource %s>' % self.filename

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


def generate_filename(awards):
    last_awards = awards.resource.order_by(Resource.filename.desc()).first()
    if last_awards is None:
        return '0001.'
    else:
        return str(int(last_awards.filename) + 1).rjust(4, '0') + '.'


def save_res(storage, awards):
    filename = ''
    try:
        maybe_name = generate_filename(awards)
        filename = resource_uploader.save(storage, folder=awards.awards_id,
                                          name=maybe_name)
        res = Resource()
        res.filename = filename
        res.awards_id = awards.awards_id
        res.upload_time = datetime.now()
        res.save()
        current_app.logger.info(u'创建文件 %s 成功' % filename)
        return 'OK'
    except UploadNotAllowed:
        return u"非法上传"
    except IntegrityError:
        os.remove(resource_uploader.path(filename))
        db.session.rollback()
        return u'文件名已存在'
    except Exception, e:
        current_app.logger.error(u'创建文件失败')
        current_app.logger.error(e)
        return 'FAIL'


def delete_res(res):
    try:
        os.remove(resource_uploader.path(res.filename))
        res.delete()
        current_app.logger.error(u'删除文件成功')
        return 'OK'
    except Exception, e:
        current_app.logger.error(u'删除文件失败')
        current_app.logger.error(e)
        return 'FAIL'
    pass


def get_url(res):
    return resource_uploader.path(res.filename)


def get_size(res):
    return os.path.getsize(resource_uploader.path(res.filename))