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

"""PyAMS_content.component.fields.interfaces module

This module defines form fields paragraph interface.
"""

__docformat__ = 'restructuredtext'

from pyams_content.component.paragraph import IBaseParagraph
from pyams_content.component.paragraph.schema import ParagraphRendererChoice

from pyams_content import _


#
# Form fields paragraphs interfaces
#

FORM_FIELDS_PARAGRAPH_TYPE = 'form-fields'
FORM_FIELDS_PARAGRAPH_NAME = _("Form fields")
FORM_FIELDS_PARAGRAPH_RENDERERS = 'PyAMS_content.paragraph.form-fields.renderers'
FORM_FIELDS_PARAGRAPH_ICON_CLASS = 'fas fa-th-list'


class IFormFieldsParagraph(IBaseParagraph):
    """Form fields paragraph"""

    renderer = ParagraphRendererChoice(
        description=_("Presentation template used for form fields"),
        renderers=FORM_FIELDS_PARAGRAPH_RENDERERS)
