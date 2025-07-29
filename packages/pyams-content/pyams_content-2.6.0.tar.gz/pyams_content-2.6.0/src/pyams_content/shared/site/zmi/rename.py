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

"""PyAMS_content.shared.common.zmi.rename module

This module defines components which can be used to rename a site element.
"""

from pyramid.events import subscriber
from zope.container.interfaces import IContainer, IOrderedContainer
from zope.interface import Invalid
from zope.lifecycleevent import ObjectMovedEvent

from pyams_content.interfaces import MANAGE_SITE_PERMISSION
from pyams_content.shared.site.interfaces import IBaseSiteItem
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer, IDataExtractedEvent
from pyams_layer.interfaces import IPyAMSLayer
from pyams_skin.viewlet.menu import MenuItem
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.traversing import get_parent
from pyams_utils.unicode import translate_string
from pyams_utils.url import absolute_url
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalEditForm
from pyams_zmi.interfaces import IAdminLayer, TITLE_SPAN_BREAK
from pyams_zmi.interfaces.form import IFormTitle
from pyams_zmi.interfaces.viewlet import IContextActionsDropdownMenu
from pyams_zmi.utils import get_object_label

__docformat__ = 'restructuredtext'

from pyams_content import _


@viewlet_config(name='rename-site-item.menu',
                context=IBaseSiteItem, layer=IAdminLayer,
                manager=IContextActionsDropdownMenu, weight=10,
                permission=MANAGE_SITE_PERMISSION)
class SiteItemRenameMenu(MenuItem):
    """Site item rename menu"""

    label = _("Change URL")
    icon_class = 'fas fa-pencil-alt'

    href = 'rename-site-item.html'
    modal_target = True


@ajax_form_config(name='rename-site-item.html',
                  context=IBaseSiteItem, layer=IPyAMSLayer,
                  permission=MANAGE_SITE_PERMISSION)
class SiteItemRenameForm(AdminModalEditForm):
    """Site item rename form"""

    subtitle = _("Change item URL")
    legend = _("New item URL")

    fields = Fields(IBaseSiteItem).select('__name__')

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        name = self.widgets.get('__name__')
        if name is not None:
            name.required = True
            name.label = _("Item URL")
            name.description = _("URL part used to access this item")

    def apply_changes(self, data):
        data = data.get(self, data)
        content = self.get_content()
        parent = content.__parent__
        order = list(parent.keys())
        old_name = content.__name__
        new_name = data['__name__'] = translate_string(data.get('__name__', ''),
                                                       force_lower=True, spaces='-')
        changes = super().apply_changes(data)
        if changes:
            parent[new_name] = content
            del parent[old_name]
            self.request.registry.notify(ObjectMovedEvent(content, parent, old_name,
                                                          parent, new_name))
            if IOrderedContainer.providedBy(parent):
                # restore keys order
                order[order.index(old_name)] = new_name
                parent.updateOrder(order)
        return changes


@adapter_config(required=(IBaseSiteItem, IAdminLayer, SiteItemRenameForm),
                provides=IFormTitle)
def base_site_item_rename_form_title(context, request, form):
    """Base site item rename form title"""
    parent = get_parent(context, IContainer, allow_context=False)
    return TITLE_SPAN_BREAK.format(
        get_object_label(parent, request, form),
        get_object_label(context, request, form))


@subscriber(IDataExtractedEvent, form_selector=SiteItemRenameForm)
def handle_rename_form_data(event):
    """Handle form rename data"""
    data = event.data
    form = event.form
    if not data.get('__name__'):
        form.widgets.errors += (Invalid(_("Item URL can't be empty!")),)
    else:
        context = form.context
        new_name = translate_string(data.get('__name__', ''), force_lower=True, spaces='-')
        if (new_name in context.__parent__) and (new_name != context.__name__):
            form.widgets.errors += (Invalid(_("Selected name is already used!")),)


@adapter_config(required=(IBaseSiteItem, IAdminLayer, SiteItemRenameForm),
                provides=IAJAXFormRenderer)
class SiteItemRenameFormRenderer(ContextRequestViewAdapter):
    """Site item rename form renderer"""

    def render(self, changes):
        """Form renderer"""
        if changes is None:
            return None
        return {
            'status': 'redirect',
            'location': absolute_url(self.context, self.request, 'admin'),
            'smallbox': {
                'status': 'success',
                'message': self.request.localizer.translate(self.view.success_message)
            }
        }
