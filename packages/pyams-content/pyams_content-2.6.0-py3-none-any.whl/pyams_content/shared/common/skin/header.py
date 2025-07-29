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

"""PyAMS_*** module

"""

from pyams_content.feature.header.interfaces import IPageHeaderTitle
from pyams_content.shared.common import IBaseSharedTool, IWfSharedContent
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_utils.adapter import adapter_config

__docformat__ = 'restructuredtext'


@adapter_config(required=(IBaseSharedTool, IPyAMSLayer),
                provides=IPageHeaderTitle)
def base_shared_tool_page_title(context, request):
    """Base shared tool page title getter"""
    return II18n(context).query_attribute('title', request=request)


@adapter_config(required=(IWfSharedContent, IPyAMSLayer),
                provides=IPageHeaderTitle)
def shared_content_page_title(context, request):
    """Shared content page title getter"""
    return II18n(context).query_attribute('title', request=request)
