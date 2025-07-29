# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from pyams_content.component.map.portlet.skin.interfaces import IMapPortletDefaultRendererSettings
from pyams_content.component.map.skin.interfaces import IMapDefaultRendererSettings
from pyams_form.field import Fields
from pyams_form.interfaces.form import IFormFields, IGroup
from pyams_gis.interfaces.configuration import IMapConfiguration
from pyams_portal.zmi.interfaces import IPortletRendererSettingsEditForm
from pyams_utils.adapter import adapter_config
from pyams_zmi.form import FormGroupChecker
from pyams_zmi.interfaces import IAdminLayer

__docformat__ = 'restructuredtext'


@adapter_config(required=(IMapDefaultRendererSettings, IAdminLayer, IPortletRendererSettingsEditForm),
                provides=IFormFields)
def map_portlet_default_settings_form_fields(context, request, view):
    """Map portlet default renderer settings form fields"""
    return Fields(IMapDefaultRendererSettings).select('map_height', 'display_marker',
                                                      'display_coordinates')


@adapter_config(name='map-configuration',
                required=(IMapPortletDefaultRendererSettings, IAdminLayer, IPortletRendererSettingsEditForm),
                provides=IGroup)
class MapPortletDefaultRendererConfigurationGroup(FormGroupChecker):
    """Map portlet default renderer configuration group"""

    fields = Fields(IMapPortletDefaultRendererSettings).select('no_use_default_map_configuration') + \
        Fields(IMapConfiguration)
