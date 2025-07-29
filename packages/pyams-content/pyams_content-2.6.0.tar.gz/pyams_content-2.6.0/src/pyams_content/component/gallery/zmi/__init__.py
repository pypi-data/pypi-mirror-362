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

"""PyAMS_content.component.gallery.zmi module


"""

from cgi import FieldStorage

from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPForbidden, HTTPServerError
from pyramid.view import view_config
from zope.interface import implementer
from zope.schema.interfaces import WrongType

from pyams_content.component.gallery.interfaces import IGallery, IGalleryContainer, IGalleryFile, IGalleryTarget
from pyams_content.component.gallery.zmi.helpers import get_json_gallery_refresh_callback
from pyams_content.component.gallery.zmi.interfaces import IGalleryMediasView
from pyams_content.component.paragraph.zmi import get_json_paragraph_toolbar_refresh_event
from pyams_file.file import get_magic_content_type
from pyams_file.interfaces.archive import IArchiveExtractor
from pyams_form.interfaces.form import IInnerSubForm
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_layer.skin import apply_skin
from pyams_pagelet.pagelet import pagelet_config
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_security.permission import get_edit_permission
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_utils.factory import create_object, factory_config, get_object_factory
from pyams_utils.interfaces import ICacheKeyValue, MISSING_INFO
from pyams_utils.registry import query_utility
from pyams_utils.rest import http_error
from pyams_viewlet.viewlet import Viewlet, viewlet_config
from pyams_zmi.helper.container import delete_container_element, switch_element_attribute
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.form import IPropertiesEditForm
from pyams_zmi.interfaces.viewlet import IPropertiesMenu
from pyams_zmi.skin import AdminSkin
from pyams_zmi.view import InnerAdminView
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_content import _


class BaseGalleryMediasViewlet(Viewlet):
    """Base gallery medias viewlet"""

    @reify
    def gallery(self):
        """Gallery getter"""
        return IGalleryContainer(self.context)

    @property
    def gallery_name(self):
        """Gallery name getter"""
        return ICacheKeyValue(self.gallery)

    @property
    def edit_permission(self):
        """Edit permission getter"""
        return get_edit_permission(self.request, self.gallery, self)

    @property
    def medias(self):
        """Gallery medias getter"""
        return self.gallery.values()

    def get_title(self, media):
        """Media title getter"""
        return II18n(media).query_attribute('title', request=self.request)


@adapter_config(name='gallery-medias',
                required=(IGalleryContainer, IAdminLayer, IPropertiesEditForm),
                provides=IInnerSubForm, force_implements=False)
@template_config(template='templates/gallery-medias.pt', layer=IAdminLayer)
@factory_config(IGalleryMediasView)
class GalleryMediasViewlet(BaseGalleryMediasViewlet):
    """Gallery medias viewlet"""

    def __init__(self, context, request, view, manager=None):
        super().__init__(context, request, view, manager)


@view_config(name='upload-medias-files.json',
             context=IGalleryContainer, request_type=IPyAMSLayer,
             request_method='POST', renderer='json', xhr=True, require_csrf=False)
def upload_medias_files(request):
    """Upload medias files"""
    container = IGalleryContainer(request.context)
    permission_checker = IViewContextPermissionChecker(container, None)
    if permission_checker is None:
        return http_error(request, HTTPServerError, "Missing context permission")
    if not request.has_permission(permission_checker.edit_permission, context=container):
        return http_error(request, HTTPForbidden)
    for name in request.params.keys():
        input_file = request.params.get(name)
        if isinstance(input_file, FieldStorage):
            value = input_file.value
            content_type = get_magic_content_type(value)
            extractor = query_utility(IArchiveExtractor, name=content_type)
            if extractor is not None:
                contents = extractor.get_contents(value)
            else:
                contents = ((value, input_file.filename),)
            for content, filename in contents:
                try:
                    gallery_file = create_object(IGalleryFile)
                    container.append(gallery_file)
                    gallery_file.data = filename, content
                    gallery_file.author = MISSING_INFO
                except WrongType:
                    continue
    apply_skin(request, AdminSkin)
    result_view = create_object(IGalleryMediasView, context=container, request=request, view=None)
    result_view.update()
    result = {
        'status': 'success',
        'callbacks': [
            get_json_gallery_refresh_callback(container, request, result_view)
        ]
    }
    event = get_json_paragraph_toolbar_refresh_event(container, request)
    if event is not None:
        result.setdefault('callbacks', []).append(event)
    return result


@view_config(name='set-medias-order.json',
             context=IGalleryContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True)
def set_medias_order(request):
    """Medias ordering view"""

    order = request.params.get('order').split(';')
    request.context.updateOrder(order)
    return {
        'status': 'success',
        'closeForm': False
    }


@view_config(name='switch-media-visibility.json',
             context=IGalleryContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True)
def switch_media_visibility(request):
    """Media visibility switch view"""
    return switch_element_attribute(request)


@view_config(name='remove-media.json',
             context=IGalleryContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True)
def remove_media(request):
    """Media remover view"""
    result = delete_container_element(request, container_factory=IGalleryContainer)
    if result.get('status') == 'success':
        apply_skin(request, AdminSkin)
        gallery = request.context
        result = {
            'status': 'success',
            'callbacks': [
                get_json_gallery_refresh_callback(gallery, request, None)
            ]
        }
        event = get_json_paragraph_toolbar_refresh_event(gallery, request)
        if event is not None:
            result.setdefault('callbacks', []).append(event)
        result.setdefault('handle_json', True)
    return result


@viewlet_config(name='gallery.menu',
                context=IGalleryTarget, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=20,
                permission=VIEW_SYSTEM_PERMISSION)
class GalleryMenu(NavigationMenuItem):
    """Gallery menu"""

    label = _("Medias gallery")
    href = '#medias-gallery.html'


@pagelet_config(name='medias-gallery.html',
                context=IGalleryTarget, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
@template_config(template='templates/gallery-view.pt', layer=IAdminLayer)
@implementer(IPropertiesEditForm)
class GalleryView(InnerAdminView):
    """Gallery view"""

    title = _("Medias gallery")

    medias_view = None

    def update(self):
        super().update()
        medias_view_factory = get_object_factory(IGalleryMediasView)
        if medias_view_factory is not None:
            gallery = IGallery(self.context)
            self.medias_view = medias_view_factory(gallery, self.request, self)
            self.medias_view.update()
