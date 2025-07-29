# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from zope.interface import Interface

from pyams_content.component.map.portlet.interfaces import IMapPortletSettings
from pyams_content.component.map.portlet.skin.interfaces import IMapPortletDefaultRendererSettings
from pyams_content.component.map.skin import MapDefaultRendererSettings
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import IPortalContext, IPortletRenderer
from pyams_portal.skin import PortletRenderer
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_utils.factory import factory_config

__docformat__ = 'restructuredtext'

from pyams_content import _


@factory_config(IMapPortletDefaultRendererSettings)
class MapPortletDefaultRendererSettings(MapDefaultRendererSettings):
    """Map portlet default renderer settings persistent class"""


@adapter_config(required=(IPortalContext, IPyAMSLayer, Interface, IMapPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/map-default.pt', layer=IPyAMSLayer)
class MapPortletDefaultRenderer(PortletRenderer):
    """Map portlet default renderer"""

    label = _("Simple map (default)")

    settings_interface = IMapPortletDefaultRendererSettings
