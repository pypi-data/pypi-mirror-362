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

"""PyAMS_content.feature.alert.interfaces module

"""

from zope.interface import Interface

from pyams_content.shared.view import VIEW_CONTENT_TYPE
from pyams_sequence.schema import InternalReferenceField

__docformat__ = 'restructuredtext'

from pyams_content import _


ALERT_MANAGER_KEY = 'pyams_content.alerts'


class IAlertManagerInfo(Interface):
    """Alert manager info interface"""

    reference = InternalReferenceField(title=_("Global alerts view"),
                                       description=_("Internal view target reference; please note that alerts "
                                                     "content type selection will be added automatically to "
                                                     "settings of the selected view"),
                                       content_type=VIEW_CONTENT_TYPE,
                                       required=False)

    context_view = InternalReferenceField(title=_("Context alerts view"),
                                          description=_("Reference to the view used to get context alerts; please "
                                                        "note that alerts content type selection will be added "
                                                        "automatically to settings of the selected view"),
                                          content_type=VIEW_CONTENT_TYPE,
                                          required=False)

    def get_visible_alerts(self, request):
        """Iterator over visible alerts"""

    def get_context_alerts(self, request, context=None):
        """Iterator over visible alerts associated with request context"""
