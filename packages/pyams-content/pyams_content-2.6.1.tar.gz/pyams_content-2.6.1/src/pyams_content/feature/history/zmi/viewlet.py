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

"""PyAMS_content.feature.history.zmi.viewlet module

This module provides a small content provider which can be used to display
previous history comments.
"""

__docformat__ = 'restructuredtext'

from pyams_content.feature.history import IHistoryContainer
from pyams_security.utility import get_principal
from pyams_template.template import template_config
from pyams_utils.date import format_datetime
from pyams_utils.timezone import tztime
from pyams_viewlet.viewlet import BaseContentProvider
from pyams_zmi.interfaces import IAdminLayer


@template_config(template='templates/history.pt', layer=IAdminLayer)
class HistoryCommentsContentProvider(BaseContentProvider):
    """Comments history content provider"""

    history = None

    def update(self):
        super().update()
        self.history = IHistoryContainer(self.context, None)

    def render(self, template_name=''):
        if not self.history:
            return ''
        return super().render(template_name)

    def get_principal(self, item):
        return get_principal(self.request, item.principal).title

    @staticmethod
    def get_timestamp(item):
        return format_datetime(tztime(item.timestamp))
