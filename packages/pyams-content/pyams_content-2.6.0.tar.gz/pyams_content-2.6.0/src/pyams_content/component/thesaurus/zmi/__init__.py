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

"""PyAMS_content.component.thesaurus.zmi module


"""

from pyramid.traversal import lineage
from zope.interface import Interface, alsoProvides, implementer

from pyams_content.component.thesaurus import ICollectionsInfo, ICollectionsManager, \
    ICollectionsTarget, ITagsInfo, ITagsManager, ITagsTarget, IThemesInfo, IThemesManager, \
    IThemesTarget
from pyams_content.component.thesaurus.zmi.interfaces import IThesaurusThemesEditForm
from pyams_content.shared.common.interfaces.types import ITypedSharedTool
from pyams_content.shared.common.zmi.types.interfaces import ISharedToolTypesTable
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IGroup, IInnerSubForm
from pyams_form.subform import InnerEditForm
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_table.interfaces import IColumn
from pyams_thesaurus.interfaces.thesaurus import IThesaurus
from pyams_thesaurus.zmi.widget import ThesaurusTermsTreeFieldWidget
from pyams_utils.adapter import adapter_config
from pyams_utils.registry import query_utility
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminEditForm, AdminModalEditForm, FormGroupChecker
from pyams_zmi.interfaces import IAdminLayer, TITLE_SPAN_BREAK
from pyams_zmi.interfaces.form import IFormTitle
from pyams_zmi.interfaces.viewlet import IPropertiesMenu
from pyams_zmi.table import ActionColumn
from pyams_zmi.utils import get_object_hint, get_object_label
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem


__docformat__ = 'restructuredtext'

from pyams_content import _


class BaseThesaurusTermsEditFormMixin:
    """Base thesaurus terms edit form"""

    label_css_class = 'hidden'
    input_css_class = 'col-12'

    manager = None
    interface = None
    fieldname = None

    @property
    def fields(self):
        """Fields getter"""
        fields = Fields(self.interface).select(self.fieldname)
        fields[self.fieldname].widget_factory = ThesaurusTermsTreeFieldWidget
        return fields

    def get_content(self):
        """Content getter"""
        return self.interface(self.context)

    def update_widgets(self, prefix=None):
        """Widgets update"""
        super().update_widgets(prefix)
        widget = self.widgets.get(self.fieldname)
        if widget is not None:
            for parent in lineage(self.context):
                manager = self.manager(parent, None)
                if manager is not None:
                    widget.thesaurus_name = manager.thesaurus_name
                    widget.extract_name = manager.extract_name
                    break


#
# Tags management views
#

@viewlet_config(name='tags.menu',
                context=ITagsTarget, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=350,
                permission=VIEW_SYSTEM_PERMISSION)
class TagsMenu(NavigationMenuItem):
    """Tags menu"""

    def __new__(cls, context, request, view, manager):  # pylint: disable=unused-argument
        tags_manager = ITagsManager(request.root, None)
        if (tags_manager is None) or not tags_manager.thesaurus_name:
            return None
        return NavigationMenuItem.__new__(cls)

    label = _("Tags")
    href = '#tags.html'


class BaseTagsEditFormMixin(BaseThesaurusTermsEditFormMixin):
    """Base tags edit form"""

    legend = _("Content tags selection")

    manager = ITagsManager
    interface = ITagsInfo
    fieldname = 'tags'


