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

"""PyAMS_content.component.gallery.file module

"""

__docformat__ = 'restructuredtext'

from persistent import Persistent
from pyramid.events import subscriber
from zope.container.contained import Contained
from zope.interface import alsoProvides
from zope.lifecycleevent import IObjectAddedEvent, IObjectModifiedEvent, IObjectRemovedEvent, \
    ObjectModifiedEvent
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.gallery import IBaseGallery, IGalleryFile
from pyams_content.interfaces import MANAGE_SITE_ROOT_PERMISSION
from pyams_content.shared.common import IWfSharedContent
from pyams_file.interfaces import IImageFile, IResponsiveImage
from pyams_file.property import FileProperty
from pyams_i18n.interfaces import INegotiator
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.factory import factory_config
from pyams_utils.registry import get_current_registry, get_utility
from pyams_utils.traversing import get_parent
from pyams_workflow.content import HiddenContentPublicationInfo
from pyams_workflow.interfaces import IWorkflowPublicationInfo


#
# Gallery file
#

@factory_config(IGalleryFile)
class GalleryFile(Persistent, Contained):
    """Gallery file info"""

    _data = FileProperty(IGalleryFile['data'])
    _title = FieldProperty(IGalleryFile['title'])
    alt_title = FieldProperty(IGalleryFile['alt_title'])
    description = FieldProperty(IGalleryFile['description'])
    author = FieldProperty(IGalleryFile['author'])
    sound = FileProperty(IGalleryFile['sound'])
    sound_title = FieldProperty(IGalleryFile['sound_title'])
    sound_description = FieldProperty(IGalleryFile['sound_description'])
    visible = FieldProperty(IGalleryFile['visible'])

    @property
    def data(self):
        """File data getter"""
        return self._data

    @data.setter
    def data(self, value):
        """File data setter"""
        self._data = value
        if IImageFile.providedBy(self._data):
            alsoProvides(self._data, IResponsiveImage)

    @data.deleter
    def data(self):
        """File data deleter"""
        del self._data

    @property
    def title(self):
        """File title getter"""
        return self._title

    @title.setter
    def title(self, value):
        """File title setter"""
        self._title = value
        if self._data:
            negociator = get_utility(INegotiator)
            self._data.title = value.get(negociator.server_language)


@adapter_config(required=IGalleryFile,
                provides=IViewContextPermissionChecker)
class GalleryFilePermissionChecker(ContextAdapter):
    """Gallery file permission checker"""

    @property
    def edit_permission(self):
        """File edit permission getter"""
        gallery = get_parent(self.context, IBaseGallery)
        if gallery is not None:
            return IViewContextPermissionChecker(gallery).edit_permission
        return MANAGE_SITE_ROOT_PERMISSION


@subscriber(IObjectAddedEvent, context_selector=IGalleryFile)
def handle_added_gallery_file(event):
    """Handle added gallery file"""
    content = get_parent(event.object, IWfSharedContent)
    if content is not None:
        get_current_registry().notify(ObjectModifiedEvent(content))


@subscriber(IObjectModifiedEvent, context_selector=IGalleryFile)
def handle_modified_gallery_file(event):
    """Handle modified gallery file"""
    content = get_parent(event.object, IWfSharedContent)
    if content is not None:
        get_current_registry().notify(ObjectModifiedEvent(content))


@subscriber(IObjectRemovedEvent, context_selector=IGalleryFile)
def handle_removed_gallery_file(event):
    """Handle removed gallery file"""
    content = get_parent(event.object, IWfSharedContent)
    if content is not None:
        get_current_registry().notify(ObjectModifiedEvent(content))


@adapter_config(required=IGalleryFile,
                provides=IWorkflowPublicationInfo)
def gallery_file_publication_info(context):
    """Gallery file publication info"""
    if not context.visible:
        return HiddenContentPublicationInfo()
    return None
