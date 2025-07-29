# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from pyams_content.component.paragraph.interfaces import IBaseParagraph, IParagraphContainerTarget
from pyams_content.component.paragraph.schema import ParagraphRendererChoice

__docformat__ = 'restructuredtext'

from pyams_content import _


GROUP_PARAGRAPH_TYPE = 'group'
GROUP_PARAGRAPH_NAME = _("Paragraphs group")
GROUP_PARAGRAPH_RENDERERS = 'PyAMS_content.paragraph.group.renderers'
GROUP_PARAGRAPH_ICON_CLASS = 'fas fa-layer-group'


class IParagraphsGroup(IBaseParagraph, IParagraphContainerTarget):
    """Paragraphs group interface"""

    renderer = ParagraphRendererChoice(description=_("Presentation template used for this frame"),
                                       renderers=GROUP_PARAGRAPH_RENDERERS)
