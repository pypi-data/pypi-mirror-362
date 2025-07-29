# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from pyams_content.shared.common.interfaces import ISharedContent, ISharedTool, IWfSharedContent
from pyams_file.schema import I18nFileField
from pyams_i18n.schema import I18nTextLineField

__docformat__ = 'restructuredtext'

from pyams_content import _


FILE_CONTENT_TYPE = 'file'
FILE_CONTENT_NAME = _("File")


class IWfFile(IWfSharedContent):
    """File interface"""

    data = I18nFileField(title=_("File content"),
                         description=_("Actual file content"),
                         required=True)

    filename = I18nTextLineField(title=_("File name"),
                                 description=_("Name used to save the file on download"),
                                 required=False)


class IFile(ISharedContent):
    """Workflow managed file interface"""


class IFileManager(ISharedTool):
    """Files manager interface"""
