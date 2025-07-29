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

"""PyAMS_content.feature.header.portlet module

"""

from zope.schema.fieldproperty import FieldProperty

from pyams_content.feature.header.portlet.interfaces import IPageHeaderPortletSettings, PAGE_HEADER_ICON_CLASS, \
    PAGE_HEADER_PORTLET_NAME
from pyams_portal.portlet import Portlet, PortletSettings, portlet_config
from pyams_utils.factory import factory_config

__docformat__ = 'restructuredtext'

from pyams_content import _


@factory_config(IPageHeaderPortletSettings)
class PageHeaderPortletSettings(PortletSettings):
    """Page header portlet settings"""

    display_logo = FieldProperty(IPageHeaderPortletSettings['display_logo'])
    display_context_title = FieldProperty(IPageHeaderPortletSettings['display_context_title'])
    display_profile_link = FieldProperty(IPageHeaderPortletSettings['display_profile_link'])


@portlet_config(permission=None)
class PageHeaderPortlet(Portlet):
    """Page header portlet"""

    name = PAGE_HEADER_PORTLET_NAME
    label = _("Page header")

    settings_factory = IPageHeaderPortletSettings
    toolbar_css_class = PAGE_HEADER_ICON_CLASS
