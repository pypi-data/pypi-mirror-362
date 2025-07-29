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

"""PyAMS_content.component.illustration.portlet module

This module provides illustration portlet.
"""

from pyams_content.component.illustration.portlet.interfaces import IIllustrationPortletSettings
from pyams_portal.portlet import Portlet, PortletSettings, portlet_config
from pyams_utils.factory import factory_config


__docformat__ = 'restructuredtext'

from pyams_content import _


ILLUSTRATION_PORTLET_NAME = 'pyams_content.portlet.illustration'
ILLUSTRATION_ICON_CLASS = 'far fa-image'


@factory_config(IIllustrationPortletSettings)
class IllustrationPortletSettings(PortletSettings):
    """Illustration portlet settings"""


@portlet_config(permission=None)
class IllustrationPortlet(Portlet):
    """Illustration portlet"""

    name = ILLUSTRATION_PORTLET_NAME
    label = _("Illustration")

    settings_factory = IIllustrationPortletSettings
    toolbar_css_class = ILLUSTRATION_ICON_CLASS
