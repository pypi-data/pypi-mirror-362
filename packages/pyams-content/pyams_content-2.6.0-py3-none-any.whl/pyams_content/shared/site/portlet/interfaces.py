# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from pyams_i18n.schema import I18nTextLineField
from pyams_portal.interfaces import IPortletSettings

__docformat__ = 'restructuredtext'

from pyams_content import _


SITE_CONTAINER_SUMMARY_PORTLET_NAME = 'pyams_content.portlet.site.summary'


class ISiteContainerSummaryPortletSettings(IPortletSettings):
    """Site container summary portlet settings"""

    title = I18nTextLineField(title=_("Title"),
                              required=False)

    button_title = I18nTextLineField(title=_("Button's title"),
                                     description=_("Navigation button's title is normally defined based on "
                                                   "target's content type; you can override this label by giving a "
                                                   "custom title here"),
                                     required=False)
