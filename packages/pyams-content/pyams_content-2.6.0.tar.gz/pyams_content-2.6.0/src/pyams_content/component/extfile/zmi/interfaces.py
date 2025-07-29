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

"""PyAMS_content.component.extfile.zmi.interfaces module

This module provides private interfaces used by external files management components.
"""

from pyams_content.component.association.zmi import IAssociationItemAddForm, \
    IAssociationItemEditForm


__docformat__ = 'restructuredtext'


class IExtFileAddForm(IAssociationItemAddForm):
    """External file add form marker interface"""


class IExtFileEditForm(IAssociationItemEditForm):
    """External file edit form marker interface"""
