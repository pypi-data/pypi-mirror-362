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

"""PyAMS_*** module

"""

from pyramid.view import view_config
from zope.interface import Interface, alsoProvides

from pyams_content.component.thesaurus import ICollectionsManager, ITagsManager, IThemesManager
from pyams_content.feature.filter import ICollectionsFilter, IFilter, ITagsFilter, IThemesFilter, ITitleFilter
from pyams_content.feature.filter.interfaces import IContentTypesFilter, IFiltersContainer, IThesaurusFilter
from pyams_content.zmi import content_js
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import IPortletSettings, MANAGE_TEMPLATE_PERMISSION
from pyams_portal.zmi.interfaces import IPortletRendererSettingsEditForm
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_skin.interfaces.view import IModalPage
from pyams_skin.interfaces.viewlet import IContentSuffixViewletManager
from pyams_skin.viewlet.menu import MenuItem
from pyams_table.interfaces import IColumn, IValues
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config, query_adapter
from pyams_utils.fanstatic import get_resource_path
from pyams_utils.interfaces.data import IObjectData
from pyams_utils.traversing import get_parent
from pyams_utils.url import absolute_url
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalAddForm, AdminModalEditForm
from pyams_zmi.helper.container import delete_container_element, switch_element_attribute
from pyams_zmi.helper.event import get_json_table_row_add_callback, get_json_table_row_refresh_callback
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.form import IFormTitle, IPropertiesEditForm
from pyams_zmi.interfaces.table import ITableElementEditor
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager
from pyams_zmi.table import InnerTableAdminView, NameColumn, ReorderColumn, SortableTable, TableElementEditor, \
    TrashColumn, VisibilityColumn
from pyams_zmi.utils import get_object_label

__docformat__ = 'restructuredtext'

from pyams_content import _


class FiltersTable(SortableTable):
    """Filters table"""
    
    container_class = IFiltersContainer
    
    display_if_empty = True
    
    
@adapter_config(required=(IFiltersContainer, IAdminLayer, FiltersTable),
                provides=IValues)
class FiltersTableValues(ContextRequestViewAdapter):
    """Filters table values adapter"""
    
    @property
    def values(self):
        """Filter tables values getter"""
        yield from self.context.values()
        
        
@adapter_config(name='reorder',
                required=(IFiltersContainer, IAdminLayer, FiltersTable),
                provides=IColumn)
class FiltersTableReorderColumn(ReorderColumn):
    """Filters table reorder column"""


@view_config(name='reorder.json',
             context=IFiltersContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True,
             permission=MANAGE_TEMPLATE_PERMISSION)
def reorder_filters_table(request):
    """Reorder filters table"""
    order = request.params.get('order').split(';')
    request.context.updateOrder(order)
    return {
        'status': 'success',
        'closeForm': False
    }


@adapter_config(name='visible',
                required=(IFiltersContainer, IAdminLayer, FiltersTable),
                provides=IColumn)
class FiltersTableVisibleColumn(VisibilityColumn):
    """Filters table visible column"""

    hint = _("Click icon to show or hide filter")


@view_config(name='switch-visible-item.json',
             context=IFiltersContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True)
def switch_visible_filter(request):
    """Switch visible filter"""
    return switch_element_attribute(request)


@adapter_config(name='title',
                required=(IFiltersContainer, IAdminLayer, FiltersTable),
                provides=IColumn)
class FiltersTableTitleColumn(NameColumn):
    """Filters table name column"""

    i18n_header = _("Label")


@adapter_config(name='trash',
                required=(IFiltersContainer, IAdminLayer, FiltersTable),
                provides=IColumn)
class FiltersTableTrashColumn(TrashColumn):
    """Filters table trash column"""


@view_config(name='delete-element.json',
             context=IFiltersContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True,
             permission=MANAGE_TEMPLATE_PERMISSION)
def delete_filter(request):
    """Delete filter"""
    return delete_container_element(request)


@viewlet_config(name='filters-content-table',
                context=IFiltersContainer, layer=IAdminLayer,
                view=IPropertiesEditForm,
                manager=IContentSuffixViewletManager, weight=10)
@viewlet_config(name='filters-content-table',
                context=IFiltersContainer, layer=IAdminLayer,
                view=IPortletRendererSettingsEditForm,
                manager=IContentSuffixViewletManager, weight=10)
class FiltersTableView(InnerTableAdminView):
    """Filters table view"""

    table_class = FiltersTable
    table_label = _("List of filters")


#
# Filters forms
#

