#
# Copyright (c) 2015-2024 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.feature.script module

This module provides scripts persistent classes and adapters.
"""

from persistent import Persistent
from zope.container.contained import Contained
from zope.location.interfaces import ISublocations
from zope.schema.fieldproperty import FieldProperty
from zope.traversing.interfaces import ITraversable

from pyams_content.feature.script.interfaces import IScriptContainer, IScriptContainerTarget, IScriptInfo, \
    SCRIPT_CONTAINER_KEY
from pyams_content.interfaces import MANAGE_SITE_ROOT_PERMISSION
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_utils.adapter import ContextAdapter, adapter_config, get_annotation_adapter
from pyams_utils.container import BTreeOrderedContainer
from pyams_utils.factory import factory_config

__docformat__ = 'restructuredtext'


@factory_config(IScriptInfo)
class ScriptInfo(Persistent, Contained):
    """Script persistent class"""
    
    active = FieldProperty(IScriptInfo['active'])
    name = FieldProperty(IScriptInfo['name'])
    body = FieldProperty(IScriptInfo['body'])
    bottom_script = FieldProperty(IScriptInfo['bottom_script'])


@adapter_config(required=IScriptInfo,
                provides=IViewContextPermissionChecker)
class ScriptInfoPermissionChecker(ContextAdapter):
    """Script info permission checker"""
    
    edit_permission = MANAGE_SITE_ROOT_PERMISSION


@factory_config(IScriptContainer)
class ScriptContainer(BTreeOrderedContainer):
    """Script container persistent class"""
    
    def get_active_items(self):
        """Active items iterator"""
        yield from filter(lambda x: x.active, self.values())

    def get_top_scripts(self):
        """Get iterator over top scripts"""
        yield from filter(lambda x: not x.bottom_script, self.get_active_items())

    def get_bottom_scripts(self):
        """Get iterator over bottom scripts"""
        yield from filter(lambda x: x.bottom_script, self.get_active_items())


@adapter_config(required=IScriptContainerTarget,
                provides=IScriptContainer)
def script_container(context):
    """Script container adapter"""
    return get_annotation_adapter(context, SCRIPT_CONTAINER_KEY,
                                  IScriptContainer,
                                  name='++script++')


@adapter_config(name='script',
                required=IScriptContainerTarget,
                provides=ITraversable)
class ScriptContainerTraverser(ContextAdapter):
    """Script container traverser"""
    
    def traverse(self, name, furtherPath):
        """Traverse target to script container"""
        return IScriptContainer(self.context)
    
    
@adapter_config(name='script',
                required=IScriptContainerTarget,
                provides=ISublocations)
class ScriptContainerSublocations(ContextAdapter):
    """Script container sub-locations adapter"""
    
    def sublocations(self):
        """Sub-locations getter"""
        yield from IScriptContainer(self.context).values()
