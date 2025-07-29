# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

__docformat__ = 'restructuredtext'

from pyams_content.interfaces import IBaseContent
from pyams_content.shared.site.portlet.skin import ISiteContainerSummaryItemTitle
from pyams_content.shared.site.skin.interfaces import ISiteContainerSummaryView
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSUserLayer
from pyams_utils.adapter import adapter_config


@adapter_config(required=(IBaseContent, IPyAMSUserLayer, ISiteContainerSummaryView),
                provides=ISiteContainerSummaryItemTitle)
def base_content_container_summary_item_title(context, request, view):
    """Base content container summary item title"""
    return II18n(context).query_attribute('title', request=request)
