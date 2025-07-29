# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from pyams_content.feature.search import ISearchFolder
from pyams_content.shared.site.interfaces import ISiteElementNavigation
from pyams_content.shared.site.portlet.skin.interfaces import ISiteContainerSummaryItemHeader, \
    ISiteContainerSummaryItemTitle, ISiteContainerSummaryItemURL
from pyams_content.shared.site.skin.interfaces import ISiteContainerSummaryView
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSUserLayer
from pyams_utils.adapter import ContextRequestAdapter, adapter_config
from pyams_utils.url import absolute_url
from pyams_workflow.interfaces import IWorkflowPublicationInfo

__docformat__ = 'restructuredtext'


@adapter_config(required=(ISearchFolder, IPyAMSUserLayer, ISiteContainerSummaryView),
                provides=ISiteContainerSummaryItemTitle)
def search_folder_container_summary_item_title(context, request, view):
    """Site folder container summary item  header adapter"""
    return II18n(context).query_attributes_in_order(('navigation_title', 'title'), request=request)


@adapter_config(required=(ISearchFolder, IPyAMSUserLayer, ISiteContainerSummaryView),
                provides=ISiteContainerSummaryItemHeader)
def search_folder_container_summary_item_header(context, request, view):
    """Site folder container summary item  header adapter"""
    return II18n(context).query_attribute('header', request=request)


@adapter_config(required=(ISearchFolder, IPyAMSUserLayer, ISiteContainerSummaryView),
                provides=ISiteContainerSummaryItemURL)
def search_folder_container_summary_item_url(context, request, view):
    """Site folder container summary item target URL adapter"""
    return absolute_url(context, request)


@adapter_config(context=(ISearchFolder, IPyAMSUserLayer),
                provides=ISiteElementNavigation)
class SearchFolderNavigation(ContextRequestAdapter):
    """Site folder navigation adapter"""

    @property
    def visible(self):
        if not self.context.visible_in_list:
            return False
        return IWorkflowPublicationInfo(self.context).is_visible(self.request)
