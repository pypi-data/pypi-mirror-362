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

"""PyAMS_content.component.verbatim.interfaces module

This module defines interfaces common to all text verbatim components.
"""

from zope.container.constraints import contains
from zope.container.interfaces import IOrderedContainer
from zope.interface import Interface
from zope.schema import Bool, TextLine

from pyams_content.component.paragraph.interfaces import IBaseParagraph
from pyams_content.component.paragraph.schema import ParagraphRendererChoice
from pyams_i18n.schema import I18nHTMLField, I18nTextLineField

__docformat__ = 'restructuredtext'

from pyams_content import _


class IVerbatimBase(Interface):
    """Base verbatim interface"""

    quote = I18nHTMLField(title=_("Quoted text"),
                          description=_("Quotation marks will be added automatically "
                                        "by presentation template..."),
                          required=False)
    
    author = TextLine(title=_("Author"),
                      description=_("Name of the quote author"),
                      required=False)
    
    charge = I18nTextLineField(title=_("In charge of"),
                               description=_("Label of author function"),
                               required=False)


class IVerbatimInfo(IVerbatimBase):
    """Verbatim information interface"""
    
    title = I18nTextLineField(title=_("Title"),
                              description=_("Verbatim title"),
                              required=False)
    
    visible = Bool(title=_("Visible?"),
                   description=_("Is this verbatim visible in front-office?"),
                   required=True,
                   default=True)


class IVerbatimContainer(IOrderedContainer):
    """Verbatim container interface"""

    contains(IVerbatimInfo)

    def get_visible_items(self):
        """Get iterator over visible verbatim"""


#
# Verbatim paragraph
#

VERBATIM_PARAGRAPH_TYPE = 'verbatim'
VERBATIM_PARAGRAPH_NAME = _("Verbatim")
VERBATIM_PARAGRAPH_RENDERERS = 'PyAMS_content.paragraph.verbatim.renderers'
VERBATIM_PARAGRAPH_ICON_CLASS = 'fas fa-quote-right'


class IVerbatimParagraph(IVerbatimBase, IBaseParagraph):
    """Verbatim paragraph interface"""

    renderer = ParagraphRendererChoice(description=_("Presentation template used for this verbatim"),
                                       renderers=VERBATIM_PARAGRAPH_RENDERERS)
