from flask.ext.uploads import UploadSet, DEFAULTS, ARCHIVES, UploadNotAllowed

resource_uploader = UploadSet('resource', DEFAULTS + ARCHIVES,
                              default_dest=lambda app: app.instance_root)


def save_file(file_data, file_attr, awards):
    pass