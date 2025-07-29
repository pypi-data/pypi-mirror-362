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

"""PyAMS_content.component.fields.zmi.paragraph module

This modules provides components for management of form fields paragraphs.
"""

__docformat__ = 'restructuredtext'

from pyams_content.component.fields.interfaces import FORM_FIELDS_PARAGRAPH_ICON_CLASS, \
    FORM_FIELDS_PARAGRAPH_NAME, FORM_FIELDS_PARAGRAPH_TYPE, IFormFieldsParagraph
from pyams_content.component.paragraph import IParagraphContainer, IParagraphContainerTarget
from pyams_content.component.paragraph.zmi import BaseParagraphAddForm, BaseParagraphAddMenu, \
    IParagraphContainerBaseTable
from pyams_form.ajax import ajax_form_config
from pyams_layer.interfaces import IPyAMSLayer
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager


@viewlet_config(name='add-form-fields-paragraph.menu',
                context=IParagraphContainerTarget, layer=IAdminLayer,
                view=IParagraphContainerBaseTable,
                manager=IContextAddingsViewletManager, weight=600)
class FormFieldsParagraphAddMenu(BaseParagraphAddMenu):
    """Form fields paragraph add menu"""

    label = FORM_FIELDS_PARAGRAPH_NAME
    icon_class = FORM_FIELDS_PARAGRAPH_ICON_CLASS

    factory_name = FORM_FIELDS_PARAGRAPH_TYPE
    href = 'add-form-fields-paragraph.html'


@ajax_form_config(name='add-form-fields-paragraph.html',
                  context=IParagraphContainer, layer=IPyAMSLayer)
class FormFieldsParagraphAddForm(BaseParagraphAddForm):
    """Form fields paragraph add form"""

    content_factory = IFormFieldsParagraph
