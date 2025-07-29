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

"""PyAMS_content.reference module

"""

from persistent import Persistent
from pyramid.events import subscriber
from zope.component.interfaces import ISite
from zope.container.contained import Contained
from zope.container.folder import Folder
from zope.interface import implementer
from zope.lifecycleevent import IObjectAddedEvent
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_content.interfaces import MANAGE_REFERENCE_TABLE_PERMISSION
from pyams_content.reference.interfaces import IReferenceInfo, IReferenceManager, IReferenceTable, IReferenceTableRoles, \
    REFERENCE_TABLE_ROLES
from pyams_i18n.interfaces import II18n, II18nManager
from pyams_security.interfaces import IDefaultProtectionPolicy, IRolesPolicy, IViewContextPermissionChecker
from pyams_security.property import RolePrincipalsFieldProperty
from pyams_security.security import ProtectedObjectMixin, ProtectedObjectRoles
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.factory import factory_config
from pyams_utils.registry import query_utility
from pyams_utils.request import check_request
from pyams_utils.traversing import get_parent

__docformat__ = 'restructuredtext'


@factory_config(IReferenceManager)
class ReferencesManager(Folder):
    """References tables container"""

    title = FieldProperty(IReferenceManager['title'])
    short_name = FieldProperty(IReferenceManager['short_name'])

    def __init__(self):
        super().__init__()
        self.title = {
            'en': 'References tables',
            'fr': 'Tables de références'
        }
        self.short_name = self.title.copy()


@subscriber(IObjectAddedEvent, context_selector=IReferenceManager)
def handle_added_references_manager(event):
    """Handle new references manager"""
    site = get_parent(event.object, ISite)
    registry = site.getSiteManager()
    if registry is not None:
        registry.registerUtility(event.object, IReferenceManager)


@implementer(IDefaultProtectionPolicy, IReferenceTable, II18nManager)
class ReferenceTable(ProtectedObjectMixin, Folder):
    """References table"""

    title = FieldProperty(IReferenceTable['title'])
    short_name = FieldProperty(IReferenceTable['short_name'])

    languages = FieldProperty(II18nManager['languages'])


@implementer(IReferenceTableRoles)
class ReferenceTableRoles(ProtectedObjectRoles):
    """References table roles"""

    managers = RolePrincipalsFieldProperty(IReferenceTableRoles['managers'])


@adapter_config(required=IReferenceTable,
                provides=IReferenceTableRoles)
def reference_table_roles(context):
    """References table roles adapter"""
    return ReferenceTableRoles(context)


@adapter_config(name=REFERENCE_TABLE_ROLES,
                required=IReferenceTable,
                provides=IRolesPolicy)
class ReferenceTableRolesPolicy(ContextAdapter):
    """References table roles policy"""

    roles_interface = IReferenceTableRoles
    weight = 10


@implementer(IReferenceInfo)
class ReferenceInfo(Persistent, Contained):
    """Reference record"""

    title = FieldProperty(IReferenceInfo['title'])
    short_name = FieldProperty(IReferenceInfo['short_name'])


@adapter_config(required=IReferenceInfo,
                provides=IViewContextPermissionChecker)
class ReferenceInfoPermissionChecker(ContextAdapter):
    """Reference info permission checker"""

    edit_permission = MANAGE_REFERENCE_TABLE_PERMISSION


class ReferencesVocabulary(SimpleVocabulary):
    """Base references vocabulary"""

    table_interface = None

    def __init__(self, context=None):
        table = query_utility(self.table_interface)
        if table is not None:
            request = check_request()
            terms = sorted([
                SimpleTerm(v.__name__,
                           title=II18n(v).query_attribute('title', request=request))
                for v in table.values()
            ], key=lambda t: t.title)
        else:
            terms = []
        super().__init__(terms)
