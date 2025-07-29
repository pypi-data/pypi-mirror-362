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

"""PyAMS_content.feature.navigation.zmi module

This module defines navigation management components interfaces.
"""

from zope.interface import Interface

from pyams_content.component.association.zmi import IAssociationsTable
from pyams_content.component.association.zmi.interfaces import IAssociationsContainerEditForm, \
    IAssociationsView


__docformat__ = 'restructuredtext'


class IMenuLinksView(IAssociationsView):
    """Menu links view marker interface"""


class IMenuLinksTable(IAssociationsTable):
    """Menu links table marker interface"""


class IMenuLinksContainerEditForm(IAssociationsContainerEditForm):
    """Menu links container edit form marker interface"""


class IMenusView(Interface):
    """Menus view marker interface"""


class IMenusTable(Interface):
    """Menus table marker interface"""


class IMenusContainerEditForm(Interface):
    """Menus container edit form marker interface"""


class IMenuAddForm(Interface):
    """Menu add form marker interface"""


class IMenuEditForm(Interface):
    """Menu edit form marker interface"""
