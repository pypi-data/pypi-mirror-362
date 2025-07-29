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

"""PyAMS_content.shared.alert.type module

"""

from persistent import Persistent
from zope.container.contained import Contained
from zope.container.ordered import OrderedContainer
from zope.location.interfaces import ISublocations
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.traversing.interfaces import ITraversable

from pyams_content.interfaces import MANAGE_TOOL_PERMISSION
from pyams_content.reference.pictogram import IPictogramTable
from pyams_content.shared.alert import IAlertManager, IAlertTypesManager
from pyams_content.shared.alert.interfaces import ALERT_TYPES_MANAGER_ANNOTATION_KEY, ALERT_TYPES_VOCABULARY, IAlertType
from pyams_i18n.interfaces import II18n
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_utils.adapter import ContextAdapter, adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.registry import query_utility
from pyams_utils.request import check_request
from pyams_utils.traversing import get_parent
from pyams_utils.vocabulary import vocabulary_config

__docformat__ = 'restructuredtext'


@factory_config(IAlertType)
class AlertType(Persistent, Contained):
    """Alert type persistent class"""

    visible = FieldProperty(IAlertType['visible'])
    dashboard_label = FieldProperty(IAlertType['dashboard_label'])
    pictogram = FieldProperty(IAlertType['pictogram'])
    color = FieldProperty(IAlertType['color'])

    def get_pictogram(self):
        table = query_utility(IPictogramTable)
        return table.get(self.pictogram) if table is not None else None


@adapter_config(required=IAlertType,
                provides=IViewContextPermissionChecker)
class AlertTypePermissionChecker(ContextAdapter):
    """Alert type permission checker"""

    edit_permission = MANAGE_TOOL_PERMISSION


@factory_config(IAlertTypesManager)
class AlertTypesManager(OrderedContainer):
    """Alert types manager"""

    def get_visible_items(self):
        """Visible alert types iterator"""
        yield from filter(lambda x: x.visible, self.values())


@adapter_config(required=IAlertManager,
                provides=IAlertTypesManager)
def alerts_types_manager(context):
    """Alerts types manager adapter"""
    return get_annotation_adapter(context, ALERT_TYPES_MANAGER_ANNOTATION_KEY, IAlertTypesManager,
                                  name='++types++')


@adapter_config(name='types',
                required=IAlertManager,
                provides=ITraversable)
class AlertsManagerTypesNamespace(ContextAdapter):
    """Alerts manager types ++gravity++ namespace"""

    def traverse(self, name, furtherpath=None):
        return IAlertTypesManager(self.context)


@adapter_config(name='types',
                required=IAlertManager,
                provides=ISublocations)
class AlertsManagerTypesSublocations(ContextAdapter):
    """Alerts manager types sub-locations adapter"""

    def sublocations(self):
        return IAlertTypesManager(self.context).values()


@vocabulary_config(name=ALERT_TYPES_VOCABULARY)
class AlertTypesVocabulary(SimpleVocabulary):
    """Alert types vocabulary"""

    def __init__(self, context):
        terms = []
        parent = get_parent(context, IAlertManager)
        if parent is not None:
            request = check_request()
            manager = IAlertTypesManager(parent)
            terms = [
                SimpleTerm(alert_type.__name__,
                           title=II18n(alert_type).query_attribute('label', request=request))
                for alert_type in manager.values()
            ]
        super().__init__(terms)
