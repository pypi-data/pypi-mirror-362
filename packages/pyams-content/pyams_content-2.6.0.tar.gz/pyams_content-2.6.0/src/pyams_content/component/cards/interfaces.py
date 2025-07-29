#
# Copyright (c) 2015-2024 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.component.cards.interfaces module

Bootstrap cards paragraph interfaces.
"""

from pyams_content.component.paragraph import IBaseParagraph
from pyams_content.component.paragraph.schema import ParagraphRendererChoice
from pyams_portal.portlets.cards import ICardsContainer

__docformat__ = 'restructuredtext'

from pyams_content import _


CARDS_PARAGRAPH_TYPE = 'cards'
CARDS_PARAGRAPH_NAME = _("Bootstrap cards")
CARDS_PARAGRAPH_RENDERERS = 'PyAMS_content.paragraph.cards.renderers'
CARDS_PARAGRAPH_ICON_CLASS = 'fas fa-clipboard-list'


class ICardsParagraph(ICardsContainer, IBaseParagraph):
    """Cards paragraph interface"""

    renderer = ParagraphRendererChoice(description=_("Presentation template used for cards"),
                                       renderers=CARDS_PARAGRAPH_RENDERERS)
