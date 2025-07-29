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

"""PyAMS_content.component.illustration.skin.interfaces module

This module provides skin interfaces specific to illustrations rendering.
"""

from zope.interface import Attribute, Interface
from zope.schema import Bool

from pyams_content.feature.renderer import IRendererSettings
from pyams_skin.schema import BootstrapThumbnailsSelectionField


__docformat__ = 'restructuredtext'

from pyams_content import _


#
# Illustrations renderers
#

ILLUSTRATION_BEFORE_TITLE = 'before-title'
ILLUSTRATION_BEFORE_BODY = 'before-body'
ILLUSTRATION_AFTER_BODY = 'after-body'


class IIllustrationRenderer(Interface):
    """Illustration renderer interface"""

    position = Attribute("Illustration position related to its attached content")


class IIllustrationDefaultRendererSettings(IRendererSettings):
    """Illustration default renderer settings interface"""

    thumb_selection = BootstrapThumbnailsSelectionField(
        title=_("Image selection"),
        description=_("Illustration can use responsive selections, but you "
                      "can also force selection of another specific format"),
        default_width=12,
        change_width=False,
        required=False)


class IParagraphIllustrationSideRendererSettings(IIllustrationDefaultRendererSettings):
    """Illustration paragraph side renderer settings interface"""

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
