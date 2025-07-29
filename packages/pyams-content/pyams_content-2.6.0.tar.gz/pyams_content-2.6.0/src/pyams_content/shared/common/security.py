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

"""PyAMS_content.shared.common.security module

This module defines common security rules used by all shared tools.
"""

from zope.interface import implementer
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_content.shared.common import IWfSharedContent
from pyams_content.shared.common.interfaces import CONTENT_MANAGER_CONTRIBUTORS, CONTENT_MANAGER_ROLES, \
    IBaseSharedTool, ISharedToolRoles, IWfSharedContentRoles, SHARED_CONTENT_ROLES
from pyams_security.interfaces import IRolesPolicy
from pyams_security.property import RolePrincipalsFieldProperty
from pyams_security.security import ProtectedObjectRoles
from pyams_security.utility import get_principal
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.vocabulary import vocabulary_config

__docformat__ = 'restructuredtext'


@implementer(ISharedToolRoles)
class SharedToolRoles(ProtectedObjectRoles):
    """Shared tool roles"""

    webmasters = RolePrincipalsFieldProperty(ISharedToolRoles['webmasters'])
    pilots = RolePrincipalsFieldProperty(ISharedToolRoles['pilots'])
    managers = RolePrincipalsFieldProperty(ISharedToolRoles['managers'])
    contributors = RolePrincipalsFieldProperty(ISharedToolRoles['contributors'])
    designers = RolePrincipalsFieldProperty(ISharedToolRoles['designers'])


@adapter_config(required=IBaseSharedTool,
                provides=ISharedToolRoles)
def shared_tool_roles_adapter(context):
    """Shared tool roles adapter"""
    return SharedToolRoles(context)


@adapter_config(name=CONTENT_MANAGER_ROLES,
                required=IBaseSharedTool,
                provides=IRolesPolicy)
class SharedToolRolesPolicy(ContextAdapter):
    """Shared tool roles policy"""

    roles_interface = ISharedToolRoles
    weight = 10


@implementer(IWfSharedContentRoles)
class WfSharedContentRoles(ProtectedObjectRoles):
    """Shared content roles"""

    owner = RolePrincipalsFieldProperty(IWfSharedContentRoles['owner'])
    managers = RolePrincipalsFieldProperty(IWfSharedContentRoles['managers'])
    contributors = RolePrincipalsFieldProperty(IWfSharedContentRoles['contributors'])
    designers = RolePrincipalsFieldProperty(IWfSharedContentRoles['designers'])
    readers = RolePrincipalsFieldProperty(IWfSharedContentRoles['readers'])
    guests = RolePrincipalsFieldProperty(IWfSharedContentRoles['guests'])


@adapter_config(required=IWfSharedContent,
                provides=IWfSharedContentRoles)
def shared_content_roles_adapter(context):
    """Shared content roles adapter"""
    return WfSharedContentRoles(context)


@adapter_config(name=SHARED_CONTENT_ROLES,
                required=IWfSharedContent,
                provides=IRolesPolicy)
class SharedContentRolesPolicy(ContextAdapter):
    """Shared content roles policy"""

    roles_interface = IWfSharedContentRoles
    weight = 10


@vocabulary_config(name=CONTENT_MANAGER_CONTRIBUTORS)
class SharedToolContributorsVocabulary(SimpleVocabulary):
    """Shared tool contributors vocabulary"""

    def __init__(self, context):
        roles = ISharedToolRoles(context, None)
        terms = []
        for principal_id in roles.contributors or set():
            principal = get_principal(None, principal_id)
            if principal is not None:
                terms.append(SimpleTerm(principal.id, title=principal.title))
        super().__init__(terms)
