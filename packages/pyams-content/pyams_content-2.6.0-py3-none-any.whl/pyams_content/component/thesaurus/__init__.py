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

"""PyAMS_content.component.thesaurus module

This module handles persistent classes using thesaurus based properties.
"""

from persistent import Persistent
from pyramid.events import subscriber
from pyramid.location import lineage
from zope.container.contained import Contained
from zope.interface import alsoProvides
from zope.lifecycleevent import IObjectAddedEvent, IObjectModifiedEvent, ObjectModifiedEvent
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.thesaurus.interfaces import COLLECTIONS_INFO_KEY, \
    COLLECTIONS_MANAGER_KEY, ICollectionsInfo, ICollectionsManager, ICollectionsManagerTarget, \
    ICollectionsTarget, ITagsInfo, ITagsManager, ITagsManagerTarget, ITagsTarget, IThemesInfo, \
    IThemesManager, IThemesManagerTarget, IThemesTarget, TAGS_INFO_KEY, TAGS_MANAGER_KEY, \
    THEMES_INFO_KEY, THEMES_MANAGER_KEY
from pyams_content.shared.site.interfaces import ISiteFolder
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_security.permission import get_edit_permission
from pyams_thesaurus.interfaces.thesaurus import IThesaurus
from pyams_utils.adapter import ContextAdapter, adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.inherit import BaseInheritInfo, InheritedFieldProperty
from pyams_utils.registry import get_pyramid_registry, query_utility
from pyams_utils.request import query_request
from pyams_utils.traversing import get_parent


__docformat__ = 'restructuredtext'


@adapter_config(required=ITagsInfo,
                provides=IViewContextPermissionChecker)
@adapter_config(required=IThemesInfo,
                provides=IViewContextPermissionChecker)
@adapter_config(required=ICollectionsInfo,
                provides=IViewContextPermissionChecker)
class TagsInfoPermissionChecker(ContextAdapter):
    """Tags info permission checker"""

    @property
    def edit_permission(self):
        """Tags info edit permission getter"""
        request = query_request()
        for index, parent in enumerate(lineage(self.context)):
            if index == 0:
                continue
            permission = get_edit_permission(request, parent)
            if permission is not None:
                return permission
        return None


#
# Tags management
#

@factory_config(ITagsManager)
class TagsManager(Persistent, Contained):
    """Tags manager persistent class"""

    thesaurus_name = FieldProperty(ITagsManager['thesaurus_name'])
    extract_name = FieldProperty(ITagsManager['extract_name'])

    enable_glossary = FieldProperty(ITagsManager['enable_glossary'])
    glossary_thesaurus_name = FieldProperty(ITagsManager['glossary_thesaurus_name'])

    @property
    def glossary(self):
        """Glossary getter"""
        if not self.enable_glossary:
            return None
        return query_utility(IThesaurus, name=self.glossary_thesaurus_name)


@adapter_config(required=ITagsManagerTarget,
                provides=ITagsManager)
def tags_manager_factory(target):
    """Tags manager factory"""
    return get_annotation_adapter(target, TAGS_MANAGER_KEY, ITagsManager,
                                  name='++tags-manager++')


@factory_config(ITagsInfo)
class TagsInfo(Persistent, Contained):
    """Tags info persistent class"""

    tags = FieldProperty(ITagsInfo['tags'])


@adapter_config(required=ITagsTarget,
                provides=ITagsInfo)
def tags_info_factory(target):
    """Tags info factory"""
    return get_annotation_adapter(target, TAGS_INFO_KEY, ITagsInfo,
                                  name='++tags++')


@subscriber(IObjectModifiedEvent, context_selector=ITagsInfo)
def handle_modified_tags_info(event):
    """Handle modified tags info"""
    target = get_parent(event.object, ITagsTarget)
    if target is not None:
        registry = get_pyramid_registry()
        registry.notify(ObjectModifiedEvent(target))


#
# Themes management
#

@factory_config(IThemesManager)
class ThemesManager(Persistent, Contained):
    """Themes manager persistent class"""

    thesaurus_name = FieldProperty(IThemesManager['thesaurus_name'])
    extract_name = FieldProperty(IThemesManager['extract_name'])


@adapter_config(required=IThemesManagerTarget,
                provides=IThemesManager)
def themes_manager_factory(target):
    """Themes manager factory"""
    return get_annotation_adapter(target, THEMES_MANAGER_KEY, IThemesManager,
                                  name='++themes-manager++')


@factory_config(IThemesInfo)
class ThemesInfo(BaseInheritInfo, Persistent, Contained):
    """Themes info persistent class"""

    adapted_interface = IThemesInfo
    target_interface = IThemesTarget

    _themes = FieldProperty(IThemesInfo['themes'])
    themes = InheritedFieldProperty(IThemesInfo['themes'])


@adapter_config(required=IThemesTarget,
                provides=IThemesInfo)
def themes_info_factory(target):
    """Themes info factory"""
    return get_annotation_adapter(target, THEMES_INFO_KEY, IThemesInfo,
                                  name='++themes++')


@subscriber(IObjectAddedEvent, context_selector=ISiteFolder, parent_selector=IThemesTarget)
def handle_added_site_folder(event):
    """Handle site folder when added to a themes target"""
    alsoProvides(event.object, IThemesTarget)


@subscriber(IObjectModifiedEvent, context_selector=IThemesInfo)
def handle_modified_themes_info(event):
    """Handle modified themes info"""
    target = get_parent(event.object, IThemesTarget)
    if target is not None:
        registry = get_pyramid_registry()
        registry.notify(ObjectModifiedEvent(target))


#
# Collections management
#

@factory_config(ICollectionsManager)
class CollectionsManager(Persistent, Contained):
    """Collections manager persistent class"""

    thesaurus_name = FieldProperty(ICollectionsManager['thesaurus_name'])
    extract_name = FieldProperty(ICollectionsManager['extract_name'])


@adapter_config(required=ICollectionsManagerTarget,
                provides=ICollectionsManager)
def collections_manager_factory(target):
    """Collections manager factory"""
    return get_annotation_adapter(target, COLLECTIONS_MANAGER_KEY, ICollectionsManager,
                                  name='++collections-manager++')


@factory_config(ICollectionsInfo)
class CollectionsInfo(Persistent, Contained):
    """Collections info persistent class"""

    collections = FieldProperty(ICollectionsInfo['collections'])


@adapter_config(required=ICollectionsTarget,
                provides=ICollectionsInfo)
def collections_info_factory(target):
    """Collections info factory"""
    return get_annotation_adapter(target, COLLECTIONS_INFO_KEY, ICollectionsInfo,
                                  name='++collections++')


@subscriber(IObjectModifiedEvent, context_selector=ICollectionsInfo)
def handle_modified_collections_info(event):
    """Handle modified collections info"""
    target = get_parent(event.object, ICollectionsTarget)
    if target is not None:
        registry = get_pyramid_registry()
        registry.notify(ObjectModifiedEvent(target))
