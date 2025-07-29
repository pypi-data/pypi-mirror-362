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

"""PyAMS_content.root module

This module defines roles and permissions checker of site root.
"""

from persistent import Persistent
from pyramid.events import subscriber
from zope.container.contained import Contained
from zope.interface import Interface, implementer
from zope.schema.fieldproperty import FieldProperty
from zope.traversing.interfaces import ITraversable

from pyams_content.interfaces import MANAGE_SITE_ROOT_PERMISSION
from pyams_content.root.interfaces import ISiteRootInfos, ISiteRootRoles, \
    ISiteRootToolsConfiguration, SITEROOT_ROLES, SITE_ROOT_INFOS_KEY, \
    SITE_ROOT_TOOLS_CONFIGURATION_KEY
from pyams_file.property import FileProperty
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces import IGrantedRoleEvent, IRolesPolicy, ISecurityManager, IViewContextPermissionChecker
from pyams_security.interfaces.base import IRole
from pyams_security.interfaces.plugin import ILocalGroup
from pyams_security.property import RolePrincipalsFieldProperty
from pyams_security.security import ProtectedObjectRoles
from pyams_site.interfaces import ISiteRoot
from pyams_utils.adapter import ContextAdapter, ContextRequestViewAdapter, adapter_config, \
    get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.list import next_from
from pyams_utils.registry import get_utility

__docformat__ = 'restructuredtext'

from pyams_utils.traversing import get_parent


@factory_config(provided=ISiteRootInfos)
class SiteRootInfos(Persistent, Contained):
    """Site root information"""

    title = FieldProperty(ISiteRootInfos['title'])
    short_title = FieldProperty(ISiteRootInfos['short_title'])
    description = FieldProperty(ISiteRootInfos['description'])
    author = FieldProperty(ISiteRootInfos['author'])
    icon = FileProperty(ISiteRootInfos['icon'])
    logo = FileProperty(ISiteRootInfos['logo'])
    public_url = FieldProperty(ISiteRootInfos['public_url'])
    support_email = FieldProperty(ISiteRootInfos['support_email'])


@adapter_config(required=ISiteRoot, provides=ISiteRootInfos)
def site_root_infos_factory(context):
    """Site root information factory"""
    return get_annotation_adapter(context, SITE_ROOT_INFOS_KEY,
                                  ISiteRootInfos, name='++infos++')


@adapter_config(name='infos',
                required=ISiteRoot, provides=ITraversable)
class SiteRootInfosTraverser(ContextAdapter):
    """Site root infos traverser"""

    def traverse(self, name, furtherPath=None):
        """Namespace traverser"""
        return ISiteRootInfos(self.context)


@implementer(ISiteRootRoles)
class SiteRootRoles(ProtectedObjectRoles):
    """Site root roles"""

    webmasters = RolePrincipalsFieldProperty(ISiteRootRoles['webmasters'])
    designers = RolePrincipalsFieldProperty(ISiteRootRoles['designers'])
    operators = RolePrincipalsFieldProperty(ISiteRootRoles['operators'])

    def get_operators_group(self):
        """Get operators group"""
        if not self.operators:
            return None
        sm = get_utility(ISecurityManager)
        return sm.get_raw_principal(next_from(self.operators))


@adapter_config(required=ISiteRoot,
                provides=ISiteRootRoles)
def site_root_roles_adapter(context):
    """Site root roles adapters"""
    return SiteRootRoles(context)


@adapter_config(name=SITEROOT_ROLES,
                required=ISiteRoot,
                provides=IRolesPolicy)
class SiteRootRolesPolicy(ContextAdapter):
    """Site root roles policy"""

    roles_interface = ISiteRootRoles
    weight = 10


@adapter_config(required=(ISiteRoot, IPyAMSLayer, Interface),
                provides=IViewContextPermissionChecker)
@adapter_config(required=(ISiteRootInfos, IPyAMSLayer, Interface),
                provides=IViewContextPermissionChecker)
class SiteRootPermissionChecker(ContextRequestViewAdapter):
    """Site root permission checker"""

    edit_permission = MANAGE_SITE_ROOT_PERMISSION


@subscriber(IGrantedRoleEvent)
def handle_granted_role(event):
    """Handle granted role event"""
    role = get_utility(IRole, name=event.role_id)
    if (role is None) or not role.custom_data.get('set_as_operator', True):
        return
    root = get_parent(event.object, ISiteRoot)
    if root is None:
        return
    roles = ISiteRootRoles(root)
    group = roles.get_operators_group()
    if (group is None) or not ILocalGroup.providedBy(group):
        return
    group.principals |= {event.principal_id}
