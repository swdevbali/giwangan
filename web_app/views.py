from flask import url_for, request
from flask_admin import BaseView, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from markupsafe import Markup
from werkzeug.utils import redirect
from wtforms import TextAreaField
from wtforms.widgets import TextArea
from flask_admin import form

# https://stackoverflow.com/questions/34971368/getting-ckeditor-to-work-with-flask-admin
import settings


class CKEditorWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += " ckeditor"
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKEditorWidget, self).__call__(field, **kwargs)


class CKEditorField(TextAreaField):
    widget = CKEditorWidget()


class SecuredHomeView(AdminIndexView):

    def __init__(self):
        super(SecuredHomeView, self).__init__(template='admin/index.html', url='/admin')

    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect('/')
        return redirect(url_for('security.login', next=request.full_path))


class AdminOnlyModelView(ModelView):
    for_admin_only = True

    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect('/')
        return redirect(url_for('security.login', next=request.full_path))


class PageModelView(AdminOnlyModelView):
    column_list= ('title', 'tag', 'keyword')
    form_overrides = dict(content=CKEditorField)
    create_template = 'admin/ckeditor.html'
    edit_template = 'admin/ckeditor.html'


class MenuModelView(AdminOnlyModelView):
    form_columns = ('title', 'order')


class UserModelView(AdminOnlyModelView):
    column_list = ('email', 'active', 'roles')
    form_columns = ('email', 'active', 'roles')


class RoleModelView(AdminOnlyModelView):
    pass


class SiteConfigurationView(AdminOnlyModelView):
    pass


class ImageView(AdminOnlyModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''
        url = '/static/upload/' + form.thumbgen_filename(model.path)
        return Markup('<a href="{}" target="_blank"><img src="{}"></a>'.format(url, url))

    column_formatters = {
        'path': _list_thumbnail
    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'path': form.ImageUploadField('Image',
                                      base_path=settings.FILE_PATH,
                                      thumbnail_size=(100, 100, True))
    }