class FilterAddMenu(MenuItem):
    """Filter add menu"""

    modal_target = True

    def get_href(self):
        return absolute_url(self.context, self.request, self.href)


class FilterAddForm(AdminModalAddForm):
    """Base filter add form"""

    subtitle = _("New filter")
    legend = _("New filter properties")

    fields = Fields(IFilter).omit('visible')

    def add(self, obj):
        self.context.append(obj)


@adapter_config(required=(IFiltersContainer, IAdminLayer, FilterAddForm),
                provides=IFormTitle)
def filter_add_form_title(context, request, view):
    """Filter add form title"""
    target = get_parent(context, IPortletSettings)
    return query_adapter(IFormTitle, request, target, view)


@adapter_config(required=(IFiltersContainer, IAdminLayer, FilterAddForm),
                provides=IAJAXFormRenderer)
class FilterAddFormRenderer(ContextRequestViewAdapter):
    """Filter add form renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        return {
            'status': 'success',
            'callbacks': [
                get_json_table_row_add_callback(self.context, self.request,
                                                FiltersTable, changes)
            ]
        }


@adapter_config(required=(IFilter, IAdminLayer, Interface),
                provides=ITableElementEditor)
class FilterElementEditor(TableElementEditor):
    """Filter element editor"""


@adapter_config(required=(IFilter, IAdminLayer, IModalPage),
                provides=IFormTitle)
def filter_edit_form_title(context, request, view):
    """Filter edit form title"""
    target = get_parent(context, IPortletSettings)
    return query_adapter(IFormTitle, request, target, view)


class FilterEditForm(AdminModalEditForm):
    """Filter base edit form"""

    @property
    def subtitle(self):
        """Form title getter"""
        translate = self.request.localizer.translate
        return translate(_("Filter: {}")).format(get_object_label(self.context, self.request, self))

    legend = _("Filter properties")
    fields = Fields(IFilter).omit('visible')


@adapter_config(required=(IFilter, IAdminLayer, FilterEditForm),
                provides=IAJAXFormRenderer)
class FilterEditFormRenderer(ContextRequestViewAdapter):
    """Filter edit form renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        return {
            'status': 'success',
            'callbacks': [
                get_json_table_row_refresh_callback(self.context.__parent__, self.request,
                                                    FiltersTable, self.context)
            ]
        }


#
# Title filter forms
#

@viewlet_config(name='add-title-filter.menu',
                context=IFiltersContainer, layer=IAdminLayer, view=FiltersTable,
                manager=IContextAddingsViewletManager, weight=10,
                permission=MANAGE_TEMPLATE_PERMISSION)
class TitleFilterAddMenu(FilterAddMenu):
    """Title filter add menu"""

    label = _("Title filter")
    href = 'add-title-filter.html'


@ajax_form_config(name='add-title-filter.html',
                  context=IFiltersContainer, layer=IPyAMSLayer,
                  permission=MANAGE_TEMPLATE_PERMISSION)
class TitleFilterAddForm(FilterAddForm):
    """Title filter add form"""

    fields = Fields(ITitleFilter).omit('visible')
    content_factory = ITitleFilter


