# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.paragraph import BaseParagraph, IBaseParagraph
from pyams_content.feature.renderer import RenderersVocabulary
from pyams_content.shared.common.interfaces import ISpecificitiesParagraph, SPECIFICITIES_PARAGRAPH_ICON_CLASS, \
    SPECIFICITIES_PARAGRAPH_NAME, SPECIFICITIES_PARAGRAPH_RENDERERS, SPECIFICITIES_PARAGRAPH_TYPE
from pyams_utils.factory import factory_config
from pyams_utils.vocabulary import vocabulary_config

__docformat__ = 'restructuredtext'


@factory_config(ISpecificitiesParagraph)
@factory_config(IBaseParagraph, name=SPECIFICITIES_PARAGRAPH_TYPE)
class SpecificitiesParagraph(BaseParagraph):
    """Specificities paragraph"""
    
    factory_name = SPECIFICITIES_PARAGRAPH_TYPE
    factory_label = SPECIFICITIES_PARAGRAPH_NAME
    factory_intf = ISpecificitiesParagraph
    
    icon_class = SPECIFICITIES_PARAGRAPH_ICON_CLASS
    secondary = True
    
    renderer = FieldProperty(ISpecificitiesParagraph['renderer'])


@vocabulary_config(name=SPECIFICITIES_PARAGRAPH_RENDERERS)
class SpecificitiesParagraphRenderersVocabulary(RenderersVocabulary):
    """Specificities paragraph renderers vocabulary"""

    content_interface = ISpecificitiesParagraph
