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

"""PyAMS_content.component.extfile module

This module provides components which are used to handle external files.
"""

import os

from pyramid.events import subscriber
from zope.interface import alsoProvides, implementer
from zope.lifecycleevent import IObjectAddedEvent, IObjectModifiedEvent, IObjectRemovedEvent, \
    ObjectModifiedEvent
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.association import AssociationItem
from pyams_content.component.association.interfaces import IAssociationInfo
from pyams_content.component.extfile.interfaces import EXTAUDIO_ICON_CLASS, EXTAUDIO_ICON_HINT, \
    EXTFILE_ICON_CLASS, EXTFILE_ICON_HINT, EXTIMAGE_ICON_CLASS, EXTIMAGE_ICON_HINT, \
    EXTVIDEO_ICON_CLASS, EXTVIDEO_ICON_HINT, IBaseExtFile, IExtAudio, IExtFile, \
    IExtFileManagerInfo, IExtImage, IExtVideo
from pyams_content.shared.common import IWfSharedContent
from pyams_file.file import EXTENSIONS_THUMBNAILS
from pyams_file.interfaces import IFileInfo, IImageFile, IResponsiveImage
from pyams_file.property import I18nFileProperty
from pyams_i18n.interfaces import II18n, INegotiator
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.factory import factory_config
from pyams_utils.interfaces import MISSING_INFO
from pyams_utils.registry import get_pyramid_registry, query_utility
from pyams_utils.request import check_request
from pyams_utils.size import get_human_size
from pyams_utils.traversing import get_parent


__docformat__ = 'restructuredtext'

from pyams_content import _


@implementer(IBaseExtFile)
class BaseExtFile(AssociationItem):
    """External file persistent class"""

    title = FieldProperty(IBaseExtFile['title'])
    description = FieldProperty(IBaseExtFile['description'])
    author = FieldProperty(IBaseExtFile['author'])
    language = FieldProperty(IBaseExtFile['language'])
    filename = FieldProperty(IBaseExtFile['filename'])


@adapter_config(required=IBaseExtFile,
                provides=IAssociationInfo)
class BaseExtFileAssociationInfoAdapter(ContextAdapter):
    """Base external file association info adapter"""

    @property
    def pictogram(self):
        """Pictogram getter"""
        return self.context.icon_class

    @property
    def user_title(self):
        """User title getter"""
        request = check_request()
        manager_info = IExtFileManagerInfo(request.root)
        title = II18n(self.context).query_attribute('title', request=request)
        if not title:
            title = self.context.filename
            if '.' in title:
                title, _extension = title.rsplit('.', 1)
        prefix = II18n(manager_info).query_attribute('default_title_prefix',
                                                     request=request) or ''
        return f'{prefix} {title}'

    @property
    def user_header(self):
        """User header getter"""
        request = check_request()
        return II18n(self.context).query_attribute('description', request=request)

    @property
    def user_icon(self):
        """User icon getter"""
        filename = self.context.filename
        if filename:
            _name, ext = os.path.splitext(filename)
            return f'''<img class="mx-3 align-top"''' \
                   f''' src="/--static--/pyams_file_views/img/16x16/''' \
                   f'''{EXTENSIONS_THUMBNAILS.get(ext, 'unknown.png')}" />'''

    @property
    def inner_title(self):
        """Inner title getter"""
        return self.context.filename or MISSING_INFO

    @property
    def human_size(self):
        """Human size getter"""
        data = II18n(self.context).query_attribute('data')
        if data:
            return get_human_size(data.get_size())
        return MISSING_INFO


def update_properties(extfile):
    """Update missing file properties"""
    request = check_request()
    i18n = query_utility(INegotiator)
    if i18n is not None:
        lang = i18n.server_language
        data = II18n(extfile).get_attribute('data', lang, request)
        if data:
            info = IFileInfo(data)
            info.title = II18n(extfile).get_attribute('title', lang, request)
            info.description = II18n(extfile).get_attribute('description', lang, request)
            if not extfile.filename:
                extfile.filename = info.filename
            else:
                info.filename = extfile.filename
            info.language = extfile.language


@subscriber(IObjectAddedEvent, context_selector=IBaseExtFile)
def handle_added_extfile(event):
    """Handle added external file"""
    # update inner file properties
    extfile = event.object
    update_properties(extfile)
    # notify content modification
    content = get_parent(extfile, IWfSharedContent)
    if content is not None:
        get_pyramid_registry().notify(ObjectModifiedEvent(content))


@subscriber(IObjectModifiedEvent, context_selector=IBaseExtFile)
def handle_modified_extfile(event):
    """Handle modified external file"""
    # update inner file properties
    extfile = event.object
    update_properties(extfile)
    # notify content modification
    content = get_parent(extfile, IWfSharedContent)
    if content is not None:
        get_pyramid_registry().notify(ObjectModifiedEvent(content))


@subscriber(IObjectRemovedEvent, context_selector=IBaseExtFile)
def handle_removed_extfile(event):
    """Handle removed external file"""
    content = get_parent(event.object, IWfSharedContent)
    if content is not None:
        get_pyramid_registry().notify(ObjectModifiedEvent(content))


@factory_config(IExtFile)
class ExtFile(BaseExtFile):
    """Generic external file persistent class"""

    icon_class = EXTFILE_ICON_CLASS
    icon_hint = EXTFILE_ICON_HINT

    data = I18nFileProperty(IExtFile['data'])


@factory_config(IExtImage)
class ExtImage(BaseExtFile):
    """External image persistent class"""

    icon_class = EXTIMAGE_ICON_CLASS
    icon_hint = EXTIMAGE_ICON_HINT

    _data = I18nFileProperty(IExtImage['data'])

    @property
    def data(self):
        """Data getter"""
        return self._data

    @data.setter
    def data(self, value):
        """Data setter"""
        self._data = value
        for data in self._data.values():
            if IImageFile.providedBy(data):
                alsoProvides(data, IResponsiveImage)

    @data.deleter
    def data(self):
        """Data deleter"""
        del self._data


@factory_config(IExtVideo)
class ExtVideo(BaseExtFile):
    """External video file persistent class"""

    icon_class = EXTVIDEO_ICON_CLASS
    icon_hint = EXTVIDEO_ICON_HINT

    data = I18nFileProperty(IExtVideo['data'])


@factory_config(IExtAudio)
class ExtAudio(BaseExtFile):
    """External audio file persistent class"""

    icon_class = EXTAUDIO_ICON_CLASS
    icon_hint = EXTAUDIO_ICON_HINT

    data = I18nFileProperty(IExtAudio['data'])