@ajax_form_config(name='properties.html',
                  context=ITitleFilter, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class TitleFilterEditForm(FilterEditForm):
    """Title filter edit form"""

    fields = Fields(ITitleFilter).omit('visible')


#
# Content-type filter forms
#

@viewlet_config(name='add-content-type-filter.menu',
                context=IFiltersContainer, layer=IAdminLayer, view=FiltersTable,
                manager=IContextAddingsViewletManager, weight=15,
                permission=MANAGE_TEMPLATE_PERMISSION)
class ContentTypeFilterAddMenu(FilterAddMenu):
    """Content-type filter add menu"""

    label = _("Content-type filter")
    href = 'add-content-type-filter.html'


@ajax_form_config(name='add-content-type-filter.html',
                  context=IFiltersContainer, layer=IPyAMSLayer,
                  permission=MANAGE_TEMPLATE_PERMISSION)
class ContentTypeFilterAddForm(FilterAddForm):
    """Content-type filter add form"""

    fields = Fields(IContentTypesFilter).omit('visible')
    content_factory = IContentTypesFilter


@ajax_form_config(name='properties.html',
                  context=IContentTypesFilter, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class ContentTypeFilterEditForm(FilterEditForm):
    """Content-type filter edit form"""

    fields = Fields(IContentTypesFilter).omit('visible')


#
# Thesaurus-based filters forms
#

class ThesaurusFilterAddForm(FilterAddForm):
    """Thesaurus-based filter add form"""

    fields = Fields(IThesaurusFilter).omit('visible')

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        thesaurus_name = self.widgets.get('thesaurus_name')
        if thesaurus_name is not None:
            thesaurus_name.prompt = True
            thesaurus_name.prompt_message = _("(no selected thesaurus)")
            thesaurus_name.object_data = {
                'ams-modules': {
                    'content': {
                        'src': get_resource_path(content_js)
                    }
                },
                'ams-change-handler': 'MyAMS.content.thesaurus.changeThesaurus'
            }
            alsoProvides(thesaurus_name, IObjectData)


@ajax_form_config(name='properties.html',
                  context=IThesaurusFilter, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class ThesaurusFilterEditForm(FilterEditForm):
    """Thesaurus-based filter edit form"""

    fields = Fields(IThesaurusFilter).omit('visible')

    def update_widgets(self, prefix=None):
        # store thesaurus name in request header to be able to set
        # extract name correctly
        if self.request.method == 'POST':
            name = f'{self.prefix}widgets.thesaurus_name'
            value = self.request.params.get(name)
            if value is not None:
                self.request.headers['X-Thesaurus-Name'] = value
        super().update_widgets(prefix)
        thesaurus_name = self.widgets.get('thesaurus_name')
        if thesaurus_name is not None:
            thesaurus_name.prompt = True
            thesaurus_name.prompt_message = _("(no selected thesaurus)")
            thesaurus_name.object_data = {
                'ams-modules': {
                    'content': {
                        'src': get_resource_path(content_js)
                    }
                },
                'ams-change-handler': 'MyAMS.content.thesaurus.changeThesaurus'
            }
            alsoProvides(thesaurus_name, IObjectData)


@viewlet_config(name='add-tag-filter.menu',
                context=IFiltersContainer, layer=IAdminLayer, view=FiltersTable,
                manager=IContextAddingsViewletManager, weight=20,
                permission=MANAGE_TEMPLATE_PERMISSION)
class TagsFilterAddMenu(FilterAddMenu):
    """Tags filter add menu"""

    def __new__(cls, context, request, view, manager):
        tags_manager = ITagsManager(request.root, None)
        if (tags_manager is None) or not tags_manager.thesaurus_name:
            return None
        return FilterAddMenu.__new__(cls)

    label = _("Tag filter")
    href = 'add-tag-filter.html'


@ajax_form_config(name='add-tag-filter.html',
                  context=IFiltersContainer, layer=IPyAMSLayer,
                  permission=MANAGE_TEMPLATE_PERMISSION)
class TagsFilterAddForm(ThesaurusFilterAddForm):
    """Tags filter add form"""

    content_factory = ITagsFilter


@viewlet_config(name='add-theme-filter.menu',
                context=IFiltersContainer, layer=IAdminLayer, view=FiltersTable,
                manager=IContextAddingsViewletManager, weight=30,
                permission=MANAGE_TEMPLATE_PERMISSION)
class ThemesFilterAddMenu(FilterAddMenu):
    """Themes filter add menu"""

    def __new__(cls, context, request, view, manager):
        themes_manager = IThemesManager(request.root, None)
        if (themes_manager is None) or not themes_manager.thesaurus_name:
            return None
        return FilterAddMenu.__new__(cls)

    label = _("Theme filter")
    href = 'add-theme-filter.html'


@ajax_form_config(name='add-theme-filter.html',
                  context=IFiltersContainer, layer=IPyAMSLayer,
                  permission=MANAGE_TEMPLATE_PERMISSION)
class ThemesFilterAddForm(ThesaurusFilterAddForm):
    """Themes filter add form"""

    content_factory = IThemesFilter


@viewlet_config(name='add-collection-filter.menu',
                context=IFiltersContainer, layer=IAdminLayer, view=FiltersTable,
                manager=IContextAddingsViewletManager, weight=40,
                permission=MANAGE_TEMPLATE_PERMISSION)
class CollectionsFilterAddMenu(FilterAddMenu):
    """Collections filter add menu"""

    def __new__(cls, context, request, view, manager):
        collections_manager = ICollectionsManager(request.root, None)
        if (collections_manager is None) or not collections_manager.thesaurus_name:
            return None
        return FilterAddMenu.__new__(cls)

    label = _("Collection filter")
    href = 'add-collection-filter.html'


@ajax_form_config(name='add-collection-filter.html',
                  context=IFiltersContainer, layer=IPyAMSLayer,
                  permission=MANAGE_TEMPLATE_PERMISSION)
class CollectionsFilterAddForm(ThesaurusFilterAddForm):
    """Collections filter add form"""

    content_factory = ICollectionsFilter
