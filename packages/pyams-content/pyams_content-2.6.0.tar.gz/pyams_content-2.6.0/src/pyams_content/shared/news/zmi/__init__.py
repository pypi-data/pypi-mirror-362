#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.shared.news.zmi module

This module defines news management components.
"""

from zope.interface import Interface

from pyams_content.shared.common.zmi import SharedContentPropertiesEditForm
from pyams_content.shared.news import IWfNews
from pyams_form.ajax import ajax_form_config
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_utils.adapter import adapter_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IContentManagementMenu, IMenuHeader

__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(required=(IWfNews, IAdminLayer, Interface, IContentManagementMenu),
                provides=IMenuHeader)
def news_management_menu_header(context, request, view, manager):
    """News management menu header"""
    return request.localizer.translate(_("News management"))


@ajax_form_config(name='properties.html',
                  context=IWfNews, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class NewsPropertiesEditForm(SharedContentPropertiesEditForm):
    """News properties edit form"""

    interface = IWfNews