@ajax_form_config(name='tags.html',
                  context=ITagsTarget, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class TagsEditForm(BaseTagsEditFormMixin, AdminEditForm):
    """Tags edit form"""

    title = _("Content tags")


@ajax_form_config(name='tags-modal.html',
                  context=ITagsTarget, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class TagsModalEditForm(BaseTagsEditFormMixin, AdminModalEditForm):
    """Tags modal edit form"""

    modal_class = 'modal-xl'
    subtitle = _("Content type default tags")


@adapter_config(required=(ITagsTarget, IAdminLayer, TagsModalEditForm),
                provides=IFormTitle)
def tags_edit_form_title(context, request, view):
    """Tags edit form title"""
    return TITLE_SPAN_BREAK.format(
        get_object_hint(context, request, view),
        get_object_label(context, request, view))


@adapter_config(name='tags',
                required=(ITagsInfo, IAdminLayer, BaseTagsEditFormMixin),
                provides=IThesaurus)
def tags_edit_form_thesaurus_adapter(context, request, view):  # pylint: disable=unused-argument
    """Tags edit form thesaurus adapter"""
    manager = ITagsManager(request.root, ITagsManager)
    if manager.thesaurus_name:
        return query_utility(IThesaurus, name=manager.thesaurus_name)
    return None


@adapter_config(name='tags',
                required=(ITypedSharedTool, IAdminLayer, ISharedToolTypesTable),
                provides=IColumn)
class SharedToolTypesTagsColumn(ActionColumn):
    """Shared tool data types table tags column"""

    hint = _("Default tags")
    icon_class = 'fas fa-tag'

    href = 'tags-modal.html'
    modal_target = True

    weight = 500


#
# Themes management views
#

@viewlet_config(name='themes.menu',
                context=IThemesTarget, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=360,
                permission=VIEW_SYSTEM_PERMISSION)
class ThemesMenu(NavigationMenuItem):
    """Themes menu"""

    def __new__(cls, context, request, view, manager):  # pylint: disable=unused-argument
        for parent in lineage(context):
            themes_manager = IThemesManager(parent, None)
            if themes_manager is not None:
                return NavigationMenuItem.__new__(cls) if themes_manager.thesaurus_name else None
        return None

    label = _("Themes")
    href = '#themes.html'


class BaseThemesEditFormMixin(BaseThesaurusTermsEditFormMixin):
    """Base themes edit form mixin"""

    legend = _("Content themes selection")

    manager = IThemesManager
    interface = IThemesInfo
    fieldname = 'themes'

    def __init__(self, context, request):
        super().__init__(context, request)
        if not IThemesInfo(context).can_inherit:
            alsoProvides(self, IThesaurusThemesEditForm)
        else:
            self.legend = None


@ajax_form_config(name='themes.html',
                  context=IThemesTarget, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class ThemesEditForm(BaseThemesEditFormMixin, AdminEditForm):
    """Themes edit form"""

    title = _("Content themes")
    fields = Fields(Interface)


@ajax_form_config(name='themes-modal.html',
                  context=IThemesTarget, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class ThemesModalEditForm(BaseThemesEditFormMixin, AdminModalEditForm):
    """Themes modal edit form"""

    modal_class = 'modal-xl'
    subtitle = _("Content type default themes")
    fields = Fields(Interface)


@adapter_config(required=(IThemesTarget, IAdminLayer, ThemesModalEditForm),
                provides=IFormTitle)
def themes_edit_form_title(context, request, view):
    """Themes edit form title"""
    return TITLE_SPAN_BREAK.format(
        get_object_hint(context, request, view),
        get_object_label(context, request, view))


@adapter_config(name='themes-override',
                required=(IThemesTarget, IAdminLayer, BaseThemesEditFormMixin),
                provides=IGroup)
@implementer(IThesaurusThemesEditForm)
class ThemesEditFormInheritGroup(FormGroupChecker):
    """Themes edit form inherit group"""

    def __new__(cls, context, request, parent_form):
        if not IThemesInfo(context).can_inherit:
            return None
        return FormGroupChecker.__new__(cls)

    def __init__(self, context, request, parent_form):
        super().__init__(context, request, parent_form)
        self.legend = _("Don't inherit parent themes")

    fields = Fields(IThemesInfo).select('no_inherit')
    checker_fieldname = 'no_inherit'
    checker_mode = 'disable'


@adapter_config(name='themes-info',
                required=(IThemesTarget, IAdminLayer, IThesaurusThemesEditForm),
                provides=IInnerSubForm)
class ThemesInnerEditForm(BaseThemesEditFormMixin, InnerEditForm):
    """Themes inner edit form"""

    def __init__(self, context, request, parent_form):
        InnerEditForm.__init__(self, context, request, parent_form)
        if IThemesInfo(context).can_inherit:
            self.legend = None
            self.border_class = None


@adapter_config(name='themes',
                required=(IThemesInfo, IAdminLayer, BaseThemesEditFormMixin),
                provides=IThesaurus)
def themes_edit_form_thesaurus_adapter(context, request, view):  # pylint: disable=unused-argument
    """Themes edit form thesaurus adapter"""
    for parent in lineage(context):
        manager = IThemesManager(parent, None)
        if manager is not None:
            return query_utility(IThesaurus, name=manager.thesaurus_name) if manager.thesaurus_name else None
    return None


@adapter_config(name='themes',
                required=(ITypedSharedTool, IAdminLayer, ISharedToolTypesTable),
                provides=IColumn)
class SharedToolTypesThemesColumn(ActionColumn):
    """Shared tool data types table themes column"""

    hint = _("Default themes")
    icon_class = 'fas fa-tags'

    href = 'themes-modal.html'
    modal_target = True

    weight = 510


#
# Collections management views
#

@viewlet_config(name='collections.menu',
                context=ICollectionsTarget, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=370,
                permission=VIEW_SYSTEM_PERMISSION)
class CollectionsMenu(NavigationMenuItem):
    """Collections menu"""

    def __new__(cls, context, request, view, manager):  # pylint: disable=unused-argument
        collections_manager = ICollectionsManager(request.root, None)
        if (collections_manager is None) or not collections_manager.thesaurus_name:
            return None
        return NavigationMenuItem.__new__(cls)

    label = _("Collections")
    href = '#collections.html'


@ajax_form_config(name='collections.html',
                  context=ICollectionsTarget, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class CollectionsEditForm(BaseThesaurusTermsEditFormMixin, AdminEditForm):
    """Collections edit form"""

    legend = _("Content collections selection")

    manager = ICollectionsManager
    interface = ICollectionsInfo
    fieldname = 'collections'


@ajax_form_config(name='collections-modal.html',
                  context=ICollectionsTarget, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class CollectionsModalEditForm(BaseThemesEditFormMixin, AdminModalEditForm):
    """Collections modal edit form"""

    modal_class = 'modal-xl'
    subtitle = _("Content type default collections")


@adapter_config(required=(ICollectionsTarget, IAdminLayer, CollectionsModalEditForm),
                provides=IFormTitle)
def collections_edit_form_title(context, request, form):
    """Collections modal edit form title"""
    return TITLE_SPAN_BREAK.format(
        get_object_hint(context, request, form),
        get_object_label(context, request, form))


@adapter_config(name='collections',
                required=(ICollectionsInfo, IAdminLayer, CollectionsEditForm),
                provides=IThesaurus)
def collections_edit_form_thesaurus_adapter(context, request, view):  # pylint: disable=unused-argument
    """Collections edit form thesaurus adapter"""
    manager = ICollectionsManager(request.root, ICollectionsManager)
    if manager.thesaurus_name:
        return query_utility(IThesaurus, name=manager.thesaurus_name)
    return None
