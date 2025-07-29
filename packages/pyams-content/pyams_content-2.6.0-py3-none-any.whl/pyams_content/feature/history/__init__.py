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

"""PyAMS_content.feature.history module

This module provides persistent classes for history management.

History can be used to store state of any object implementing IHistoryTarget
interface; it is generally used before object updates, to store current state.
A comment can be associated to each history item, as well as a copy of any
email message which could has been sent during the operation.
"""

from datetime import datetime, timezone

from persistent import Persistent
from zope.container.btree import BTreeContainer
from zope.container.contained import Contained
from zope.copy import copy
from zope.schema.fieldproperty import FieldProperty

from pyams_content.feature.history.interfaces import HISTORY_CONTAINER_KEY, IHistoryContainer, IHistoryItem, \
    IHistoryTarget
from pyams_utils.adapter import adapter_config, get_annotation_adapter
from pyams_utils.factory import create_object, factory_config
from pyams_utils.timezone import gmtime, tztime

__docformat__ = 'restructuredtext'


@factory_config(IHistoryItem)
class HistoryItem(Persistent, Contained):
    """History item"""

    _timestamp = FieldProperty(IHistoryItem['timestamp'])
    principal = FieldProperty(IHistoryItem['principal'])
    message = FieldProperty(IHistoryItem['message'])
    comment = FieldProperty(IHistoryItem['comment'])
    _value = FieldProperty(IHistoryItem['value'])

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = gmtime(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = copy(value)


@factory_config(IHistoryContainer)
class HistoryContainer(BTreeContainer):
    """History container"""

    def add_history(self, context, comment=None, message=None, request=None):
        """Add context history"""
        item = create_object(IHistoryItem)
        if item is not None:
            item.timestamp = tztime(datetime.now(timezone.utc))
            if request is not None:
                item.principal = request.principal.id
            item.message = message
            item.comment = comment
            item.value = context
            self[str(item.timestamp.timestamp())] = item


@adapter_config(required=IHistoryTarget,
                provides=IHistoryContainer)
def history_target_container(context):
    """History target container"""
    return get_annotation_adapter(context, HISTORY_CONTAINER_KEY, IHistoryContainer)
