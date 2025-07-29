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

"""PyAMS_content.shared.alert module

This module defines alerts persistent classes.
"""

from zope.interface import implementer
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.thesaurus import ITagsTarget, IThemesTarget
from pyams_content.feature.review import IReviewTarget
from pyams_content.shared.alert.interfaces import ALERT_CONTENT_NAME, ALERT_CONTENT_TYPE, IAlert, IAlertManager, \
    IAlertTypesManager, IWfAlert
from pyams_content.shared.common import ISharedContent, IWfSharedContent, SharedContent, WfSharedContent
from pyams_sequence.reference import InternalReferenceMixin, get_reference_target
from pyams_utils.factory import factory_config
from pyams_utils.request import check_request
from pyams_utils.traversing import get_parent

__docformat__ = 'restructuredtext'


@factory_config(IWfAlert)
@factory_config(IWfSharedContent, name=ALERT_CONTENT_TYPE)
@implementer(ITagsTarget, IThemesTarget, IReviewTarget)
class WfAlert(WfSharedContent, InternalReferenceMixin):
    """Base alert"""

    content_type = ALERT_CONTENT_TYPE
    content_name = ALERT_CONTENT_NAME
    content_intf = IWfAlert
    content_view = False

    handle_content_url = False
    handle_header = False
    handle_description = False

    alert_type = FieldProperty(IWfAlert['alert_type'])
    body = FieldProperty(IWfAlert['body'])
    _reference = FieldProperty(IWfAlert['reference'])
    external_url = FieldProperty(IWfAlert['external_url'])
    references = FieldProperty(IWfAlert['references'])
    maximum_interval = FieldProperty(IWfAlert['maximum_interval'])

    def get_alert_type(self):
        """Alert type getter"""
        manager = get_parent(self, IAlertManager)
        types = IAlertTypesManager(manager, None)
        if types is not None:
            return types.get(self.alert_type)

    @property
    def reference(self):
        return self._reference

    @reference.setter
    def reference(self, value):
        self._reference = value
        del self.target

    def get_targets(self, state=None):
        request = check_request()
        return [
            get_reference_target(reference, state, request)
            for reference in (self.references or ())
        ]


@factory_config(IAlert)
@factory_config(ISharedContent, name=ALERT_CONTENT_TYPE)
class Alert(SharedContent):
    """Workflow managed alert class"""

    content_type = ALERT_CONTENT_TYPE
    content_name = ALERT_CONTENT_NAME
    content_view = False
