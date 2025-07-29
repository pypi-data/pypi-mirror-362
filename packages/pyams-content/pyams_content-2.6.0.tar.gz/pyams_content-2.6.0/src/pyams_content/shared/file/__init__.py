#
# Copyright (c) 2015-2023 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_*** module

"""

import mimetypes

from zope.schema.fieldproperty import FieldProperty

from pyams_content.shared.common import ISharedContent, IWfSharedContent, SharedContent, WfSharedContent
from pyams_content.shared.file.interfaces import FILE_CONTENT_NAME, FILE_CONTENT_TYPE, IFile, IFileManager, IWfFile
from pyams_file.property import I18nFileProperty
from pyams_i18n.interfaces import II18n, II18nManager, INegotiator
from pyams_utils.factory import factory_config
from pyams_utils.registry import get_utility
from pyams_utils.unicode import translate_string

__docformat__ = 'restructuredtext'


@factory_config(IWfFile)
@factory_config(IWfSharedContent, name=FILE_CONTENT_TYPE)
class WfFile(WfSharedContent):
    """File persistent class"""
    
    content_type = FILE_CONTENT_TYPE
    content_name = FILE_CONTENT_NAME
    content_intf = IWfFile
    content_view = False
    
    handle_content_url = True
    handle_header = False
    handle_description = False
    
    data = I18nFileProperty(IWfFile['data'])
    _filename = FieldProperty(IWfFile['filename'])

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value
        if self.data:
            manager = get_utility(IFileManager)
            for lang in II18nManager(manager).get_languages():
                data = II18n(self).query_attribute('data', lang=lang)
                if data:
                    filename = value.get(lang)
                    if filename:
                        data.filename = translate_string(filename,
                                                         escape_slashes=True,
                                                         force_lower=False)
                    elif not data.filename:
                        title = II18n(self).query_attribute('title')
                        extension = mimetypes.guess_extension(self.data.content_type)
                        data.filename = '{}{}'.format(translate_string(title, spaces='-', force_lower=True),
                                                      extension or '.bin')


@factory_config(IFile)
@factory_config(ISharedContent, name=FILE_CONTENT_TYPE)
class File(SharedContent):
    """Workflow managed file persistent class"""
    
    content_type = FILE_CONTENT_TYPE
    content_name = FILE_CONTENT_NAME
    content_view = False
