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

"""PyAMS_content.component.association.paragraph module

This module defines a paragraph factory which is only used to store associations.
"""

from zope.interface import implementer
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.association.interfaces import ASSOCIATION_PARAGRAPH_ICON_CLASS, \
    ASSOCIATION_PARAGRAPH_NAME, ASSOCIATION_PARAGRAPH_RENDERERS, ASSOCIATION_PARAGRAPH_TYPE, \
    IAssociationParagraph
from pyams_content.component.extfile.interfaces import IExtFileContainerTarget
from pyams_content.component.links.interfaces import ILinkContainerTarget
from pyams_content.component.paragraph import BaseParagraph, IBaseParagraph
from pyams_content.feature.renderer import RenderersVocabulary
from pyams_utils.factory import factory_config
from pyams_utils.vocabulary import vocabulary_config


__docformat__ = 'restructuredtext'


@factory_config(IAssociationParagraph)
@factory_config(IBaseParagraph, name=ASSOCIATION_PARAGRAPH_TYPE)
@implementer(IExtFileContainerTarget, ILinkContainerTarget)
class AssociationParagraph(BaseParagraph):
    """Associations paragraph"""

    factory_name = ASSOCIATION_PARAGRAPH_TYPE
    factory_label = ASSOCIATION_PARAGRAPH_NAME
    factory_intf = IAssociationParagraph

    icon_class = ASSOCIATION_PARAGRAPH_ICON_CLASS

    renderer = FieldProperty(IAssociationParagraph['renderer'])


@vocabulary_config(name=ASSOCIATION_PARAGRAPH_RENDERERS)
class AssociationParagraphRenderersVocabulary(RenderersVocabulary):
    """Associations paragraph renderers vocabulary"""

    content_interface = IAssociationParagraph
