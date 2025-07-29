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

"""PyAMS_content.component.fields.paragraph module

This module provides form fields paragraph persistent classes and adapters.
"""

from zope.schema.fieldproperty import FieldProperty
from pyams_content.component.fields.interfaces import FORM_FIELDS_PARAGRAPH_ICON_CLASS, \
    FORM_FIELDS_PARAGRAPH_NAME, FORM_FIELDS_PARAGRAPH_RENDERERS, FORM_FIELDS_PARAGRAPH_TYPE, \
    IFormFieldsParagraph
from pyams_content.component.paragraph import BaseParagraph, IBaseParagraph
from pyams_content.feature.renderer import RenderersVocabulary
from pyams_utils.factory import factory_config


__docformat__ = 'restructuredtext'

from pyams_utils.vocabulary import vocabulary_config


@factory_config(IFormFieldsParagraph)
@factory_config(IBaseParagraph, name=FORM_FIELDS_PARAGRAPH_TYPE)
class FormFieldsParagraph(BaseParagraph):
    """Form fields paragraph"""

    factory_name = FORM_FIELDS_PARAGRAPH_TYPE
    factory_label = FORM_FIELDS_PARAGRAPH_NAME
    factory_intf = IFormFieldsParagraph

    icon_class = FORM_FIELDS_PARAGRAPH_ICON_CLASS
    secondary = True

    renderer = FieldProperty(IFormFieldsParagraph['renderer'])


@vocabulary_config(name=FORM_FIELDS_PARAGRAPH_RENDERERS)
class FormFieldsParagraphRenderersVocabulary(RenderersVocabulary):
    """Form fields paragraph renderers vocabulary"""

    content_interface = IFormFieldsParagraph
