#
# Copyright (c) 2015-2024 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.component.contact.portlet.skin.zmi module

This module defines components for contact portlet renderer settings management interface.
"""

from pyams_content.component.contact.portlet.skin.interfaces import IContactPortletDefaultRendererSettings
from pyams_form.field import Fields
from pyams_form.interfaces.form import IFormFields, IGroup
from pyams_gis.interfaces.configuration import IMapConfiguration
from pyams_portal.zmi.interfaces import IPortletRendererSettingsEditForm
from pyams_utils.adapter import adapter_config
from pyams_zmi.form import FormGroupChecker
from pyams_zmi.interfaces import IAdminLayer

__docformat__ = 'restructuredtext'


@adapter_config(required=(IContactPortletDefaultRendererSettings, IAdminLayer, IPortletRendererSettingsEditForm),
                provides=IFormFields)
def contact_portlet_default_settings_form_fields(context, request, view):
    """Contact portlet default renderer settings form fields"""
    return Fields(IContactPortletDefaultRendererSettings).select('link_label')


@adapter_config(name='photo-display',
                required=(IContactPortletDefaultRendererSettings, IAdminLayer, IPortletRendererSettingsEditForm),
                provides=IGroup)
class ContactPortletDefaultRendererPhotoSettingsGroup(FormGroupChecker):
    """Contact portlet default renderer photo settings group"""

    def __new__(cls, context, request, view):
        if not context.__parent__.photo:
            return None
        return FormGroupChecker.__new__(cls)

    fields = Fields(IContactPortletDefaultRendererSettings).select('display_photo', 'photo_position')
    weight = 10


@adapter_config(name='map-display',
                required=(IContactPortletDefaultRendererSettings, IAdminLayer, IPortletRendererSettingsEditForm),
                provides=IGroup)
class ContactPortletDefaultRendererMapSettingsGroup(FormGroupChecker):
    """Contact paragraph default renderer map settings group"""

    def __new__(cls, context, request, view):
        if not context.__parent__.position:
            return None
        return FormGroupChecker.__new__(cls)

    fields = Fields(IContactPortletDefaultRendererSettings).select('display_map', 'map_position',
                                                                   'display_marker', 'display_coordinates')
    weight = 20


@adapter_config(name='map-configuration',
                required=(IContactPortletDefaultRendererSettings, IAdminLayer,
                          ContactPortletDefaultRendererMapSettingsGroup),
                provides=IGroup)
class ContactPortletParagraphDefaultRendererMapConfigurationGroup(FormGroupChecker):
    """Contact paragraph default render map configuration group"""

    fields = Fields(IContactPortletDefaultRendererSettings).select('no_use_default_map_configuration') + \
        Fields(IMapConfiguration)
