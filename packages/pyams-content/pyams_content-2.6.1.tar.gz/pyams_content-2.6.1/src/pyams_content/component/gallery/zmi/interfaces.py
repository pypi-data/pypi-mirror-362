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

"""PyAMS_content.component.gallery.zmi.interfaces module

This module defines interfaces which are used by gallery management interface.
"""

__docformat__ = 'restructuredtext'

from zope.interface import Interface
from zope.schema import TextLine

from pyams_file.schema import FileField

from pyams_content import _


class IGalleryMediasView(Interface):
    """Gallery medias view marker interface"""


class IGalleryMediasAddFields(Interface):
    """Gallery medias add fields interface"""

    medias_data = FileField(title=_("Images or videos data"),
                            description=_("You can upload a single file, or choose to upload "
                                          "a whole ZIP archive"),
                            required=True)

    author = TextLine(title=_("Author"),
                      description=_("Name of document's author"),
                      required=False)


class IGalleryMediaThumbnailView(Interface):
    """Gallery media thumbnail view marker interface"""
