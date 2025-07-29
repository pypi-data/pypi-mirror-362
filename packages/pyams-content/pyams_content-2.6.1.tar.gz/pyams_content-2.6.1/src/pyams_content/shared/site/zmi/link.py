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

"""PyAMS_content.site.zmi.link module

"""

from uuid import uuid4

from zope.container.interfaces import IContainer
from zope.interface import Interface, implementer
from zope.intid import IIntIds
from zope.schema import Int

from pyams_content.interfaces import CREATE_CONTENT_PERMISSION, MANAGE_CONTENT_PERMISSION
from pyams_content.shared.site.interfaces import IExternalSiteLink, IInternalSiteLink, \
    ISiteContainer, ISiteLink, ISiteManager
from pyams_content.shared.site.zmi.interfaces import ISiteTreeTable
from pyams_content.shared.site.zmi.tree import SiteContainerTreeTable
from pyams_content.shared.site.zmi.widget.folder import SiteManagerFoldersSelectorFieldWidget
from pyams_content.zmi.interfaces import IDashboardColumn, IDashboardContentLabel, \
    IDashboardContentModifier, IDashboardContentNumber, IDashboardContentOwner, \
    IDashboardContentStatus, IDashboardContentStatusDatetime, IDashboardContentType, \
    IDashboardContentVersion, IDashboardContentVisibility
from pyams_skin.interfaces.view import IModalEditForm
from pyams_utils.interfaces import MISSING_INFO
from pyams_zmi.interfaces.form import IFormTitle, IPropertiesEditForm
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.form import apply_changes
from pyams_form.interfaces.form import IAJAXFormRenderer, IGroup
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_skin.viewlet.menu import MenuDivider, MenuItem
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config, query_adapter
from pyams_utils.registry import get_utility
from pyams_utils.traversing import get_parent
from pyams_utils.url import absolute_url
from pyams_viewlet.viewlet import viewlet_config
from pyams_workflow.interfaces import IWorkflowPublicationInfo
from pyams_zmi.form import AdminModalAddForm, AdminModalEditForm, FormGroupChecker
from pyams_zmi.helper.event import get_json_table_row_refresh_callback
from pyams_zmi.interfaces import IAdminLayer, TITLE_SPAN_BREAK
from pyams_zmi.interfaces.table import ITableElementEditor
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager
from pyams_zmi.table import TableElementEditor
from pyams_zmi.utils import get_object_label


__docformat__ = 'restructuredtext'

from pyams_content import _


class SiteLinkAddForm(AdminModalAddForm):
    """Base site link add form"""

    subtitle = _("New link")

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        if 'parent' in self.widgets:
            self.widgets['parent'].permission = CREATE_CONTENT_PERMISSION

    def add(self, obj):
        setattr(self, '_v_target', obj.__parent__)

    def update_content(self, link, data):
        data = data.get(self, data)
        # locate new link
        intids = get_utility(IIntIds)
        parent = intids.queryObject(data.pop('parent'))
        if parent is not None:
            uuid = str(uuid4())
            parent[uuid] = link
        # initialize new link attributes
        apply_changes(self, link, data)


@adapter_config(required=(ISiteContainer, IAdminLayer, SiteLinkAddForm),
                provides=IFormTitle)
def site_link_add_form_title(context, request, form):
    """Site link add form title"""
    manager = get_parent(context, ISiteManager)
    if manager is context:
        return get_object_label(manager, request, form)
    return TITLE_SPAN_BREAK.format(
        get_object_label(manager, request, form),
        get_object_label(context, request, form))


@adapter_config(required=(ISiteContainer, IAdminLayer, SiteLinkAddForm),
                provides=IAJAXFormRenderer)
