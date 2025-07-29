# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from pyams_content.component.map.skin.interfaces import IMapDefaultRendererSettings
from pyams_content.component.paragraph.zmi.interfaces import IParagraphRendererSettingsEditForm
from pyams_form.field import Fields
from pyams_form.interfaces.form import IFormFields, IGroup
from pyams_gis.interfaces.configuration import IMapConfiguration
from pyams_utils.adapter import adapter_config
from pyams_zmi.form import FormGroupChecker
from pyams_zmi.interfaces import IAdminLayer

__docformat__ = 'restructuredtext'


@adapter_config(required=(IMapDefaultRendererSettings, IAdminLayer, IParagraphRendererSettingsEditForm),
                provides=IFormFields)
def map_paragraph_default_renderer_settings_form_fields(context, request, view):
    return Fields(IMapDefaultRendererSettings).select('map_height', 'display_marker',
                                                      'display_coordinates')


@adapter_config(name='map-configuration',
                required=(IMapDefaultRendererSettings, IAdminLayer, IParagraphRendererSettingsEditForm),
                provides=IGroup)
class MapParagraphDefaultRendererConfigurationGroup(FormGroupChecker):
    """Map paragraph default render configuration group"""

    fields = Fields(IMapDefaultRendererSettings).select('no_use_default_map_configuration') + \
        Fields(IMapConfiguration)
