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

"""PyAMS_content.component.verbatim.portlet module

This module defines base verbatim portlet and settings.
"""

from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.verbatim import VerbatimContainer
from pyams_content.component.verbatim.portlet.interfaces import IVerbatimPortletSettings
from pyams_portal.portlet import Portlet, PortletSettings, portlet_config
from pyams_utils.factory import factory_config

__docformat__ = 'restructuredtext'

from pyams_content import _


VERBATIM_PORTLET_NAME = 'pyams_content.portlet.verbatim'


@factory_config(provided=IVerbatimPortletSettings)
class VerbatimPortletSettings(VerbatimContainer, PortletSettings):
    """Verbatim portlet settings"""

    title = FieldProperty(IVerbatimPortletSettings['title'])
    lead = FieldProperty(IVerbatimPortletSettings['lead'])


@portlet_config(permission=None)
class VerbatimPortlet(Portlet):
    """Verbatim portlet"""

    name = VERBATIM_PORTLET_NAME
    label = _("Verbatim")

    settings_factory = IVerbatimPortletSettings
    toolbar_css_class = 'fas fa-quote-right'
