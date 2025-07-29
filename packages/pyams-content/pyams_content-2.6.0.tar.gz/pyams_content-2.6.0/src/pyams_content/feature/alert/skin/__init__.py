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

"""PyAMS_*** module

"""

__docformat__ = 'restructuredtext'

from zope.interface import Interface

from pyams_content.feature.alert import IAlertManagerInfo
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSUserLayer
from pyams_template.template import template_config
from pyams_viewlet.viewlet import ViewContentProvider, contentprovider_config


@contentprovider_config(name='pyams_content.alerts',
                        layer=IPyAMSUserLayer, view=Interface)
@template_config(template='templates/alerts.pt',
                 layer=IPyAMSUserLayer)
class AlertsContentProvider(ViewContentProvider):
    """Alerts content provider"""

    def get_alerts(self):
        """Alerts getter"""
        alerts = IAlertManagerInfo(self.request.root, None)
        if alerts is not None:
            yield from alerts.get_visible_alerts(self.request)

    def get_gravity(self, alert):
        """Alert gravity getter"""
        alert_type = alert.get_alert_type()
        if alert_type is not None:
            return II18n(alert_type).query_attribute('label', request=self.request)


@contentprovider_config(name='pyams_content.context_alerts',
                        layer=IPyAMSUserLayer, view=Interface)
@template_config(template='templates/context-alerts.pt',
                 layer=IPyAMSUserLayer)
class ContextAlertsContentProvider(AlertsContentProvider):
    """Content alerts content provider"""

    def get_alerts(self):
        """Context alerts getter"""
        alerts = IAlertManagerInfo(self.request.root, None)
        if alerts is not None:
            yield from alerts.get_context_alerts(self.request)
