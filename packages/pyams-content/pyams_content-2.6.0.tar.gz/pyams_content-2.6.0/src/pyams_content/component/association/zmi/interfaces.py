#
# Copyright (c) 2015-2022 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.component.association.zmi.interfaces module

This module defines associations-related management interfaces.
"""

from zope.interface import Interface

from pyams_zmi.interfaces.form import IPropertiesEditForm


__docformat__ = 'restructuredtext'


class IAssociationsView(Interface):
    """Associations view marker interface"""


class IAssociationsTable(Interface):
    """Associations table marker interface"""


class IAssociationsContainerEditForm(Interface):
    """Associations container edit form marker interface"""


class IAssociationItemAddForm(Interface):
    """Association item add form marker interface"""


class IAssociationItemEditForm(IPropertiesEditForm):
    """Association item edit form marker interface"""
