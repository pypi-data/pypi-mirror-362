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

"""PyAMS_content.shared.common.portlet.header module

This module defines a shared content header portlet.
"""

from zope.schema.fieldproperty import FieldProperty

from pyams_content.shared.common.portlet.interfaces import HEADER_PORTLET_NAME, ISharedContentHeaderPortletSettings
from pyams_portal.portlet import Portlet, PortletSettings, portlet_config
from pyams_utils.factory import factory_config

__docformat__ = 'restructuredtext'

from pyams_content import _


@factory_config(provided=ISharedContentHeaderPortletSettings)
class SharedContentHeaderPortletSettings(PortletSettings):
    """Shared content portlet settings"""

    display_illustration = FieldProperty(ISharedContentHeaderPortletSettings['display_illustration'])
    display_breadcrumbs = FieldProperty(ISharedContentHeaderPortletSettings['display_breadcrumbs'])
    display_title = FieldProperty(ISharedContentHeaderPortletSettings['display_title'])
    display_tags = FieldProperty(ISharedContentHeaderPortletSettings['display_tags'])
    display_header = FieldProperty(ISharedContentHeaderPortletSettings['display_header'])
    display_publication_date = FieldProperty(ISharedContentHeaderPortletSettings['display_publication_date'])
    publication_date_prefix = FieldProperty(ISharedContentHeaderPortletSettings['publication_date_prefix'])
    display_alerts = FieldProperty(ISharedContentHeaderPortletSettings['display_alerts'])
    display_specificities = FieldProperty(ISharedContentHeaderPortletSettings['display_specificities'])


@portlet_config(permission=None)
class SharedContentHeaderPortlet(Portlet):
    """Shared content header portlet"""

    name = HEADER_PORTLET_NAME
    label = _("Content header")

    settings_factory = ISharedContentHeaderPortletSettings
    toolbar_css_class = 'fas fa-header'
