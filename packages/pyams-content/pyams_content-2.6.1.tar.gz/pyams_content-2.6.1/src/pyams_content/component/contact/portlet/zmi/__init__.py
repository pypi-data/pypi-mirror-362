# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.component.contact.portlet.zmi module

This module defines components for contact portlet settings management interface.
"""

from zope.interface import Interface, alsoProvides

from pyams_content.component.contact.portlet.interfaces import IContactPortletSettings
from pyams_form.field import Fields
from pyams_form.interfaces.form import IInnerSubForm
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import IPortletPreviewer
from pyams_portal.zmi import PortletPreviewer
from pyams_portal.zmi.interfaces import IPortletConfigurationEditor
from pyams_portal.zmi.portlet import PortletConfigurationEditForm
from pyams_portal.zmi.widget import RendererSelectFieldWidget
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_utils.interfaces.data import IObjectData
from pyams_zmi.interfaces import IAdminLayer

__docformat__ = 'restructuredtext'


@adapter_config(name='configuration',
                required=(IContactPortletSettings, IAdminLayer, IPortletConfigurationEditor),
                provides=IInnerSubForm)
class ContactPortletSettingsEditForm(PortletConfigurationEditForm):
    """Contact portlet settings edit form"""

    @property
    def fields(self):
        fields = Fields(IContactPortletSettings).select('title', 'name', 'charge', 'company',
                                                        'contact_email', 'phone_number', 'contact_form', 'photo',
                                                        'address', 'position', 'renderer', 'devices_visibility',
                                                        'css_class')
        fields['renderer'].widget_factory = RendererSelectFieldWidget
        return fields

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


@adapter_config(required=(Interface, IPyAMSLayer, Interface, IContactPortletSettings),
                provides=IPortletPreviewer)
@template_config(template='templates/contact-preview.pt', layer=IPyAMSLayer)
class ContactPortletPreviewer(PortletPreviewer):
    """Contact portlet previewer"""
