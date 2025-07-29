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

"""PyAMS_content.root.configuration module

"""

import logging

from persistent import Persistent
from pyramid.path import DottedNameResolver
from zope.container.contained import Contained
from zope.lifecycleevent import ObjectCreatedEvent
from zope.schema.fieldproperty import FieldProperty

from pyams_content.reference import IReferenceManager
from pyams_content.root import ISiteRootToolsConfiguration, SITE_ROOT_TOOLS_CONFIGURATION_KEY
from pyams_content.shared.common.interfaces import ISharedToolContainer
from pyams_site.interfaces import ISiteRoot
from pyams_utils.adapter import adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config, get_object_factory
from pyams_utils.interfaces import MISSING_INFO

__docformat__ = 'restructuredtext'


LOGGER = logging.getLogger('PyAMS (content)')


@factory_config(ISiteRootToolsConfiguration)
class SiteRootToolsConfiguration(Persistent, Contained):
    """Site root tools configuration"""

    tables_manager_name = FieldProperty(ISiteRootToolsConfiguration['tables_manager_name'])
    tables_names = FieldProperty(ISiteRootToolsConfiguration['tables_names'])

    tools_manager_name = FieldProperty(ISiteRootToolsConfiguration['tools_manager_name'])
    tools_names = FieldProperty(ISiteRootToolsConfiguration['tools_names'])

    def get_tables_manager(self):
        """Tables manager getter"""
        name = self.tables_manager_name
        if name is not None:
            return self.__parent__.get(self.tables_manager_name)
        return None

    def check_tables_manager(self, registry):
        """Tables manager checker"""
        manager = self.get_tables_manager()
        if manager is None:
            settings = registry.settings
            factory = settings.get('pyams_content.config.references_manager_factory')
            if factory is not None:
                factory = DottedNameResolver().resolve(factory)
            if factory is None:
                factory = get_object_factory(IReferenceManager)
            if factory is not None:
                manager = factory()
            if manager is not None:
                self.tables_manager_name = name = \
                    settings.get('pyams_content.config.references_manager_name', 'references')
                self.__parent__[name] = manager
                self.tables_names = {}
        return manager

    def check_table(self, interface, table_name, registry):
        """Reference table checker"""
        table = None
        manager = self.check_tables_manager(registry)
        name = self.tables_names.get(interface)
        if name is not None:
            table = manager.get(name)
            if table is not None:
                return table
        factory = registry.settings.get(f'pyams_content.config.{table_name}_table_factory')
        if factory:
            if factory.lower() in (MISSING_INFO, 'off', 'none', 'disabled'):
                return None
            factory = DottedNameResolver().resolve(factory)
        if factory is None:
            factory = get_object_factory(interface)
        if factory is not None:
            LOGGER.info(f'Creating table from factory {factory!r}...')
            table = factory()
            registry.notify(ObjectCreatedEvent(table))
            name = registry.settings.get(f'pyams_content.config.{table_name}_table_name',
                                         table_name)
            if name not in manager:
                manager[name] = table
            self.tables_names[interface] = name
        return table

    def get_tools_manager(self):
        """Tools manager getter"""
        name = self.tools_manager_name
        if name is not None:
            return self.__parent__.get(self.tools_manager_name)
        return None

    def check_tools_manager(self, registry):
        """Tools manager checker"""
        manager = self.get_tools_manager()
        if manager is None:
            settings = registry.settings
            factory = settings.get('pyams_content.config.tools_manager_factory')
            if factory is not None:
                factory = DottedNameResolver().resolve(factory)
            if factory is None:
                factory = get_object_factory(ISharedToolContainer)
            if factory is not None:
                manager = factory()
            if manager is not None:
                self.tools_manager_name = name = \
                    settings.get('pyams_content.config.tools_manager_name', 'tools')
                self.__parent__[name] = manager
                self.tools_names = {}
        return manager

    def check_tool(self, interface, tool_name, registry):
        """Shared tool checker"""
        tool = None
        manager = self.check_tools_manager(registry)
        name = self.tools_names.get(interface)
        if name is not None:
            tool = manager.get(name)
            if tool is not None:
                return tool
        name = registry.settings.get(f'pyams_content.config.{tool_name}_tool_name',
                                     tool_name)
        if name in manager:
            tool = manager.get(name)
            if interface.providedBy(tool):
                self.tools_names[interface] = name
                return tool
        factory = registry.settings.get(f'pyams_content.config.{tool_name}_tool_factory')
        if factory:
            if factory.lower() in (MISSING_INFO, 'off', 'none', 'disabled'):
                return None
            factory = DottedNameResolver().resolve(factory)
        if factory is None:
            factory = get_object_factory(interface)
        if factory is not None:
            LOGGER.info(f'Creating shared tool from factory {factory!r}...')
            tool = factory()
            registry.notify(ObjectCreatedEvent(tool))
            manager[name] = tool
            self.tools_names[interface] = name
        return tool


@adapter_config(required=ISiteRoot,
                provides=ISiteRootToolsConfiguration)
def site_root_tools_configuration_adapter(context):
    """Site root tools configuration adapter"""
    return get_annotation_adapter(context, SITE_ROOT_TOOLS_CONFIGURATION_KEY,
                                  ISiteRootToolsConfiguration)
