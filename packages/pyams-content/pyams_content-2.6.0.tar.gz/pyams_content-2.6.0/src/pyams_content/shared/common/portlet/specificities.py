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

"""PyAMS_content.shared.common.portlet.specificities module

This module defines a shared content "specificities" portlet.

Specificities renderers are based on named adapters for shared
contents which are handling specificities.
"""

from pyams_content.shared.common.portlet.interfaces import ISharedContentSpecificitiesPortletSettings, \
    SPECIFICITIES_PORTLET_NAME
from pyams_portal.portlet import Portlet, PortletSettings, portlet_config
from pyams_utils.factory import factory_config

__docformat__ = 'restructuredtext'

from pyams_content import _


@factory_config(provided=ISharedContentSpecificitiesPortletSettings)
class SharedContentSpecificitiesPortletSettings(PortletSettings):
    """Shared content specificities portlet settings"""


@portlet_config(permission=None)
class SharedContentSpecificitiesPortlet(Portlet):
    """Shared content specificities portlet"""

    name = SPECIFICITIES_PORTLET_NAME
    label = _("Content specificities")

    settings_factory = ISharedContentSpecificitiesPortletSettings
    toolbar_css_class = 'fas fa-paperclip'
