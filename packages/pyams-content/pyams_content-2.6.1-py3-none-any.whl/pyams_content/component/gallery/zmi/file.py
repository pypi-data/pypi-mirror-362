#
# Copyright (c) 2015-2022 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.component.gallery.zmi.file module

Gallery files management components.
"""

from pyramid.interfaces import IView
from zope.component import queryMultiAdapter
from zope.interface import Interface
from zope.lifecycleevent import ObjectCreatedEvent
from zope.schema._bootstrapinterfaces import WrongType

from pyams_content.component.gallery.interfaces import IGalleryContainer, IGalleryFile
from pyams_content.component.gallery.zmi import get_json_gallery_refresh_callback
from pyams_content.component.gallery.zmi.helpers import get_json_gallery_media_refresh_callback
from pyams_content.component.gallery.zmi.interfaces import IGalleryMediaThumbnailView, IGalleryMediasAddFields, \
    IGalleryMediasView
from pyams_content.component.paragraph.zmi import get_json_paragraph_toolbar_refresh_event
from pyams_file.file import get_magic_content_type
from pyams_file.interfaces.archive import IArchiveExtractor
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer, IGroup
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_security.permission import get_edit_permission
from pyams_security.security import ProtectedViewObjectMixin
from pyams_skin.interfaces.view import IModalPage
from pyams_skin.interfaces.viewlet import IContextActionsViewletManager
from pyams_skin.viewlet.actions import ContextAction, ContextAddAction
from pyams_template.template import template_config
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config, query_adapter
from pyams_utils.factory import create_object, factory_config
from pyams_utils.registry import query_utility
from pyams_utils.traversing import get_parent
from pyams_utils.url import absolute_url
from pyams_viewlet.viewlet import ViewContentProvider, contentprovider_config, viewlet_config
from pyams_zmi.form import AdminModalAddForm, AdminModalEditForm, FormGroupSwitcher
from pyams_zmi.interfaces import IAdminLayer, IObjectLabel
from pyams_zmi.interfaces.form import IFormTitle
from pyams_zmi.interfaces.viewlet import IToolbarViewletManager
from pyams_zmi.utils import get_object_label

__docformat__ = 'restructuredtext'

from pyams_content import _


@viewlet_config(name='add-media.menu',
                context=IGalleryContainer, layer=IAdminLayer,
                view=IGalleryMediasView,
                manager=IToolbarViewletManager, weight=10)
class GalleryMediaAddAction(ProtectedViewObjectMixin, ContextAddAction):
    """Gallery media add action"""

    label = _("Add media(s)")
    href = 'add-media.html'


@ajax_form_config(name='add-media.html',
                  context=IGalleryContainer, layer=IPyAMSLayer)
class GalleryMediaAddForm(AdminModalAddForm):
    """Gallery media add form"""

    subtitle = _("New medias")
    legend = _("New medias properties")

    fields = Fields(IGalleryMediasAddFields)
    content_factory = IGalleryFile

    def create_and_add(self, data):
        data = data.get(self, {})
        medias = []
        medias_data = data.pop('medias_data')
        filename = None
        if isinstance(medias_data, (list, tuple)):
            filename, medias_data = medias_data
        is_file = hasattr(medias_data, 'seek')
        if is_file:
            medias_data.seek(0)
        content_type = get_magic_content_type(medias_data)
        if isinstance(content_type, bytes):
            content_type = content_type.decode()
        if is_file:
            medias_data.seek(0)
        extractor = query_utility(IArchiveExtractor, name=content_type)
        if extractor is not None:
            contents = extractor.get_contents(medias_data)
        else:
            contents = ((medias_data, filename),)
        for content, filename in contents:
            try:
                media = self.create(data)
                self.add(media)
                media.data = filename, content
            except WrongType:
                continue
            else:
                medias.append(media)
        return medias

    def create(self, data):
        """Create new media from content factory"""
        media = create_object(self.content_factory)
        if media is not None:
            self.request.registry.notify(ObjectCreatedEvent(media))
            media.author = data.get('author')
        return media

    def add(self, obj):
        """Add new media to gallery"""
        self.context.append(obj)


@adapter_config(required=(IGalleryContainer, IAdminLayer, GalleryMediaAddForm),
                provides=IAJAXFormRenderer)
class GalleryMediaAddFormRenderer(ContextRequestViewAdapter):
    """Gallery media add form renderer"""

    def render(self, changes):
        """JSON result renderer"""
        if not changes:
            return None
        media = changes[0]
        result = {
            'status': 'success',
            'callbacks': [
                get_json_gallery_refresh_callback(media, self.request, self.view)
            ]
        }
        event = get_json_paragraph_toolbar_refresh_event(media, self.request)
        if event is not None:
            result.setdefault('callbacks', []).append(event)
        return result


@contentprovider_config(name='gallery-media-thumbnail',
                        context=IGalleryFile, layer=IAdminLayer,
                        view=IGalleryMediasView)
@template_config(template='templates/gallery-thumbnail.pt', layer=IAdminLayer)
@factory_config(IGalleryMediaThumbnailView)
class GalleryMediaPreview(ViewContentProvider):
    """Gallery media preview"""

    def get_thumbnail_target(self):
        """Gallery media thumbnail target getter"""
        value = self.context.data
        if value is not None:
            view = queryMultiAdapter((value, self.request), IView, name='preview.html')
            if view is not None:
                return absolute_url(value, self.request, 'preview.html')
        return None


@viewlet_config(name='show-hide-media.action',
                context=IGalleryFile, layer=IAdminLayer, view=Interface,
                manager=IContextActionsViewletManager, weight=10,
                permission=VIEW_SYSTEM_PERMISSION)
class GalleryFileShowHideAction(ContextAction):
    """Gallery file show/hide action"""

    can_edit = False

    def __init__(self, context, request, view, manager):
        super().__init__(context, request, view, manager)
        gallery = get_parent(context, IGalleryContainer)
        if gallery is not None:
            edit_permission = get_edit_permission(request, context=gallery, view=view)
            self.can_edit = request.has_permission(edit_permission, context=context)

    @property
    def hint(self):
        """Hint getter"""
        if self.can_edit:
            return _("Show/hide media")
        return None

    css_class = 'btn-sm px-1'

    @property
    def icon_class(self):
        """Icon class getter"""
        if IGalleryFile(self.context).visible:
            icon_class = 'far fa-fw fa-eye'
        else:
            icon_class = 'far fa-fw fa-eye-slash text-danger'
        if self.can_edit:
            icon_class += ''
        return icon_class

    def get_href(self):
        """Icon URL getter"""
        return None

    @property
    def click_handler(self):
        """Action click handler getter"""
        if self.can_edit:
            return 'MyAMS.content.galleries.switchVisibleMedia'
        return None


#
# Gallery file properties
#

@adapter_config(required=(IGalleryFile, IPyAMSLayer, Interface),
                provides=IObjectLabel)
def gallery_file_label(context, request, view):
    """Gallery file label getter"""
    title = II18n(context).query_attribute('title', request=request)
    if not title:
        title = get_object_label(context.data, request, view)
    return title


@adapter_config(required=(IGalleryFile, IAdminLayer, IModalPage),
                provides=IFormTitle)
def gallery_file_modal_view_title(context, request, view):
    """Gallery file modal view title getter"""
    parent = get_parent(context, IGalleryContainer)
    return query_adapter(IFormTitle, request, parent, view)


@viewlet_config(name='show-properties.action',
                context=IGalleryFile, layer=IAdminLayer, view=Interface,
                manager=IContextActionsViewletManager, weight=20,
                permission=VIEW_SYSTEM_PERMISSION)
class GalleryFilePropertiesAction(ContextAction):
    """Gallery file properties action"""

    hint = _("Media properties")
    css_class = 'btn-sm px-1'
    icon_class = 'far fa-edit'

    href = 'properties.html'
    modal_target = True


@ajax_form_config(name='properties.html',
                  context=IGalleryFile, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class GalleryFilePropertiesEditForm(AdminModalEditForm):
    """Gallery file properties edit form"""

    @property
    def subtitle(self):
        translate = self.request.localizer.translate
        return translate(_("Media: {}")).format(
            get_object_label(self.context, self.request, self))

    legend = _("Gallery media properties")
    modal_class = 'modal-xl'

    fields = Fields(IGalleryFile).select('data', 'title', 'alt_title', 'description', 'author')

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        data = self.widgets.get('data')
        if data is not None:
            data.required = False


@adapter_config(name='gallery-media-sound',
                required=(IGalleryFile, IAdminLayer, GalleryFilePropertiesEditForm),
                provides=IGroup)
class GalleryFilePropertiesEditFormSoundGroup(FormGroupSwitcher):
    """Gallery file properties edit form sound group"""

    legend = _("Audio content")

    fields = Fields(IGalleryFile).select('sound', 'sound_title', 'sound_description')


@adapter_config(required=(IGalleryFile, IAdminLayer, GalleryFilePropertiesEditForm),
                provides=IAJAXFormRenderer)
class GalleryFilePropertiesEditFormRenderer(ContextRequestViewAdapter):
    """Gallery file properties edit form renderer"""

    def render(self, changes):
        if not changes:
            return None
        return {
            'status': 'success',
            'message': self.request.localizer.translate(self.view.success_message),
            'callbacks': [
                get_json_gallery_media_refresh_callback(self.context, self.request, self.view)
            ]
        }


#
# Gallery file remover
#

@viewlet_config(name='delete-media.action',
                context=IGalleryFile, layer=IAdminLayer, view=Interface,
                manager=IContextActionsViewletManager, weight=99,
                permission=VIEW_SYSTEM_PERMISSION)
class GalleryFileDeleteAction(ContextAction):
    """Gallery file delete action"""

    def __new__(cls, context, request, view, manager):
        gallery = get_parent(context, IGalleryContainer)
        if gallery is not None:
            edit_permission = get_edit_permission(request, context=gallery, view=view)
            if not request.has_permission(edit_permission, context=context):
                return None
        return ContextAction.__new__(cls)

    hint = _("Delete media")
    css_class = 'btn-sm px-1'
    icon_class = 'fas fa-trash'

    def get_href(self):
        """Icon URL getter"""
        return None

    click_handler = 'MyAMS.content.galleries.removeMedia'
