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

from datetime import datetime, timezone

from hypatia.interfaces import ICatalog
from hypatia.catalog import CatalogQuery
from hypatia.query import And, Eq, Any, Lt, Or, Gt
from pyramid.events import subscriber
from zope.component.interfaces import ISite
from zope.lifecycleevent.interfaces import IObjectAddedEvent

from pyams_catalog.query import CatalogResultSet
from pyams_content.shared.alert.interfaces import ALERT_CONTENT_TYPE, IAlertManager
from pyams_content.shared.common.manager import SharedTool
from pyams_sequence.interfaces import ISequentialIdInfo
from pyams_utils.factory import factory_config
from pyams_utils.registry import get_utility
from pyams_utils.request import check_request
from pyams_utils.timezone import tztime
from pyams_utils.traversing import get_parent
from pyams_workflow.interfaces import IWorkflow


@factory_config(IAlertManager)
class AlertManager(SharedTool):
    """Alert manager class"""

    shared_content_type = ALERT_CONTENT_TYPE
    shared_content_menu = False

    def find_context_alerts(self, context=None, request=None):
        """Find alerts matching given params"""
        if request is None:
            request = check_request()
        if context is None:
            context = request.context
        sequence_info = ISequentialIdInfo(context, None)
        if sequence_info is None:
            return
        now = tztime(datetime.now(timezone.utc))
        catalog = get_utility(ICatalog)
        workflow = IWorkflow(self)
        params = And(Eq(catalog['content_type'], self.shared_content_type),
                     Eq(catalog['link_references'], sequence_info.hex_oid),
                     Any(catalog['workflow_state'], workflow.published_states),
                     Lt(catalog['effective_date'], now),
                     Or(Gt(catalog['push_end_date'], now),
                        Eq(catalog['push_end_date'], None)))
        yield from CatalogResultSet(CatalogQuery(catalog).query(params))


@subscriber(IObjectAddedEvent, context_selector=IAlertManager)
def handle_added_alert_manager(event):
    """Register alert manager when added"""
    site = get_parent(event.newParent, ISite)
    registry = site.getSiteManager()
    if registry is not None:
        registry.registerUtility(event.object, IAlertManager)
