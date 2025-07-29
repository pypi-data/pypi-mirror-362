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

"""PyAMS_content.component.verbatim.portlet.zmi module

This module defines management interface components for verbatim portlet.
"""

from zope.interface import Interface

from pyams_content.component.verbatim.portlet.interfaces import IVerbatimPortletSettings
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import IPortletPreviewer
from pyams_portal.zmi import PortletPreviewer
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_utils.html import html_to_text

__docformat__ = 'restructuredtext'


@adapter_config(required=(Interface, IPyAMSLayer, Interface, IVerbatimPortletSettings),
                provides=IPortletPreviewer)
@template_config(template='templates/verbatim-preview.pt', layer=IPyAMSLayer)
class VerbatimPortletPreviewer(PortletPreviewer):
    """Verbatim portlet previewer"""

    @staticmethod
    def html_to_text(quote):
        return html_to_text(quote)
