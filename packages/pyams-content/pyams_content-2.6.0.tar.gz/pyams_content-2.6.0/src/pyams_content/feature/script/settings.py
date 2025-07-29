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

"""PyAMS_content.feature.script.settings module

Persistent classes for scripts settings management.
"""

from persistent import Persistent
from zope.container.contained import Contained
from zope.schema.fieldproperty import FieldProperty

from pyams_content.feature.script.interfaces import IScriptContainerSettings, IScriptContainerTarget, \
    SCRIPT_SETTINGS_KEY
from pyams_content.interfaces import MANAGE_SITE_ROOT_PERMISSION
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_utils.adapter import ContextAdapter, adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.zodb import volatile_property

__docformat__ = 'restructuredtext'


@factory_config(IScriptContainerSettings)
class ScriptContainerSettings(Persistent, Contained):
    """Script container settings persistent class"""

    _variables = FieldProperty(IScriptContainerSettings['variables'])
    
    @property
    def variables(self):
        return self._variables
    
    @variables.setter
    def variables(self, values):
        self._variables = values
        del self.items

    @volatile_property
    def items(self):
        """Variables mapping getter"""
        result = {}
        for line in self.variables or ():
            if (not line) or line.startswith('#'):
                continue
            key, value = line.split('=', 1)
            result[key.strip()] = value.strip()
        return result


@adapter_config(required=IScriptContainerSettings,
                provides=IViewContextPermissionChecker)
class ScriptContainerSettingsPermissionChecker(ContextAdapter):
    """Script container settings permission checker"""
    
    edit_permission = MANAGE_SITE_ROOT_PERMISSION


@adapter_config(required=IScriptContainerTarget,
                provides=IScriptContainerSettings)
def script_container_settings(context):
    """Script container settings adapter"""
    return get_annotation_adapter(context, SCRIPT_SETTINGS_KEY, 
                                  IScriptContainerSettings)
