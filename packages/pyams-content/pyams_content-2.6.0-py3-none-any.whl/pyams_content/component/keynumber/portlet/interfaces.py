# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from pyams_content.component.keynumber import IKeyNumbersContainer
from pyams_content.feature.navigation import IMenusContainer
from pyams_i18n.schema import I18nTextField, I18nTextLineField
from pyams_portal.interfaces import IPortletSettings

__docformat__ = 'restructuredtext'

from pyams_content import _


class IKeyNumbersPortletSettings(IPortletSettings, IKeyNumbersContainer):
    """Key number portlet settings interface"""
    
    title = I18nTextLineField(title=_("Title"),
                              description=_("Main component title"),
                              required=False)
    
    header = I18nTextField(title=_("Header"),
                           description=_("Short text to be displayed below title"),
                           required=False)
