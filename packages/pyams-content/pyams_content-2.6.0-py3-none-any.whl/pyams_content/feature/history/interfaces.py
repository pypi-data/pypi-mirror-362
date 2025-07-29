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

"""PyAMS_content.feature.history.interfaces module

This module is used to define interfaces of history items which can be attached to
an object; these items are tagged with a timestamp and contain copies of original
object before its updates, along with messages and internal comments.
"""

from zope.annotation.interfaces import IAttributeAnnotatable
from zope.container.constraints import contains
from zope.container.interfaces import IContainer
from zope.interface import Interface
from zope.schema import Datetime, Object, Text

from pyams_security.schema import PrincipalField
from pyams_utils.schema import HTMLField

__docformat__ = 'restructuredtext'

from pyams_content import _


class IHistoryTarget(IAttributeAnnotatable):
    """History target marker interface"""


class IHistoryItem(Interface):
    """History item interface"""

    timestamp = Datetime(title=_("Timestamp"),
                         description=_("Date and time at which history item was created"))

    principal = PrincipalField(title=_("Principal"),
                               description=_("Name of history action principal"),
                               required=True)

    message = HTMLField(title=_("HTML message"),
                        description=_("HTML message which was sent to a principal"),
                        required=False)

    comment = Text(title=_("Internal comment"),
                   required=False)

    value = Object(title=_("History item value"),
                   schema=IHistoryTarget)


HISTORY_CONTAINER_KEY = 'pyams_content.history'


class IHistoryContainer(IContainer):
    """History container interface"""

    contains(IHistoryItem)

    def add_history(self, context, comment=None, message=None, request=None):
        """Add copy of context to history"""
