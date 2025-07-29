# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

import json

from zope.interface import implementer
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.map.interfaces import IMapParagraph
from pyams_content.component.map.skin.interfaces import IBaseMapRendererSettings, IMapDefaultRendererSettings
from pyams_content.feature.renderer import DefaultContentRenderer, IContentRenderer
from pyams_gis.configuration import MapConfiguration
from pyams_gis.interfaces.configuration import IMapConfiguration
from pyams_gis.interfaces.utility import IMapManager
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import DEFAULT_RENDERER_NAME
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_utils.dict import update_dict
from pyams_utils.factory import factory_config
from pyams_utils.registry import get_utility

__docformat__ = 'restructuredtext'

from pyams_content import _


@implementer(IBaseMapRendererSettings)
class BaseMapRendererSettings(MapConfiguration):
    """Map default renderer settings"""

    use_default_map_configuration = FieldProperty(IBaseMapRendererSettings['use_default_map_configuration'])
    map_height = FieldProperty(IBaseMapRendererSettings['map_height'])
    display_marker = FieldProperty(IBaseMapRendererSettings['display_marker'])
    display_coordinates = FieldProperty(IBaseMapRendererSettings['display_coordinates'])

    @property
    def no_use_default_map_configuration(self):
        return not bool(self.use_default_map_configuration)

    @no_use_default_map_configuration.setter
    def no_use_default_map_configuration(self, value):
        self.use_default_map_configuration = not bool(value)

    @property
    def configuration(self):
        if self.use_default_map_configuration:
            manager = get_utility(IMapManager)
            return IMapConfiguration(manager)
        return self

    def get_marker(self, context):
        """Marker position getter"""
        if self.display_marker and context.position:
            coordinates = context.position.wgs_coordinates
            return {
                'lon': float(coordinates['longitude']),
                'lat': float(coordinates['latitude'])
            }

    def get_map_configuration(self, context):
        configuration = self.configuration.get_configuration()
        update_dict(configuration, 'marker', self.get_marker(context))
        return json.dumps(configuration)


@factory_config(IMapDefaultRendererSettings)
class MapDefaultRendererSettings(BaseMapRendererSettings):
    """Map default renderer settings"""


@adapter_config(name=DEFAULT_RENDERER_NAME,
                required=(IMapParagraph, IPyAMSLayer),
                provides=IContentRenderer)
@template_config(template='templates/map-default.pt',
                 layer=IPyAMSLayer)
class MapParagraphDefaultRenderer(DefaultContentRenderer):
    """Map paragraph default renderer"""

    label = _("Simple map renderer (default)")

    settings_interface = IMapDefaultRendererSettings
