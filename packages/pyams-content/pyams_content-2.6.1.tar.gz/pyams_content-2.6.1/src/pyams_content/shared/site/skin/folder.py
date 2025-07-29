# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from pyramid.httpexceptions import HTTPSeeOther

from pyams_content.shared.site.interfaces import ISiteElementNavigation, ISiteFolder, SITE_CONTAINER_REDIRECT_MODE
from pyams_content.shared.site.portlet.skin.interfaces import ISiteContainerSummaryItemHeader, \
    ISiteContainerSummaryItemTitle, ISiteContainerSummaryItemURL
from pyams_content.shared.site.skin.interfaces import ISiteContainerSummaryView
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSUserLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_portal.skin.page import PortalContextIndexPage, PortalContextPreviewPage
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_utils.adapter import ContextRequestAdapter, adapter_config
from pyams_utils.url import absolute_url, relative_url
from pyams_workflow.interfaces import IWorkflowPublicationInfo

__docformat__ = 'restructuredtext'


@adapter_config(required=(ISiteFolder, IPyAMSUserLayer, ISiteContainerSummaryView),
                provides=ISiteContainerSummaryItemTitle)
def site_folder_container_summary_item_title(context, request, view):
    """Site folder container summary item title getter"""
    return II18n(context).query_attributes_in_order(('navigation_title', 'title'), request=request)


@adapter_config(required=(ISiteFolder, IPyAMSUserLayer, ISiteContainerSummaryView),
                provides=ISiteContainerSummaryItemHeader)
def site_folder_container_summary_item_header(context, request, view):
    """Site folder container summary item  header"""
    return II18n(context).query_attribute('header', request=request)


@adapter_config(required=(ISiteFolder, IPyAMSUserLayer, ISiteContainerSummaryView),
                provides=ISiteContainerSummaryItemURL)
def site_folder_container_summary_item_target(context, request, view):
    """Site folder container summary item target URL"""
    return absolute_url(context, request)


@adapter_config(context=(ISiteFolder, IPyAMSUserLayer),
                provides=ISiteElementNavigation)
class SiteFolderNavigation(ContextRequestAdapter):
    """Site folder navigation adapter"""

    @property
    def visible(self):
        if not self.context.visible_in_list:
            return False
        return IWorkflowPublicationInfo(self.context).is_visible(self.request)


@pagelet_config(name='',
                context=ISiteFolder, layer=IPyAMSUserLayer)
class SiteFolderIndexPage(PortalContextIndexPage):
    """Site folder index page"""

    def __call__(self, **kwargs):
        if self.context.navigation_mode == SITE_CONTAINER_REDIRECT_MODE:
            target = next(self.context.get_visible_items(self.request), None)
            if target is not None:
                return HTTPSeeOther(relative_url(target, request=self.request))
        return super().__call__(**kwargs)


@pagelet_config(name='preview.html',
                context=ISiteFolder, layer=IPyAMSUserLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class SiteFolderPreviewPage(PortalContextPreviewPage):
    """Site folder preview page"""

    def __call__(self, **kwargs):
        if self.context.navigation_mode == SITE_CONTAINER_REDIRECT_MODE:
            target = next(self.context.get_visible_items(self.request), None)
            if target is not None:
                return HTTPSeeOther(relative_url(target, request=self.request,
                                                 view_name='preview.html'))
        return super().__call__(**kwargs)
