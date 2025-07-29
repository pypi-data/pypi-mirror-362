# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.component.contact.portlet.interfaces module

This module defines interfaces of contact portlet settings.
"""

from pyams_content.component.contact.interfaces import IContactInfo
from pyams_i18n.schema import I18nTextLineField
from pyams_portal.interfaces import IPortletSettings

__docformat__ = 'restructuredtext'

from pyams_content import _


class IContactPortletSettings(IPortletSettings, IContactInfo):
    """Contact portlet settings interface"""

    title = I18nTextLineField(title=_("Title"),
                              required=False)