class SiteLinkAddFormRenderer(ContextRequestViewAdapter):
    """Site link add form renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if changes is None:
            return None
        target = getattr(self.view, '_v_target', self.request.context)
        return {
            'status': 'reload',
            'location': absolute_url(target, self.request, 'site-tree.html')
        }


@adapter_config(required=(ISiteLink, IAdminLayer, Interface),
                provides=ITableElementEditor)
class SiteLinkTableElementEditor(TableElementEditor):
    """Site link table element editor"""


@implementer(IPropertiesEditForm)
class SiteLinkPropertiesEditForm(AdminModalEditForm):
    """Site link properties edit form"""

    @property
    def subtitle(self):
        """Title getter"""
        translate = self.request.localizer.translate
        return translate(_("{content_name}: {label}")).format(
                content_name=translate(self.context.content_name),
                label=get_object_label(self.context, self.request, self))

    legend = _("Link properties")

    _edit_permission = MANAGE_CONTENT_PERMISSION


@adapter_config(required=(ISiteLink, IAdminLayer,
                          SiteLinkPropertiesEditForm),
                provides=IGroup)
class SiteLinkHeaderGroup(FormGroupChecker):
    """Site link header group"""

    fields = Fields(ISiteLink).select('show_header', 'navigation_header')
    checker_fieldname = 'show_header'


@adapter_config(required=(ISiteLink, IAdminLayer,
                          SiteLinkPropertiesEditForm),
                provides=IAJAXFormRenderer)
class SiteLinkPropertiesEditFormRenderer(ContextRequestViewAdapter):
    """Site link properties edit form renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        container = get_parent(self.context, ISiteManager)
        return {
            'status': 'success',
            'message': self.request.localizer.translate(self.view.success_message),
            'callbacks': [
                get_json_table_row_refresh_callback(container, self.request,
                                                    SiteContainerTreeTable, self.context)
            ]
        }


