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

"""PyAMS_content.component.frame.portlet.interfaces module

This module defines framed text portlet interfaces.
"""

from pyams_content.component.frame.interfaces import IFrameInfo
from pyams_content.component.illustration import IIllustrationTarget
from pyams_i18n.schema import I18nTextLineField
from pyams_portal.interfaces import IPortletSettings

__docformat__ = 'restructuredtext'

from pyams_content import _


class IFramePortletSettings(IPortletSettings, IFrameInfo, IIllustrationTarget):
    """Rich text portlet settings interface"""

    title = I18nTextLineField(title=_("Title"),
                              required=False)
