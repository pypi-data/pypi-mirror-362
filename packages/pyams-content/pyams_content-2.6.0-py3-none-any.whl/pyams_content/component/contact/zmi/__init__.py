# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.component.contact.portlet module

This module defines contact paragraph management interface components.
"""

from zope.interface import alsoProvides

from pyams_content.component.contact.interfaces import CONTACT_PARAGRAPH_ICON_CLASS, CONTACT_PARAGRAPH_NAME, \
    CONTACT_PARAGRAPH_TYPE, IContactParagraph
from pyams_content.component.paragraph.interfaces import IParagraphContainer, IParagraphContainerTarget
from pyams_content.component.paragraph.zmi import BaseParagraphAddForm, BaseParagraphAddMenu, \
    InnerParagraphPropertiesEditForm, ParagraphPropertiesEditFormMixin
from pyams_content.component.paragraph.zmi.interfaces import IInnerParagraphEditForm, IParagraphContainerBaseTable
from pyams_form.ajax import ajax_form_config
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_utils.adapter import adapter_config
from pyams_utils.interfaces.data import IObjectData
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalEditForm
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager

__docformat__ = 'restructuredtext'


class ContactParagraphBaseFormMixin:
    """Contact paragraph base form mixin"""

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        contact_email = self.widgets.get('contact_email')
        if contact_email is not None:
            contact_email.object_data = {
                'input-mask': {
                    'alias': 'email',
                    'clearIncomplete': True
                }
            }
            alsoProvides(contact_email, IObjectData)
        phone_number = self.widgets.get('phone_number')
        if phone_number is not None:
            phone_number.object_data = {
                'input-mask': {
                    'mask': '[+9{3}] 99 99 99 99 99',
                    'clearIncomplete': True
                }
            }
            alsoProvides(phone_number, IObjectData)


@viewlet_config(name='add-contact-paragraph.menu',
                context=IParagraphContainerTarget, layer=IAdminLayer,
                view=IParagraphContainerBaseTable,
                manager=IContextAddingsViewletManager, weight=600)
class ContactParagraphAddMenu(BaseParagraphAddMenu):
    """Contact paragraph add menu"""

    label = CONTACT_PARAGRAPH_NAME
    icon_class = CONTACT_PARAGRAPH_ICON_CLASS

    factory_name = CONTACT_PARAGRAPH_TYPE
    href = 'add-contact-paragraph.html'


@ajax_form_config(name='add-contact-paragraph.html',
                  context=IParagraphContainer, layer=IPyAMSLayer)
class ContactParagraphAddForm(ContactParagraphBaseFormMixin, BaseParagraphAddForm):
    """Contact paragraph add form"""
    
    content_factory = IContactParagraph


class ContactParagraphPropertiesEditFormMixin(ContactParagraphBaseFormMixin,
                                              ParagraphPropertiesEditFormMixin):
    """Contact paragraph properteis edit form mixin"""


@adapter_config(required=(IContactParagraph, IAdminLayer),
                provides=IInnerParagraphEditForm)
class ContactParagraphInnerPropertiesEditForm(ContactParagraphPropertiesEditFormMixin,
                                              InnerParagraphPropertiesEditForm):
    """Contact paragraph inner properties edit form"""


@ajax_form_config(name='properties.html',
                  context=IContactParagraph, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class ContactParagraphPropertiesEditForm(ContactParagraphPropertiesEditFormMixin,
                                         AdminModalEditForm):
    """Contact paragraph properties edit form"""
