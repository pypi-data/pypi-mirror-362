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

"""PyAMS_content.component.paragraph.interfaces.html module

This module defines interfaces of HTML paragraphs
"""

from pyams_content.component.paragraph.interfaces import IBaseParagraph
from pyams_content.component.paragraph.schema import ParagraphRendererChoice
from pyams_i18n.schema import I18nHTMLField, I18nTextField


__docformat__ = 'restructuredtext'

from pyams_content import _


#
# Raw HTML code paragraph
#

RAW_PARAGRAPH_TYPE = 'raw'
RAW_PARAGRAPH_NAME = _("Raw HTML code")
RAW_PARAGRAPH_RENDERERS = 'PyAMS_content.paragraph.raw.renderers'
RAW_PARAGRAPH_ICON_CLASS = 'fas fa-code'


class IRawParagraph(IBaseParagraph):
    """Raw HTML code paragraph interface"""

    body = I18nTextField(title=_("Source code"),
                         description=_("You can use &lt;CTRL&gt;+&lt;,&gt; to change "
                                       "editor settings"),
                         required=False)

    renderer = ParagraphRendererChoice(description=_("Paragraph renderer"),
                                       renderers=RAW_PARAGRAPH_RENDERERS)


#
# Rich text HTML paragraph
#

HTML_PARAGRAPH_TYPE = 'html'
HTML_PARAGRAPH_NAME = _("Rich text")
HTML_PARAGRAPH_RENDERERS = 'PyAMS_content.paragraph.html.renderers'
HTML_PARAGRAPH_ICON_CLASS = 'fas fa-font'


class IHTMLParagraph(IBaseParagraph):
    """Rich text paragraph interface"""

    body = I18nHTMLField(title=_("Body"),
                         required=False)

    renderer = ParagraphRendererChoice(description=_("Presentation template used for this "
                                                     "paragraph"),
                                       renderers=HTML_PARAGRAPH_RENDERERS)
