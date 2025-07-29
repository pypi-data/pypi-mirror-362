#
# Copyright (c) 2015-2023 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.shared.view.thesaurus module

This module provides persistent classes and adapters used to handle views
thesaurus-based settings support and catalog-based queries.
"""

__docformat__ = 'restructuredtext'

from hypatia.interfaces import ICatalog
from hypatia.query import Eq, Any
from persistent import Persistent
from zope.container.contained import Contained
from zope.intid.interfaces import IIntIds
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.thesaurus import ICollectionsInfo, ITagsInfo, IThemesInfo
from pyams_content.shared.view import IViewSettings, IWfView
from pyams_content.shared.view.interfaces.query import IViewQueryParamsExtension
from pyams_content.shared.view.interfaces.settings import IViewCollectionsSettings, IViewTagsSettings, \
    IViewThemesSettings, VIEW_COLLECTIONS_SETTINGS_KEY, VIEW_TAGS_SETTINGS_KEY, VIEW_THEMES_SETTINGS_KEY
from pyams_utils.adapter import ContextAdapter, adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.registry import get_utility


#
# Tags management
#

@factory_config(IViewTagsSettings)
class ViewTagsSettings(Persistent, Contained):
    """View tags settings"""

    select_context_tags = FieldProperty(IViewTagsSettings['select_context_tags'])
    tags = FieldProperty(IViewTagsSettings['tags'])

    @property
    def is_using_context(self):
        """Context usage checker"""
        return self.select_context_tags

    def get_tags(self, context):
        """Selection tags getter"""
        tags = set()
        if self.select_context_tags:
            tags_info = ITagsInfo(context, None)
            if tags_info is not None:
                tags |= set(tags_info.tags or ())
        if self.tags:
            tags |= set(self.tags)
        return tags

    def get_tags_index(self, context):
        """Tags index values getter"""
        intids = get_utility(IIntIds)
        return [
            intids.register(term)
            for term in self.get_tags(context)
        ]


@adapter_config(required=IWfView,
                provides=IViewTagsSettings)
@adapter_config(name='tags',
                required=IWfView,
                provides=IViewSettings)
def view_tags_settings(view):
    """View tags settings factory"""
    return get_annotation_adapter(view, VIEW_TAGS_SETTINGS_KEY,
                                  IViewTagsSettings,
                                  name='++view:tags++')


@adapter_config(name='tags',
                required=IWfView,
                provides=IViewQueryParamsExtension)
class ViewTagsQueryParamsExtension(ContextAdapter):
    """View tags query params extension"""

    weight = 50

    def get_params(self, context, request=None):
        """Query params getter"""
        catalog = get_utility(ICatalog)
        settings = IViewTagsSettings(self.context)
        # check tags
        tags = settings.get_tags_index(context)
        if tags:
            yield Any(catalog['tags'], tags)
        elif settings.select_context_tags:
            yield None


#
# Themes management
#

@factory_config(IViewThemesSettings)
class ViewThemesSettings(Persistent, Contained):
    """View themes settings"""

    select_context_themes = FieldProperty(IViewThemesSettings['select_context_themes'])
    themes = FieldProperty(IViewThemesSettings['themes'])
    include_subthemes = FieldProperty(IViewThemesSettings['include_subthemes'])

    @property
    def is_using_context(self):
        return self.select_context_themes

    def get_themes(self, context):
        themes = set()
        if self.select_context_themes:
            themes_info = IThemesInfo(context, None)
            if themes_info is not None:
                themes |= set(themes_info.themes or ())
        if self.themes:
            themes |= set(self.themes)
        if self.include_subthemes:
            for theme in themes.copy():
                themes |= set(theme.get_all_childs())
        return themes

    def get_themes_index(self, context):
        intids = get_utility(IIntIds)
        return [intids.register(term) for term in self.get_themes(context)]


@adapter_config(context=IWfView,
                provides=IViewThemesSettings)
@adapter_config(name='themes',
                context=IWfView,
                provides=IViewSettings)
def view_themes_settings(view):
    """View themes settings factory"""
    return get_annotation_adapter(view, VIEW_THEMES_SETTINGS_KEY,
                                  IViewThemesSettings,
                                  name='++view:themes++')


@adapter_config(name='themes',
                context=IWfView,
                provides=IViewQueryParamsExtension)
class ViewThemesQueryParamsExtension(ContextAdapter):
    """View themes query params extension"""

    weight = 52

    def get_params(self, context, request=None):
        """Query params getter"""
        catalog = get_utility(ICatalog)
        settings = IViewThemesSettings(self.context)
        # check themes
        themes = settings.get_themes_index(context)
        if themes:
            yield Any(catalog['themes'], themes)
        elif settings.select_context_themes:
            yield None


#
# Collections management
#

@factory_config(IViewCollectionsSettings)
class ViewCollectionsSettings(Persistent, Contained):
    """View collections settings"""

    select_context_collections = FieldProperty(IViewCollectionsSettings['select_context_collections'])
    collections = FieldProperty(IViewCollectionsSettings['collections'])

    @property
    def is_using_context(self):
        return self.select_context_collections

    def get_collections(self, context):
        collections = set()
        if self.select_context_collections:
            collections_info = ICollectionsInfo(context, None)
            if collections_info is not None:
                collections |= set(collections_info.collections or ())
        if self.collections:
            collections |= set(self.collections)
        return collections

    def get_collections_index(self, context):
        intids = get_utility(IIntIds)
        return [intids.register(term) for term in self.get_collections(context)]


@adapter_config(required=IWfView,
                provides=IViewCollectionsSettings)
@adapter_config(name='collections',
                required=IWfView,
                provides=IViewSettings)
def view_collections_settings(view):
    """View collections settings factory"""
    return get_annotation_adapter(view, VIEW_COLLECTIONS_SETTINGS_KEY,
                                  IViewCollectionsSettings,
                                  name='++view:collections++')


@adapter_config(name='collections',
                context=IWfView,
                provides=IViewQueryParamsExtension)
class ViewCollectionsQueryParamsExtension(ContextAdapter):
    """View collections query params extension"""

    weight = 54

    def get_params(self, context, request=None):
        """Query params getter"""
        catalog = get_utility(ICatalog)
        settings = IViewCollectionsSettings(self.context)
        # check collections
        collections = settings.get_collections_index(context)
        if collections:
            yield Any(catalog['collections'], collections)
        elif settings.select_context_collections:
            yield None
