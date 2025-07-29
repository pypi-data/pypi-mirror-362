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

"""PyAMS_content.shared.common.restrictions module

This modules defines components which are used to handle contributors and managers
*restrictions*. These restrictions are rules which can be defined and extended using
adapters to define access rules.
"""

from persistent import Persistent
from pyramid.events import subscriber
from zope.container.contained import Contained
from zope.container.folder import Folder
from zope.interface import alsoProvides
from zope.schema.fieldproperty import FieldProperty

from pyams_content.interfaces import CONTRIBUTOR_ROLE, MANAGER_ROLE
from pyams_content.shared.common import IBaseSharedTool, ISharedContent, IWfSharedContent
from pyams_content.shared.common.interfaces import CONTRIBUTORS_RESTRICTIONS_KEY, \
    CONTRIBUTOR_WORKFLOW_RESTRICTIONS_KEY, IContributorRestrictions, \
    IContributorWorkflowRestrictions, IManagerRestrictions, IManagerWorkflowRestrictions, \
    IPrincipalRestrictions, IRestrictionInfo, ISharedToolRestrictions, IWfSharedContentRoles, \
    MANAGERS_RESTRICTIONS_KEY, MANAGER_WORKFLOW_RESTRICTIONS_KEY
from pyams_security.interfaces import IGrantedRoleEvent, IRevokedRoleEvent
from pyams_security.interfaces.base import IPrincipalInfo
from pyams_utils.adapter import adapter_config, get_adapter_weight, get_annotation_adapter
from pyams_utils.factory import factory_config, get_object_factory
from pyams_utils.request import check_request
from pyams_utils.traversing import get_parent


__docformat__ = 'restructuredtext'


@factory_config(IPrincipalRestrictions)
class PrincipalRestrictionInfo(Persistent, Contained):
    """Principal restriction info"""

    principal_id = FieldProperty(IPrincipalRestrictions['principal_id'])

    def __init__(self, principal_id):
        self.principal_id = principal_id


@factory_config(provided=ISharedToolRestrictions)
class SharedToolRestrictions(Folder):
    """Shared tool restrictions persistent class"""

    def new_restrictions(self, principal, interface=None):
        """New principal restrictions factory"""
        if IPrincipalInfo.providedBy(principal):
            principal = principal.id
        factory = get_object_factory(IPrincipalRestrictions)
        restrictions = factory(principal)
        if interface is not None:
            alsoProvides(restrictions, interface)
        return restrictions

    def set_restrictions(self, principal, restrictions=None, interface=None):
        """Set new restrictions for given principal"""
        if IPrincipalInfo.providedBy(principal):
            principal = principal.id
        if principal not in self:
            if restrictions is None:
                restrictions = self.new_restrictions(principal, interface)
            self[principal] = restrictions

    def get_restrictions(self, principal, create_if_none=False):
        """Principal restrictions getter"""
        if IPrincipalInfo.providedBy(principal):
            principal = principal.id
        restrictions = self.get(principal)
        if (restrictions is None) and create_if_none:
            restrictions = self.new_restrictions(principal)
            self.set_restrictions(principal, restrictions)
        return restrictions

    def drop_restrictions(self, principal):
        """Drop restrictions for given principal"""
        if IPrincipalInfo.providedBy(principal):
            principal = principal.id
        if principal in self:
            del self[principal]

    def can_access(self, context, permission, request=None):
        """Principal access checker"""
        if request is None:
            request = check_request()
        if permission and not request.has_permission(permission, context=context):
            return False
        restrictions = self.get_restrictions(request.principal, create_if_none=False)
        if restrictions:
            for _name, adapter in sorted(request.registry.getAdapters((restrictions,),
                                                                      IRestrictionInfo),
                                         key=get_adapter_weight):
                if adapter.can_access(context, permission, request):
                    return True
        return False


#
# Contributor restrictions
#

@adapter_config(required=IBaseSharedTool,
                provides=IContributorRestrictions)
def shared_tool_contributor_restrictions(context):
    """Shared tool contributor restrictions"""
    return get_annotation_adapter(context, CONTRIBUTORS_RESTRICTIONS_KEY,
                                  ISharedToolRestrictions)


