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

"""PyAMS_content.feature.navigation;portlet.interfaces module

"""

from zope.interface import Attribute, Interface

from pyams_content.feature.navigation import IMenusContainerTarget
from pyams_content.feature.navigation.interfaces import IMenuLinksContainerTarget
from pyams_i18n.schema import I18nTextLineField
from pyams_portal.interfaces import IPortletSettings


__docformat__ = 'restructuredtext'

from pyams_content import _


class ISimpleNavigationPortletSettings(IMenuLinksContainerTarget, IPortletSettings):
    """Simple navigation portlet settings interface"""

    title = I18nTextLineField(title=_("Title"),
                              description=_("Portlet main title"),
                              required=False)

    links = Attribute("Navigation links")


class ISimpleNavigationMenu(Interface):
    """Simple navigation menu marker interface"""


class IDoubleNavigationPortletSettings(IMenusContainerTarget, IPortletSettings):
    """Double navigation portlet settings interface"""

    title = I18nTextLineField(title=_("Title"),
                              description=_("Portlet main title"),
                              required=False)

    menus = Attribute("Navigation menus")
