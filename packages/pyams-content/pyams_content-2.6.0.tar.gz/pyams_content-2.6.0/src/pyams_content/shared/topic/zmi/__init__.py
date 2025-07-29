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

"""PyAMS_content.shared.topic.zmi module

This module defines topics management components.
"""

from zope.interface import Interface

from pyams_content.shared.common.zmi.types.content import TypedSharedContentPropertiesEditForm
from pyams_content.shared.topic import IWfTopic
from pyams_form.ajax import ajax_form_config
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_utils.adapter import adapter_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IContentManagementMenu, IMenuHeader


__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(required=(IWfTopic, IAdminLayer, Interface, IContentManagementMenu),
                provides=IMenuHeader)
def topic_management_menu_header(context, request, view, manager):
    """Topic management menu header"""
    return request.localizer.translate(_("Topic management"))


@ajax_form_config(name='properties.html',
                  context=IWfTopic, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class TopicPropertiesEditForm(TypedSharedContentPropertiesEditForm):
    """Topic properties edit form"""

    interface = IWfTopic
