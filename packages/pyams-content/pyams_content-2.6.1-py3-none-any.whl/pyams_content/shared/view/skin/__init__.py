#
# Copyright (c) 2015-2023 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.shared.view.skin module

This module defines a simple view which is used to get a preview of view items.
"""

from pyams_content.shared.view import IWfView
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_portal.skin.page import PortalContextPreviewPage
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_template.template import template_config

__docformat__ = 'restructuredtext'


@pagelet_config(name='preview.html',
                context=IWfView, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
@template_config(template='templates/preview.pt', layer=IPyAMSLayer)
class ViewPreviewPage(PortalContextPreviewPage):
    """Shared view preview page"""

    @property
    def items(self):
        return self.context.get_results(self.context, ignore_cache=True, request=self.request)
