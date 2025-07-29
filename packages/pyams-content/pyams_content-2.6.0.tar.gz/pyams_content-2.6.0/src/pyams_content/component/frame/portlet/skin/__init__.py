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

"""PyAMS_content.component.frame.portlet.skin module

This module defines renderers for framed text portlet.
"""

from zope.interface import Interface

from pyams_content.component.frame.portlet import IFramePortletSettings
from pyams_content.component.frame.portlet.skin.interfaces import IFramePortletDefaultRendererSettings, \
    IFramePortletLateralRendererSettings
from pyams_content.component.frame.skin import FrameDefaultRendererSettings, FrameLateralRendererSettings
from pyams_content.component.illustration import IIllustration
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import IPortalContext, IPortletRenderer
from pyams_portal.skin import PortletRenderer
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_utils.factory import factory_config

__docformat__ = 'restructuredtext'

from pyams_content import _


@factory_config(IFramePortletDefaultRendererSettings)
class FramePortletDefaultRendererSettings(FrameDefaultRendererSettings):
    """Frame portlet default renderer settings"""
    
    
@adapter_config(required=(IPortalContext, IPyAMSLayer, Interface, IFramePortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/frame-default.pt', layer=IPyAMSLayer)
class FramePortletDefaultRenderer(PortletRenderer):
    """Frame portlet default renderer"""

    label = _("Full width frame (default)")

    settings_interface = IFramePortletDefaultRendererSettings

    illustration = None
    illustration_renderer = None

    def update(self):
        super().update()
        illustration = IIllustration(self.settings)
        if illustration.has_data():
            self.illustration = illustration
            self.illustration_renderer = illustration.get_renderer(self.request)
            self.illustration_renderer.update()


@factory_config(IFramePortletLateralRendererSettings)
class FramePortletLateralRendererSettings(FrameLateralRendererSettings):
    """Frame portlet lateral renderer settings"""
    
    
@adapter_config(name='lateral',
                required=(IPortalContext, IPyAMSLayer, Interface, IFramePortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/frame-lateral.pt', layer=IPyAMSLayer)
class FramePortletLateralRenderer(FramePortletDefaultRenderer):
    """Frame portlet default renderer"""

    label = _("Floating lateral frame")

    settings_interface = IFramePortletLateralRendererSettings
