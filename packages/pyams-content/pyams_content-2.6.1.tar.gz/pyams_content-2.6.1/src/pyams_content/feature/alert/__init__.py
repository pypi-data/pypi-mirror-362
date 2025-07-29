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

"""PyAMS_content.feature.alert module

"""
from itertools import chain

from persistent import Persistent
from zope.container.contained import Contained
from zope.schema.fieldproperty import FieldProperty

from pyams_content.feature.alert.interfaces import ALERT_MANAGER_KEY, IAlertManagerInfo
from pyams_content.shared.alert import ALERT_CONTENT_TYPE
from pyams_content.shared.alert.interfaces import IAlertManager
from pyams_sequence.reference import InternalReferenceMixin, get_reference_target
from pyams_site.interfaces import ISiteRoot
from pyams_utils.adapter import adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.list import unique_iter
from pyams_utils.registry import query_utility


@factory_config(IAlertManagerInfo)
class AlertManagerInfo(InternalReferenceMixin, Persistent, Contained):
    """Alert manager info"""

    _reference = FieldProperty(IAlertManagerInfo['reference'])
    context_view = FieldProperty(IAlertManagerInfo['context_view'])

    @property
    def reference(self):
        """Internal reference getter"""
        return self._reference

    @reference.setter
    def reference(self, value):
        """Internal reference setter"""
        self._reference = value
        del self.target

    def get_visible_alerts(self, request):
        """Iterator over visible alerts"""

        def check_alert(alert):
            """Hide alerts matching current request context"""
            for target in alert.get_targets():
                if target is request.context:
                    return False
            return True

        view = get_reference_target(self.reference)
        if view is None:
            return
        yield from filter(check_alert,
                          view.get_results(context=request.context,
                                           request=request,
                                           content_type=ALERT_CONTENT_TYPE))

    def get_context_alerts(self, request, context=None):
        """Iterator over visible alerts associated with provided context"""
        if context is None:
            context = request.context
        # extract alerts from selected context view
        view = get_reference_target(self.context_view)
        if view is not None:
            shared_alerts = view.get_results(context=context,
                                             request=request,
                                             content_type=ALERT_CONTENT_TYPE)
        else:
            shared_alerts = ()
        # extract context alerts from alerts manager
        manager = query_utility(IAlertManager)
        if manager is not None:
            context_alerts = manager.find_context_alerts(context, request)
        else:
            context_alerts = ()
        yield from unique_iter(chain(shared_alerts, context_alerts))


@adapter_config(context=ISiteRoot,
                provides=IAlertManagerInfo)
def site_root_alerts_manager_info(context):
    """Site root alerts manager information factory"""
    return get_annotation_adapter(context, ALERT_MANAGER_KEY, IAlertManagerInfo)
