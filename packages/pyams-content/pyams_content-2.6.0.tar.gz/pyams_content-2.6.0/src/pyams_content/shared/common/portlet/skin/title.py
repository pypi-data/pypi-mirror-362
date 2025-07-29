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

"""PyAMS_content.shared.common.portlet.skin.title module

This module defines shared content title portlet renderer.
"""

from zope.interface import Interface

from pyams_content.shared.common.portlet.interfaces import ISharedContentTitlePortletSettings
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import IPortalContext, IPortletRenderer
from pyams_portal.skin import PortletRenderer
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config

__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(required=(IPortalContext, IPyAMSLayer, Interface, ISharedContentTitlePortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/title-default.pt', layer=IPyAMSLayer)
class SharedContentTitlePortletRenderer(PortletRenderer):
    """Shared content title portlet renderer"""

    label = _("Shared content title (default)")
    weight = 1
