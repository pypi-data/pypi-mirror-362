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

"""PyAMS_content.component.frame.interfaces module

This module defines interfaces common to all text frames components.
"""

from zope.interface import Interface
from pyams_content.component.paragraph import IBaseParagraph
from pyams_content.component.paragraph.schema import ParagraphRendererChoice
from pyams_i18n.schema import I18nHTMLField

__docformat__ = 'restructuredtext'

from pyams_content import _


class IFrameInfo(Interface):
    """Base frame interface"""

    body = I18nHTMLField(title=_("Frame body"),
                         required=False)


FRAME_PARAGRAPH_TYPE = 'frame'
FRAME_PARAGRAPH_NAME = _("Framed text")
FRAME_PARAGRAPH_RENDERERS = 'PyAMS_content.paragraph.frame.renderers'
FRAME_PARAGRAPH_ICON_CLASS = 'fas fa-window-maximize'


class IFrameParagraph(IFrameInfo, IBaseParagraph):
    """Frame paragraph interface"""

    renderer = ParagraphRendererChoice(description=_("Presentation template used for this frame"),
                                       renderers=FRAME_PARAGRAPH_RENDERERS)
