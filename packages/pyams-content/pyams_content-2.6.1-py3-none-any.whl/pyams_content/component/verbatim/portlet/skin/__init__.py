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

"""PyAMS_content.component.verbatim.portlet.skin module

This module defines renderers for verbatim portlet.
"""

from zope.interface import Interface

from pyams_content.component.verbatim.portlet.interfaces import IVerbatimPortletSettings
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import IPortalContext, IPortletRenderer
from pyams_portal.skin import PortletRenderer
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config

__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(required=(IPortalContext, IPyAMSLayer, Interface, IVerbatimPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/verbatim-default.pt', layer=IPyAMSLayer)
class VerbatimPortletRenderer(PortletRenderer):
    """Verbatim portlet renderer"""
    
    label = _("Full width verbatim (default)")
