# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.map.portlet.interfaces import IMapPortletSettings
from pyams_portal.portlet import Portlet, PortletSettings, portlet_config
from pyams_utils.factory import factory_config

__docformat__ = 'restructuredtext'

from pyams_content import _


MAP_PORTLET_NAME = 'pyams_content.portlet.map'


@factory_config(IMapPortletSettings)
class MapPortletSettings(PortletSettings):
    """Map portlet settings"""

    title = FieldProperty(IMapPortletSettings['title'])
    position = FieldProperty(IMapPortletSettings['position'])


@portlet_config(permission=None)
class MapPortlet(Portlet):
    """Map portlet"""

    name = MAP_PORTLET_NAME
    label = _("Location map")

    settings_factory = IMapPortletSettings
    toolbar_css_class = 'fas fa-map-marker'
