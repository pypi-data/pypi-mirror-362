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

"""PyAMS_*** module

"""

__docformat__ = 'restructuredtext'

from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.cards.interfaces import CARDS_PARAGRAPH_ICON_CLASS, CARDS_PARAGRAPH_NAME, \
    CARDS_PARAGRAPH_RENDERERS, CARDS_PARAGRAPH_TYPE, ICardsParagraph
from pyams_content.component.paragraph import BaseParagraph, IBaseParagraph
from pyams_content.feature.renderer import RenderersVocabulary
from pyams_portal.portlets.cards import CardsContainer
from pyams_utils.factory import factory_config
from pyams_utils.vocabulary import vocabulary_config


@factory_config(ICardsParagraph)
@factory_config(IBaseParagraph, name=CARDS_PARAGRAPH_TYPE)
class CardsParagraph(CardsContainer, BaseParagraph):
    """Bootstrap cards paragraph"""

    factory_name = CARDS_PARAGRAPH_TYPE
    factory_label = CARDS_PARAGRAPH_NAME
    factory_intf = ICardsParagraph

    icon_class = CARDS_PARAGRAPH_ICON_CLASS
    secondary = True

    renderer = FieldProperty(ICardsParagraph['renderer'])


@vocabulary_config(name=CARDS_PARAGRAPH_RENDERERS)
class CardsParagraphRenderersVocabulary(RenderersVocabulary):
    """Cards paragraph renderers vocabulary"""

    content_interface = ICardsParagraph
