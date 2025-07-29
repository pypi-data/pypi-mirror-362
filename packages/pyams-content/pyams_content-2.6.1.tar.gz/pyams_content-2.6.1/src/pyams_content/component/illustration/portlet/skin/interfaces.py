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

"""PyAMS_content.component.illustration.portlet.skin.interfaces module

This module provides illustration portlet renderers settings interfaces.
"""

from zope.interface import Interface
from zope.schema import Bool

from pyams_skin.schema import BootstrapThumbnailsSelectionField


__docformat__ = 'restructuredtext'

from pyams_content import _


class IIllustrationPortletBaseRendererSettings(Interface):
    """Illustration portlet base renderer settings interface"""

    thumb_selection = BootstrapThumbnailsSelectionField(
        title=_("Image selection"),
        description=_("Illustration can use responsive selections, but you "
                      "can also force selection of another specific format"),
        default_width=12,
        change_width=False,
        required=False)


class IIllustrationPortletDefaultRendererSettings(IIllustrationPortletBaseRendererSettings):
    """Illustration portlet default renderer settings interface"""

    display_title = Bool(title=_("Display image title"),
                         description=_("Select 'no' to hide illustration title"),
                         required=True,
                         default=True)

    display_author = Bool(title=_("Display author"),
                          description=_("Select 'no' to hide illustration author name"),
                          required=True,
                          default=True)

    display_description = Bool(title=_("Display description"),
                               description=_("Select 'no' to hide image description"),
                               required=True,
                               default=True)


class IIllustrationPortletSideRendererSettings(IIllustrationPortletBaseRendererSettings):
    """Illustration portlet side renderer settings interface"""

    thumb_selection = BootstrapThumbnailsSelectionField(
        title=_("Image selection"),
        description=_("Illustration can use responsive selections, but you "
                      "can also force selection of another specific format"),
        default_width=5,
        required=False)

    zoom_on_click = Bool(title=_("Zoom on click"),
                         description=_("If 'yes', a click on illustration thumbnail will open a "
                                       "modal window to display image"),
                         required=True,
                         default=True)

    def get_css_cols(self, side):
        """Get columns width matching current configuration"""
