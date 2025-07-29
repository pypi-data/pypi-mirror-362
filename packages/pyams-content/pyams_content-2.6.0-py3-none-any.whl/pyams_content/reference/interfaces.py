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

"""PyAMS_content.reference.interfaces module

"""

from zope.container.constraints import containers, contains
from zope.container.interfaces import IContainer
from zope.interface import Interface

from pyams_content.interfaces import IBaseContent, REFERENCE_MANAGER_ROLE
from pyams_security.schema import PrincipalsSetField

__docformat__ = 'restructuredtext'

from pyams_content import _


class IReferenceInfo(IBaseContent):
    """Base reference interface"""

    containers('.IReferenceTable')


class IReferenceTable(IBaseContent):
    """Reference table interface"""

    containers('.IReferenceTableContainer')
    contains(IReferenceInfo)


REFERENCE_TABLE_ROLES = 'pyams_content.reference.roles'


class IReferenceTableRoles(Interface):
    """Reference table roles interface"""

    managers = PrincipalsSetField(title=_("Table managers"),
                                  description=_("Table managers can handle all table contents"),
                                  role_id=REFERENCE_MANAGER_ROLE,
                                  required=False)


class IReferenceManager(IBaseContent, IContainer):
    """References tables container"""

    contains(IReferenceTable)
