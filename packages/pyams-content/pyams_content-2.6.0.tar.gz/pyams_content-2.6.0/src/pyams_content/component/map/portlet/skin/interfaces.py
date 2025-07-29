# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from pyams_content.component.map.skin.interfaces import IMapDefaultRendererSettings
from pyams_portal.interfaces import IPortletRendererSettings

__docformat__ = 'restructuredtext'


class IMapPortletDefaultRendererSettings(IPortletRendererSettings, IMapDefaultRendererSettings):
    """Map portlet default renderer settings interface"""
