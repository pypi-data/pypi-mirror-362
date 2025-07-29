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

"""PyAMS_content.ocmponent.frame.portlet.skin.interfaces module

This module defines framed text portlet renderers settings interfaces.
"""

from pyams_content.component.frame.skin import IFrameDefaultRendererSettings, IFrameLateralRendererSettings
from pyams_portal.interfaces import IPortletRendererSettings

__docformat__ = 'restructuredtext'


class IFramePortletDefaultRendererSettings(IPortletRendererSettings, IFrameDefaultRendererSettings):
    """Frame portlet default renderer settings interface"""


class IFramePortletLateralRendererSettings(IPortletRendererSettings, IFrameLateralRendererSettings):
    """Frame portlet lateral renderer settings interface"""
