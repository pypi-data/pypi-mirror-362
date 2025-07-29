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

"""PyAMS_content.component.illustration.paragraph module

"""

from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.illustration import BasicIllustration
from pyams_content.component.illustration.interfaces import IIllustrationParagraph, \
    ILLUSTRATION_PARAGRAPH_ICON_CLASS, ILLUSTRATION_PARAGRAPH_NAME, \
    ILLUSTRATION_PARAGRAPH_RENDERERS, ILLUSTRATION_PARAGRAPH_TYPE
from pyams_content.component.paragraph import BaseParagraph
from pyams_content.component.paragraph.interfaces import IBaseParagraph
from pyams_content.feature.renderer import RenderersVocabulary
from pyams_utils.factory import factory_config
from pyams_utils.vocabulary import vocabulary_config


__docformat__ = 'restructuredtext'


@factory_config(IIllustrationParagraph)
@factory_config(IBaseParagraph, name=ILLUSTRATION_PARAGRAPH_TYPE)
class IllustrationParagraph(BasicIllustration, BaseParagraph):
    """Illustration paragraph persistent class"""

    factory_name = ILLUSTRATION_PARAGRAPH_TYPE
    factory_label = ILLUSTRATION_PARAGRAPH_NAME
    factory_intf = IIllustrationParagraph

    icon_class = ILLUSTRATION_PARAGRAPH_ICON_CLASS

    description = FieldProperty(IIllustrationParagraph['description'])
    renderer = FieldProperty(IIllustrationParagraph['renderer'])


@vocabulary_config(name=ILLUSTRATION_PARAGRAPH_RENDERERS)
class IllustrationParagraphRenderersVocabulary(RenderersVocabulary):
    """Illustration paragraph renderers vocabulary"""

    content_interface = IIllustrationParagraph
