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

"""PyAMS_content.component.cards.zmi module

This module defines components which are used for management interface
of Bootstrap cards paragraphs.
"""

from pyams_content.component.cards.interfaces import CARDS_PARAGRAPH_ICON_CLASS, CARDS_PARAGRAPH_NAME, \
    CARDS_PARAGRAPH_TYPE, ICardsParagraph
from pyams_content.component.paragraph.interfaces import IParagraphContainer, IParagraphContainerTarget
from pyams_content.component.paragraph.zmi import BaseParagraphAddForm, BaseParagraphAddMenu
from pyams_content.component.paragraph.zmi.interfaces import IParagraphContainerBaseTable
from pyams_form.ajax import ajax_form_config
from pyams_layer.interfaces import IPyAMSLayer
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager

__docformat__ = 'restructuredtext'


@viewlet_config(name='add-cards-paragraph.menu',
                context=IParagraphContainerTarget, layer=IAdminLayer,
                view=IParagraphContainerBaseTable,
                manager=IContextAddingsViewletManager, weight=600)
class CardsParagraphAddMenu(BaseParagraphAddMenu):
    """Cards paragraph add menu"""

    label = CARDS_PARAGRAPH_NAME
    icon_class = CARDS_PARAGRAPH_ICON_CLASS

    factory_name = CARDS_PARAGRAPH_TYPE
    href = 'add-cards-paragraph.html'


@ajax_form_config(name='add-cards-paragraph.html',
                  context=IParagraphContainer, layer=IPyAMSLayer)
class CardsParagraphAddForm(BaseParagraphAddForm):
    """Cards paragraph add form"""

    content_factory = ICardsParagraph
