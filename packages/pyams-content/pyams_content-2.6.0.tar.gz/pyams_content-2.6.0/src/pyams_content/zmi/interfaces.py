#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.zmi.interfaces module

Common management interfaces.
"""

from pyramid.interfaces import IView
from zope.interface import Interface


__docformat__ = 'restructuredtext'


class IDashboardView(IView):
    """Dashboard view marker interface"""


class IDashboardTable(Interface):
    """Dashboard table marker interface"""


class IDashboardColumn(Interface):
    """Dashboard column marker interface"""


class IDashboardContentVisibility(Interface):
    """Dashboard content visibility column provider interface

    Adapters to this interface should return a tuple containing a
    boolean value to specify if the generated action icon should be
    active to switch item visibility, and a string containing the
    icon HTML definition.
    """


class IDashboardContentLabel(Interface):
    """Dashboard content label column provider interface"""


class IDashboardContentType(Interface):
    """Dashboard content type column provider interface"""


class ISiteRootDashboardContentType(IDashboardContentType):
    """Site root dashboard content type column provider interface"""


class IDashboardContentNumber(Interface):
    """Dashboard content reference number column provider interface"""


class IDashboardContentStatus(Interface):
    """Dashboard content status column provider interface"""


class IDashboardContentStatusDatetime(Interface):
    """Dashboard content status datetime provider interface"""


class IDashboardContentVersion(Interface):
    """Dashboard content version column provider interface"""


class IDashboardContentModifier(Interface):
    """Dashboard content modifier column provider interface"""


class IDashboardContentOwner(Interface):
    """Dashboard content owner column provider interface"""


class IDashboardContentTimestamp(Interface):
    """Dashboard content modification timestamp column provider interface"""


class IMyDashboardMenu(Interface):
    """My dashboard menu marker interface"""


class IAllDashboardMenu(Interface):
    """General dashboard menu"""