@adapter_config(required=(ISiteLink, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentVisibility)
def site_link_dashboard_visibility(context, request, column):
    """Site link dashboard visibility"""
    if not column.has_permission(context):
        return False, ''
    icon_class = column.object_data.get('ams-icon-on' if context.visible else 'ams-icon-off')
    if not IWorkflowPublicationInfo(context.__parent__).is_published(request):
        icon_class += ' text-danger'
    hint = request.localizer.translate(_("Click to switch link visibility"))
    return True, f'<i class="fa-fw {icon_class} hint"' \
                 f'   data-original-title="{hint}"></i>'


#
# Internal link components
#

@viewlet_config(name='add-links.divider',
                context=ISiteContainer, layer=IAdminLayer, view=ISiteTreeTable,
                manager=IContextAddingsViewletManager, weight=49,
                permission=CREATE_CONTENT_PERMISSION)
class SiteLinksAddMenuDivider(MenuDivider):
    """Site links add menus divider"""


@viewlet_config(name='add-internal-link.menu',
                context=ISiteContainer, layer=IAdminLayer, view=ISiteTreeTable,
                manager=IContextAddingsViewletManager, weight=50,
                permission=CREATE_CONTENT_PERMISSION)
class InternalSiteLinkAddMenu(MenuItem):
    """Internal site link add menu"""

    label = _("Add internal link...")
    icon_class = 'fas fa-sign-in-alt fa-rotate-270'

    href = 'add-internal-link.html'
    modal_target = True


class IInternalSiteLinkAddFormFields(IInternalSiteLink):
    """Internal content link add form fields interface"""

    parent = Int(title=_("Parent"),
                 description=_("Link's parent"),
                 required=True)


@ajax_form_config(name='add-internal-link.html',
                  context=ISiteContainer, layer=IPyAMSLayer,
                  permission=CREATE_CONTENT_PERMISSION)
class InternalSiteLinkAddForm(SiteLinkAddForm):
    """Internal site link add form"""

    subtitle = _("New internal link")
    legend = _("New internal link properties")

    fields = Fields(IInternalSiteLinkAddFormFields).select('reference', 'force_canonical_url',
                                                           'navigation_title', 'parent')
    fields['parent'].widget_factory = SiteManagerFoldersSelectorFieldWidget
    content_factory = IInternalSiteLink

    def update_content(self, link, data):
        super().update_content(link, data)
        data = data.get(self, data)
        link.reference = data['reference']


@ajax_form_config(name='properties.html',
                  context=IInternalSiteLink, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class InternalSiteLinkPropertiesEditForm(SiteLinkPropertiesEditForm):
    """Internal site link properties edit form"""

    fields = Fields(IInternalSiteLink).select('reference', 'force_canonical_url',
                                              'navigation_title')


@adapter_config(required=(IInternalSiteLink, IAdminLayer, IModalEditForm),
                provides=IFormTitle)
def internal_site_link_edit_form_title(context, request, form):
    """Internal site link edit form title"""
    parent = get_parent(context, IContainer)
    return query_adapter(IFormTitle, request, parent, form)


@adapter_config(required=(IInternalSiteLink, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentLabel)
def internal_content_link_dashboard_label(context, request, column):
    """Internal content link dashboard label"""
    label = II18n(context).query_attribute('navigation_title', request=request)
    if not label:
        target = context.target
        if target is not None:
            label = get_object_label(target, request)
    translate = request.localizer.translate
    return f'{label} <i class="ml-1 fas fa-sign-in-alt fa-rotate-270 hint" ' \
           f'data-original-title="{translate(context.content_name)}"></i>'


def get_internal_link_adapter(context, request, column, interface):
    """Get internal link column adapter"""
    target = context.target
    if target is not None:
        value = request.registry.queryMultiAdapter((target, request, column), interface)
        return f'({value.strip()})' if value is not None else MISSING_INFO
    return MISSING_INFO


@adapter_config(required=(IInternalSiteLink, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentType)
def internal_content_link_type(context, request, column):
    """Internal content link dashboard type"""
    return get_internal_link_adapter(context, request, column, IDashboardContentType)


@adapter_config(required=(IInternalSiteLink, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentNumber)
def internal_content_link_dashboard_number(context, request, column):
    """Internal content link dashboard number"""
    return get_internal_link_adapter(context, request, column, IDashboardContentNumber)


@adapter_config(required=(IInternalSiteLink, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentStatus)
def internal_content_link_dashboard_status(context, request, column):
    """Internal content link dashboard status"""
    return get_internal_link_adapter(context, request, column, IDashboardContentStatus)


@adapter_config(required=(IInternalSiteLink, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentStatusDatetime)
def internal_content_link_dashboard_status_datetime(context, request, column):
    """Internal content link dashboard status datetime"""
    return get_internal_link_adapter(context, request, column, IDashboardContentStatusDatetime)


@adapter_config(required=(IInternalSiteLink, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentVersion)
def internal_content_link_dashboard_version(context, request, column):
    """Internal content link dashboard version"""
    return get_internal_link_adapter(context, request, column, IDashboardContentVersion)


@adapter_config(required=(IInternalSiteLink, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentModifier)
def internal_content_link_dashboard_modifier(context, request, column):
    """Internal content link dashboard modifier"""
    return get_internal_link_adapter(context, request, column, IDashboardContentModifier)


@adapter_config(required=(IInternalSiteLink, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentOwner)
def internal_content_link_dashboard_owner(context, request, column):
    """Internal content link dashboard owner"""
    return get_internal_link_adapter(context, request, column, IDashboardContentOwner)


#
# External site link components
#

@viewlet_config(name='add-external-link.menu',
                context=ISiteContainer, layer=IAdminLayer, view=ISiteTreeTable,
                manager=IContextAddingsViewletManager, weight=60,
                permission=CREATE_CONTENT_PERMISSION)
class ExternalSiteLinkAddMenu(MenuItem):
    """External site link add menu"""

    label = _("Add external link...")
    icon_class = 'fas fa-link'

    href = 'add-external-link.html'
    modal_target = True


class IExternalSiteLinkAddFormFields(IExternalSiteLink):
    """External site link add form fields interface"""

    parent = Int(title=_("Parent"),
                 description=_("Link's parent"),
                 required=True)


@ajax_form_config(name='add-external-link.html',
                  context=ISiteContainer, layer=IPyAMSLayer,
                  permission=CREATE_CONTENT_PERMISSION)
class ExternalSiteLinkAddForm(SiteLinkAddForm):
    """External site link add form"""

    subtitle = _("New external link")
    legend = _("New external link properties")

    fields = Fields(IExternalSiteLinkAddFormFields).select('url', 'navigation_title',
                                                           'parent')
    fields['parent'].widget_factory = SiteManagerFoldersSelectorFieldWidget
    content_factory = IExternalSiteLink

    def update_content(self, link, data):
        super().update_content(link, data)
        data = data.get(self, data)
        link.url = data['url']


@ajax_form_config(name='properties.html',
                  context=IExternalSiteLink, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class ExternalSiteLinkPropertiesEditForm(SiteLinkPropertiesEditForm):
    """External site link properties edit form"""

    fields = Fields(IExternalSiteLink).select('url', 'navigation_title')


@adapter_config(required=(IExternalSiteLink, IAdminLayer, IModalEditForm),
                provides=IFormTitle)
def external_site_link_edit_form_title(context, request, form):
    """External site link edit form title"""
    parent = get_parent(context, IContainer)
    return query_adapter(IFormTitle, request, parent, form)


@adapter_config(required=(IExternalSiteLink, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentLabel)
def external_site_link_dashboard_label(context, request, column):
    """External site link dashboard label"""
    label = II18n(context).query_attribute('navigation_title', request=request)
    if not label:
        label = context.url
    translate = request.localizer.translate
    return f'{label} <i class="ml-1 fas fa-link hint" ' \
           f'data-original-title="{translate(context.content_name)}"></i>'
