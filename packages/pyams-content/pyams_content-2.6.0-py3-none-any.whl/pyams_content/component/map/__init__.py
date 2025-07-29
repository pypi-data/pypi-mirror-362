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

"""PyAMS_content.component.map module

This is the base module of location maps paragraphs and portlets.
"""

from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.map.interfaces import IMapParagraph, MAP_PARAGRAPH_ICON_CLASS, MAP_PARAGRAPH_NAME, \
    MAP_PARAGRAPH_RENDERERS, MAP_PARAGRAPH_TYPE
from pyams_content.component.paragraph import BaseParagraph
from pyams_content.component.paragraph.interfaces import IBaseParagraph
from pyams_content.feature.renderer import RenderersVocabulary
from pyams_utils.factory import factory_config
from pyams_utils.vocabulary import vocabulary_config

__docformat__ = 'restructuredtext'


@factory_config(IMapParagraph)
@factory_config(IBaseParagraph, name=MAP_PARAGRAPH_TYPE)
class MapParagraph(BaseParagraph):
    """Map paragraph persistent class"""

    factory_name = MAP_PARAGRAPH_TYPE
    factory_label = MAP_PARAGRAPH_NAME
    factory_intf = IMapParagraph

    icon_class = MAP_PARAGRAPH_ICON_CLASS
    secondary = True

    position = FieldProperty(IMapParagraph['position'])


@vocabulary_config(name=MAP_PARAGRAPH_RENDERERS)
class MapParagraphRenderersVocabulary(RenderersVocabulary):
    """Map paragraph renderers vocabulary"""

    content_interface = IMapParagraph
