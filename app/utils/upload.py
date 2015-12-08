from flask.ext.uploads import UploadSet, DEFAULTS, ARCHIVES, UploadNotAllowed
from app.models.Resource import Resource

resource_uploader = UploadSet('resource', DEFAULTS + ARCHIVES,
                              default_dest=lambda app: app.instance_root)


def generate_name():
    pass


def save_file(storage, upload_form, awards):
    try:
        filename = resource_uploader.save(storage, folder=awards.awards_id,
                                          name='.')
        res = Resource()
        res.filename = filename
    except Exception, e:
        return 'FAIL'
    pass