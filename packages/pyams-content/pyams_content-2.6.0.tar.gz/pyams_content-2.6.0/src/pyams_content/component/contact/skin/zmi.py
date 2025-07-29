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

This module defines components for contact paragraph renderer settings management interface.
"""

from pyams_content.component.contact.skin.interfaces import IContactDefaultRendererSettings
from pyams_content.component.paragraph.zmi.interfaces import IParagraphRendererSettingsEditForm
from pyams_form.field import Fields
from pyams_form.interfaces.form import IFormFields, IGroup
from pyams_gis.interfaces.configuration import IMapConfiguration
from pyams_utils.adapter import adapter_config
from pyams_zmi.form import FormGroupChecker
from pyams_zmi.interfaces import IAdminLayer

__docformat__ = 'restructuredtext'


@adapter_config(required=(IContactDefaultRendererSettings, IAdminLayer, IParagraphRendererSettingsEditForm),
                provides=IFormFields)
def contact_paragraph_default_renderer_settings_form_fields(context, request, view):
    return Fields(IContactDefaultRendererSettings).select('link_label')


@adapter_config(name='photo-display',
                required=(IContactDefaultRendererSettings, IAdminLayer, IParagraphRendererSettingsEditForm),
                provides=IGroup)
class ContactParagraphDefaultRendererPhotoSettingsGroup(FormGroupChecker):
    """Contact paragraph default renderer photo settings group"""

    def __new__(cls, context, request, view):
        if not context.__parent__.photo:
            return None
        return FormGroupChecker.__new__(cls)

    fields = Fields(IContactDefaultRendererSettings).select('display_photo', 'photo_position')
    weight = 10


@adapter_config(name='map-display',
                required=(IContactDefaultRendererSettings, IAdminLayer, IParagraphRendererSettingsEditForm),
                provides=IGroup)
class ContactParagraphDefaultRendererMapSettingsGroup(FormGroupChecker):
    """Contact paragraph default renderer map settings group"""

    def __new__(cls, context, request, view):
        if not context.__parent__.position:
            return None
        return FormGroupChecker.__new__(cls)

    fields = Fields(IContactDefaultRendererSettings).select('display_map', 'map_position',
                                                            'display_marker', 'display_coordinates')
    weight = 20


@adapter_config(name='map-configuration',
                required=(IContactDefaultRendererSettings, IAdminLayer, ContactParagraphDefaultRendererMapSettingsGroup),
                provides=IGroup)
class ContactParagraphDefaultRendererMapConfigurationGroup(FormGroupChecker):
    """Contact paragraph default render map configuration group"""

    fields = Fields(IContactDefaultRendererSettings).select('no_use_default_map_configuration') + \
        Fields(IMapConfiguration)
