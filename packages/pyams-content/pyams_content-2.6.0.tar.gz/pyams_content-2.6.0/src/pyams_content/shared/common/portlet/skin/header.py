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

"""PyAMS_content.shared.common.portlet.skin.header module

This module defines shared contents header portlet renderer.
"""

from zope.interface import Interface

from pyams_content.shared.common.portlet.interfaces import ISharedContentHeaderPortletSettings
from pyams_content.skin.interfaces import IContentTitle
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import IPortalContext, IPortletRenderer
from pyams_portal.skin import PortletRenderer
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config

__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(required=(IPortalContext, IPyAMSLayer, Interface, ISharedContentHeaderPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/header-default.pt', layer=IPyAMSLayer)
class SharedContentHeaderPortletRenderer(PortletRenderer):
    """Shared content header portlet renderer"""

    label = _("Shared content header (default)")
    weight = 1

    @property
    def title(self):
        """Title getter"""
        return self.request.registry.queryMultiAdapter((self.context, self.request, self.view),
                                                       IContentTitle) or ''
