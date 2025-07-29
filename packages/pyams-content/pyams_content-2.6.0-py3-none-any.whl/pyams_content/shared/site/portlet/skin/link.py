# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from pyams_content.shared.site.interfaces import IExternalSiteLink, IInternalSiteLink
from pyams_content.shared.site.portlet.skin.interfaces import ISiteContainerSummaryItemButtonTitle, \
    ISiteContainerSummaryItemHeader, ISiteContainerSummaryItemTitle, \
    ISiteContainerSummaryItemURL
from pyams_content.shared.site.skin.interfaces import ISiteContainerSummaryView
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSUserLayer
from pyams_utils.adapter import adapter_config
from pyams_utils.url import canonical_url, relative_url

__docformat__ = 'restructuredtext'


#
# Internal site links adapters
#

@adapter_config(required=(IInternalSiteLink, IPyAMSUserLayer, ISiteContainerSummaryView),
                provides=ISiteContainerSummaryItemTitle)
def internal_site_link_container_summary_item_title(context, request, view):
    """Internal site link container summary item title getter"""
    title = II18n(context).query_attribute('navigation_title', request=request)
    if not title:
        target = context.get_target(request=request)
        if target is not None:
            title = request.registry.queryMultiAdapter((target, request, view),
                                                       ISiteContainerSummaryItemTitle)
    return title


@adapter_config(required=(IInternalSiteLink, IPyAMSUserLayer, ISiteContainerSummaryView),
                provides=ISiteContainerSummaryItemHeader)
def internal_site_link_container_summary_item_header(context, request, view):
    """Internal site link container summary item  header"""
    if not context.show_header:
        return None
    header = II18n(context).query_attribute('navigation_header', request=request)
    if not header:
        target = context.get_target(request=request)
        if target is not None:
            header = request.registry.queryMultiAdapter((target, request, view),
                                                        ISiteContainerSummaryItemHeader)
    return header


@adapter_config(required=(IInternalSiteLink, IPyAMSUserLayer, ISiteContainerSummaryView),
                provides=ISiteContainerSummaryItemButtonTitle)
def internal_site_link_container_summary_item_button_title(context, request, view):
    """Internal site link container summary item button title"""
    target = context.get_target(request=request)
    if target is not None:
        return request.registry.queryMultiAdapter((target, request, view),
                                                  ISiteContainerSummaryItemButtonTitle)
    return None
    
    
@adapter_config(required=(IInternalSiteLink, IPyAMSUserLayer, ISiteContainerSummaryView),
                provides=ISiteContainerSummaryItemURL)
def internal_site_link_container_summary_item_target(context, request, view):
    """Internal site link container summary item target URL"""
    target = context.get_target(request=request)
    if target is not None:
        if context.force_canonical_url:
            return canonical_url(target, request)
        return relative_url(target, request)
    return None


#
# External site links adapters
#

@adapter_config(required=(IExternalSiteLink, IPyAMSUserLayer, ISiteContainerSummaryView),
                provides=ISiteContainerSummaryItemTitle)
def external_site_link_container_summary_item_title(context, request, view):
    """External site link container summary item title getter"""
    return II18n(context).query_attribute('navigation_title', request=request)


@adapter_config(required=(IExternalSiteLink, IPyAMSUserLayer, ISiteContainerSummaryView),
                provides=ISiteContainerSummaryItemHeader)
def external_site_link_container_summary_item_header(context, request, view):
    """External site link container summary item header"""
    if not context.show_header:
        return None
    return II18n(context).query_attribute('navigation_header', request=request)


@adapter_config(required=(IExternalSiteLink, IPyAMSUserLayer, ISiteContainerSummaryView),
                provides=ISiteContainerSummaryItemURL)
def external_site_link_container_summary_item_target(context, request, view):
    """External site link container summary item URL"""
    return context.url
