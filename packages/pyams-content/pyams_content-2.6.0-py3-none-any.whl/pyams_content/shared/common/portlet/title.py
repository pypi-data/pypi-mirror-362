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

"""PyAMS_content.shared.common.portlet.title module

This module defines a small shared content title portlet, which can be used
instead of header portlet just to render content title.
"""

from zope.schema.fieldproperty import FieldProperty

from pyams_content.shared.common.portlet.interfaces import ISharedContentTitlePortletSettings, TITLE_PORTLET_NAME
from pyams_portal.portlet import Portlet, PortletSettings, portlet_config
from pyams_utils.factory import factory_config

__docformat__ = 'restructuredtext'

from pyams_content import _


@factory_config(provided=ISharedContentTitlePortletSettings)
class SharedContentTitlePortletSettings(PortletSettings):
    """Shared content title portlet settings"""

    display_publication_date = FieldProperty(ISharedContentTitlePortletSettings['display_publication_date'])
    publication_date_prefix = FieldProperty(ISharedContentTitlePortletSettings['publication_date_prefix'])
    display_specificities = FieldProperty(ISharedContentTitlePortletSettings['display_specificities'])


@portlet_config(permission=None)
class SharedContentTitlePortlet(Portlet):
    """Shared content title portlet"""

    name = TITLE_PORTLET_NAME
    label = _("Content title")

    settings_factory = ISharedContentTitlePortletSettings
    toolbar_css_class = 'fas fa-bold'
