# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from zope.schema import Choice

from pyams_content.component.paragraph.interfaces import DEFAULT_PARAGRAPH_RENDERER_NAME

__docformat__ = 'restructuredtext'

from pyams_content import _


class ParagraphRendererChoice(Choice):
    """Paragraph renderer choice schema field factory"""

    def __init__(self, description, renderers):
        super().__init__(title=_("Renderer"),
                         description=description,
                         vocabulary=renderers,
                         default=DEFAULT_PARAGRAPH_RENDERER_NAME)
