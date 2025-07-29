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

"""PyAMS_content.feature.navigation.portlet module

"""

from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.association import IAssociationContainer
from pyams_content.component.association.interfaces import ASSOCIATION_CONTAINER_KEY
from pyams_content.feature.navigation import IMenusContainer
from pyams_content.feature.navigation.interfaces import IMenuLinksContainer
from pyams_content.feature.navigation.portlet.interfaces import IDoubleNavigationPortletSettings, \
    ISimpleNavigationMenu, ISimpleNavigationPortletSettings
from pyams_portal.portlet import Portlet, PortletSettings, portlet_config
from pyams_utils.adapter import adapter_config
from pyams_utils.factory import factory_config

from pyams_content import _


SIMPLE_NAVIGATION_PORTLET_NAME = 'pyams_content.portlet.navigation'
SIMPLE_NAVIGATION_ICON_CLASS = 'fas fa-bars'

SIMPLE_NAVIGATION_LINKS_KEY = f'{ASSOCIATION_CONTAINER_KEY}::links'


@factory_config(ISimpleNavigationPortletSettings)
class SimpleNavigationPortletSettings(PortletSettings):
    """Simple navigation portlet settings"""

    title = FieldProperty(ISimpleNavigationPortletSettings['title'])

    @property
    def links(self):
        """Menu links getter"""
        return IAssociationContainer(self)


@adapter_config(name='links',
                required=ISimpleNavigationPortletSettings,
                provides=IMenuLinksContainer)
def simple_navigation_links_adapter(context):
    """Simple navigation links factory"""
    return context.links


@portlet_config(permission=None)
class SimpleNavigationPortlet(Portlet):
    """Simple navigation portlet"""

    name = SIMPLE_NAVIGATION_PORTLET_NAME
    label = _("Simple navigation menu")

    settings_factory = ISimpleNavigationPortletSettings
    toolbar_css_class = SIMPLE_NAVIGATION_ICON_CLASS


DOUBLE_NAVIGATION_PORTLET_NAME = f'{SIMPLE_NAVIGATION_PORTLET_NAME}::menus'
DOUBLE_NAVIGATION_ICON_CLASS = 'fas fa-table-list'

DOUBLE_NAVIGATION_MENUS8KEY = f'{ASSOCIATION_CONTAINER_KEY}::menus'


@factory_config(IDoubleNavigationPortletSettings)
class DoubleNavigationPortletSettings(PortletSettings):
    """Double navigation portlet settings"""

    title = FieldProperty(IDoubleNavigationPortletSettings['title'])

    @property
    def menus(self):
        """Menus getter"""
        return IMenusContainer(self)


@adapter_config(name='menus',
                required=IDoubleNavigationPortletSettings,
                provides=IMenusContainer)
def double_navigation_menus_adapter(context):
    """Double navigation menus factory"""
    return context.menus


@portlet_config(permission=None)
class DoubleNavigationPortlet(Portlet):
    """Double navigation portlet"""

    name = DOUBLE_NAVIGATION_PORTLET_NAME
    label = _("Double navigation menus")

    settings_factory = IDoubleNavigationPortletSettings
    toolbar_css_class = DOUBLE_NAVIGATION_ICON_CLASS
