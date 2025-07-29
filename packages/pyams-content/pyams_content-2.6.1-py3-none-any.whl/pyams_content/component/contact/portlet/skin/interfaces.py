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

"""PyAMS_content.component.contact.portlet.skin.interfaces module

This module defines interfaces of contact portlet renderers settings.
"""

from pyams_content.component.contact.skin.interfaces import IContactDefaultRendererSettings
from pyams_portal.interfaces import IPortletRendererSettings

__docformat__ = 'restructuredtext'


class IContactPortletDefaultRendererSettings(IPortletRendererSettings, IContactDefaultRendererSettings):
    """Contact portlet default renderer settings interface"""