@factory_config(IContributorWorkflowRestrictions)
class ContributorWorkflowRestrictions(Persistent):
    """Contributor workflow restrictions"""

    weight = 10

    show_workflow_warning = FieldProperty(
        IContributorWorkflowRestrictions['show_workflow_warning'])
    owners = FieldProperty(IContributorWorkflowRestrictions['owners'])

    def can_access(self, context, permission, request):  # pylint: disable=unused-argument
        """Access checker"""
        roles = IWfSharedContentRoles(context, None)
        if roles is None:
            return False
        return bool(roles.owner & set(self.owners or ()))


@adapter_config(name='workflow',
                required=IContributorRestrictions,
                provides=IRestrictionInfo)
@adapter_config(required=IPrincipalRestrictions,
                provides=IContributorWorkflowRestrictions)
def contributor_workflow_restrictions_adapter(context):
    """Base contributor restrictions adapter"""
    return get_annotation_adapter(context, CONTRIBUTOR_WORKFLOW_RESTRICTIONS_KEY,
                                  IContributorWorkflowRestrictions)


@adapter_config(required=ISharedContent,
                provides=IContributorRestrictions)
@adapter_config(required=IWfSharedContent,
                provides=IContributorRestrictions)
def shared_content_contributor_restrictions(context):
    """Shared tool contributor restrictions"""
    tool = get_parent(context, IBaseSharedTool)
    if tool is not None:
        return IContributorRestrictions(tool)
    return None


@subscriber(IGrantedRoleEvent, role_selector=CONTRIBUTOR_ROLE)
def handle_added_contributor_role(event):
    """Handle added contributor role"""
    restrictions = IContributorRestrictions(event.object.__parent__, None)
    if restrictions is not None:
        restrictions.set_restrictions(event.principal_id, interface=IContributorRestrictions)


@subscriber(IRevokedRoleEvent, role_selector=CONTRIBUTOR_ROLE)
def handle_revoked_contributor_role(event):
    """Handle revoked contributor role"""
    restrictions = IContributorRestrictions(event.object.__parent__, None)
    if restrictions is not None:
        restrictions.drop_restrictions(event.principal_id)


#
# Manager restrictions
#

@adapter_config(required=IBaseSharedTool,
                provides=IManagerRestrictions)
def shared_tool_manager_restrictions(context):
    """Shared tool manager restrictions"""
    return get_annotation_adapter(context, MANAGERS_RESTRICTIONS_KEY,
                                  ISharedToolRestrictions)


@factory_config(IManagerWorkflowRestrictions)
class ManagerWorkflowRestrictions(Persistent):
    """Manager workflow restrictions"""

    weight = 10

    show_workflow_warning = FieldProperty(IManagerWorkflowRestrictions['show_workflow_warning'])
    restricted_contents = FieldProperty(IManagerWorkflowRestrictions['restricted_contents'])
    owners = FieldProperty(IManagerWorkflowRestrictions['owners'])

    def can_access(self, context, permission, request):
        """Access checker"""
        if not self.restricted_contents:
            return True
        roles = IWfSharedContentRoles(context, None)
        if roles is None:
            return False
        return bool(roles.owner & set(self.owners or ()))


@adapter_config(name='workflow',
                required=IManagerRestrictions,
                provides=IRestrictionInfo)
@adapter_config(required=IManagerRestrictions,
                provides=IManagerWorkflowRestrictions)
def manager_workflow_restrictions_adapter(context):
    """Manager workflow restrictions adapter"""
    return get_annotation_adapter(context, MANAGER_WORKFLOW_RESTRICTIONS_KEY,
                                  IManagerWorkflowRestrictions)


@adapter_config(required=ISharedContent,
                provides=IManagerRestrictions)
@adapter_config(required=IWfSharedContent,
                provides=IManagerRestrictions)
def shared_content_manager_restrictions(context):
    """Shared content manager restrictions"""
    tool = get_parent(context, IBaseSharedTool)
    if tool is not None:
        return IManagerRestrictions(tool)
    return None


@subscriber(IGrantedRoleEvent, role_selector=MANAGER_ROLE)
def handle_added_manager_role(event):
    """Handle added manager role"""
    restrictions = IManagerRestrictions(event.object.__parent__, None)
    if restrictions is not None:
        restrictions.set_restrictions(event.principal_id, interface=IManagerRestrictions)


@subscriber(IRevokedRoleEvent, role_selector=MANAGER_ROLE)
def handle_revoked_manager_role(event):
    """Handle revoked manager role"""
    restrictions = IManagerRestrictions(event.object.__parent__, None)
    if restrictions is not None:
        restrictions.drop_restrictions(event.principal_id)
