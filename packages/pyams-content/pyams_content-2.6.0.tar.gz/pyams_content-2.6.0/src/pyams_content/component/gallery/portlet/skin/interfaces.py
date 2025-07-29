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

"""PyAMS_content.component.gallery.portlet.skin.interfaces module

This module defines interfaces of gallery portlet renderers settings.
"""

from zope.interface import Interface

from pyams_skin.schema import BootstrapThumbnailsSelectionField

__docformat__ = 'restructuredtext'

from pyams_content import _


class IGalleryPortletDefaultRendererSettings(Interface):
    """Gallery portlet default renderer settings interface"""

    thumb_selection = BootstrapThumbnailsSelectionField(
        title=_("Thumbnails selection"),
        description=_("Selection used to display images thumbnails"),
        default_width=2,
        change_width=True,
        required=False)

    def get_css_cols(self):
        """Return CSS columns width matching current selection"""


class IGalleryPortletCarouselRendererSettings(Interface):
    """Gallery portlet carousel renderer settings interface"""

    thumb_selection = BootstrapThumbnailsSelectionField(
        title=_("Images selection"),
        description=_("Selection used to display images"),
        default_width=12,
        change_width=False,
        required=False)


class IGalleryPortletRandomImageRendererSettings(Interface):
    """Gallery portlet random image renderer settings interface"""

    thumb_selection = BootstrapThumbnailsSelectionField(
        title=_("Images selection"),
        description=_("Selection used to display images"),
        default_width=2,
        change_width=True,
        required=False)
