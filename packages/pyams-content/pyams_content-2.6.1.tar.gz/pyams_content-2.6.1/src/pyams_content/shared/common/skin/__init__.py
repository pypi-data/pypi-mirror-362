#
# Copyright (c) 2015-2022 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.shared.common.skin module

This is the base module of shared contents content providers.
"""

from pyams_content.shared.common import ISharedContent, IWfSharedContent
from pyams_content.shared.common.interfaces import ISharedTool
from pyams_content.shared.common.interfaces.types import IWfTypedSharedContent
from pyams_content.shared.site.interfaces import ISiteElementNavigation
from pyams_content.shared.site.portlet.skin.interfaces import ISiteContainerSummaryItemButtonTitle, \
    ISiteContainerSummaryItemHeader, ISiteContainerSummaryItemTitle, \
    ISiteContainerSummaryItemURL
from pyams_content.shared.site.skin.interfaces import ISiteContainerSummaryView
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSUserLayer
from pyams_utils.adapter import ContextRequestAdapter, adapter_config
from pyams_utils.traversing import get_parent
from pyams_utils.url import relative_url

__docformat__ = 'restructuredtext'

from pyams_workflow.interfaces import IWorkflow, IWorkflowPublicationInfo, IWorkflowVersions


@adapter_config(context=(IWfSharedContent, IPyAMSUserLayer),
                provides=ISiteElementNavigation)
class WfSharedContentNavigation(ContextRequestAdapter):
    """Shared content navigation adapter"""

    @property
    def visible(self):
        return IWorkflowPublicationInfo(self.context).is_visible(self.request)


@adapter_config(required=(ISharedContent, IPyAMSUserLayer),
                provides=ISiteElementNavigation)
def shared_content_site_navigation(context, request):
    """Shared content site navigation"""
    workflow = IWorkflow(context, None)
    if workflow is not None:
        versions = IWorkflowVersions(context, None)
        try:
            visible_version = next(iter(versions.get_versions(workflow.visible_states)))
        except IndexError:
            return None
        else:
            return request.registry.queryMultiAdapter((visible_version, request),
                                                      ISiteElementNavigation)
    return None
    

@adapter_config(required=(IWfSharedContent, IPyAMSUserLayer, ISiteContainerSummaryView),
                provides=ISiteContainerSummaryItemTitle)
def shared_content_container_summary_item_title(context, request, view):
    """Shared content container summary item title"""
    return II18n(context).query_attribute('title', request=request)


@adapter_config(required=(IWfSharedContent, IPyAMSUserLayer, ISiteContainerSummaryView),
                provides=ISiteContainerSummaryItemHeader)
def shared_content_container_summary_item_header(context, request, view):
    """Shared content container summary item  header adapter"""
    return II18n(context).query_attribute('header', request=request)


@adapter_config(required=(IWfSharedContent, IPyAMSUserLayer, ISiteContainerSummaryView),
                provides=ISiteContainerSummaryItemButtonTitle)
def shared_content_container_summary_item_button_title(context, request, view):
    """Shared content container summary item button title"""
    shared_tool = get_parent(context, ISharedTool)
    if shared_tool is not None:
        return II18n(shared_tool).query_attribute('navigation_label', request=request)


@adapter_config(required=(IWfTypedSharedContent, IPyAMSUserLayer, ISiteContainerSummaryView),
                provides=ISiteContainerSummaryItemButtonTitle)
def typed_shared_content_container_summary_item_button_title(context, request, view):
    """Typed shared content container summary item button title"""
    title = None
    data_type = context.get_data_type()
    if data_type is not None:
        title = II18n(data_type).query_attribute('navigation_label', request=request)
    if not title:
        title = shared_content_container_summary_item_button_title(context, request, view)
    return title
    

@adapter_config(required=(IWfSharedContent, IPyAMSUserLayer, ISiteContainerSummaryView),
                provides=ISiteContainerSummaryItemURL)
def shared_content_container_summary_item_target(context, request, view):
    """Shared content container summary item target URL adapter"""
    return relative_url(context, request)
