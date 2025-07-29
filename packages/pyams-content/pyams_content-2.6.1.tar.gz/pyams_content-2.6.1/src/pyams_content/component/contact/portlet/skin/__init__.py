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

"""PyAMS_content.component.contact.portlet.skin module

This module defines default renderer and renderer settings for contact card portlet.
"""

from zope.interface import Interface

from pyams_content.component.contact.portlet.interfaces import IContactPortletSettings
from pyams_content.component.contact.portlet.skin.interfaces import IContactPortletDefaultRendererSettings
from pyams_content.component.contact.skin import ContactDefaultRendererSettings
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import IPortalContext, IPortletRenderer
from pyams_portal.skin import PortletRenderer
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_utils.factory import factory_config

__docformat__ = 'restructuredtext'

from pyams_content import _


@factory_config(IContactPortletDefaultRendererSettings)
class ContactPortletDefaultRendererSettings(ContactDefaultRendererSettings):
    """Contact portlet default renderer settings persistent class"""


@adapter_config(required=(IPortalContext, IPyAMSLayer, Interface, IContactPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/contact-default.pt', layer=IPyAMSLayer)
class ContactPortletDefaultRenderer(PortletRenderer):
    """Contact portlet default renderer"""

    label = _("Simple contact card (default)")

    settings_interface = IContactPortletDefaultRendererSettings
