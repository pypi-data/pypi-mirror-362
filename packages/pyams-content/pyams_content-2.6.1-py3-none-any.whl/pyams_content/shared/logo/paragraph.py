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
from pyams_content.shared.logo.interfaces import ILogosParagraph, LOGOS_PARAGRAPH_ICON_CLASS, LOGOS_PARAGRAPH_NAME, \
    LOGOS_PARAGRAPH_RENDERERS, LOGOS_PARAGRAPH_TYPE
from pyams_sequence.reference import InternalReferenceMixin, get_reference_target
from pyams_utils.factory import factory_config
from pyams_utils.vocabulary import vocabulary_config

__docformat__ = 'restructuredtext'


@factory_config(ILogosParagraph)
@factory_config(IBaseParagraph, name=LOGOS_PARAGRAPH_TYPE)
class LogosParagraph(BaseParagraph):
    """Logos paragraph"""
    
    factory_name = LOGOS_PARAGRAPH_TYPE
    factory_label = LOGOS_PARAGRAPH_NAME
    factory_intf = ILogosParagraph
    
    icon_class = LOGOS_PARAGRAPH_ICON_CLASS
    secondary = True
    
    references = FieldProperty(ILogosParagraph['references'])
    renderer = FieldProperty(ILogosParagraph['renderer'])

    def get_logos(self, status=None, with_reference=False):
        for reference in self.references or ():
            target = get_reference_target(reference, status)
            if target is not None:
                yield (reference, target) if with_reference else target
        
    def get_targets(self, state=None):
        return self.get_logos(state)
    

@vocabulary_config(name=LOGOS_PARAGRAPH_RENDERERS)
class LogosParagraphRenderersVocabulary(RenderersVocabulary):
    """Logos paragraph renderers vocabulary"""

    content_interface = ILogosParagraph
