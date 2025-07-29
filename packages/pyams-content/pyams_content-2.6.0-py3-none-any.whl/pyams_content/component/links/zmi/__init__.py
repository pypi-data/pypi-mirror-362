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

"""PyAMS_content.component.links.zmi module

"""

from pyramid.events import subscriber
from pyramid.view import view_config
from zope.interface import Invalid, implementer

from pyams_content.component.association.interfaces import IAssociationContainer, IAssociationContainerTarget, \
    IAssociationInfo
from pyams_content.component.association.zmi import AssociationItemAddFormMixin, \
    AssociationItemAddMenuMixin
from pyams_content.component.association.zmi.interfaces import IAssociationsTable
from pyams_content.component.links import ExternalLink, InternalLink, MailtoLink
from pyams_content.component.links.interfaces import IBaseLink, IExternalLink, IExternalLinksManagerInfo, IInternalLink, \
    ILinkContainerTarget, IMailtoLink
from pyams_content.component.links.zmi.interfaces import ILinkAddForm, ILinkEditForm
from pyams_content.reference.pictogram.zmi.widget import PictogramSelectFieldWidget
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IDataExtractedEvent
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_security.security import ProtectedViewObjectMixin
from pyams_skin.viewlet.menu import MenuItem
from pyams_utils.adapter import adapter_config
from pyams_utils.traversing import get_parent
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalAddForm, AdminModalEditForm
from pyams_zmi.interfaces import IAdminLayer, TITLE_SPAN_BREAK
from pyams_zmi.interfaces.form import IFormTitle
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager
from pyams_zmi.utils import get_object_hint, get_object_label

__docformat__ = 'restructuredtext'

from pyams_content import _


@implementer(ILinkAddForm)
class LinkAddFormMixin(AssociationItemAddFormMixin):
    """Link add form mixin class"""

    legend = _("New link properties")


@adapter_config(required=(IAssociationContainer, IAdminLayer, ILinkAddForm),
                provides=IFormTitle)
def link_add_form_title(context, request, form):
    """Link add form title getter"""
    parent = get_parent(context, IAssociationContainerTarget)
    hint = get_object_hint(parent, request, form)
    label = get_object_label(parent, request, form)
    return TITLE_SPAN_BREAK.format(hint, label)


@implementer(ILinkEditForm)
class LinkEditFormMixin:
    """Link edit form mixin class"""

    @property
    def subtitle(self):
        translate = self.request.localizer.translate
        return translate(_("{}: {}")).format(
            translate(self.context.icon_hint),
            get_object_label(self.context, self.request, self))

    legend = _("Link properties")


@adapter_config(required=(IBaseLink, IAdminLayer, ILinkEditForm),
                provides=IFormTitle)
def link_edit_form_title(context, request, form):
    """Link edit form title"""
    parent = get_parent(context, IAssociationContainerTarget)
    hint = get_object_hint(parent, request, form)
    label = get_object_label(parent, request, form)
    return TITLE_SPAN_BREAK.format(
        hint, label)


#
# Internal links management
#

@viewlet_config(name='add-internal-link.menu',
                context=ILinkContainerTarget, layer=IAdminLayer, view=IAssociationsTable,
                manager=IContextAddingsViewletManager, weight=50)
class InternalLinkAddMenu(ProtectedViewObjectMixin, AssociationItemAddMenuMixin, MenuItem):
    """Internal link add menu"""

    label = InternalLink.icon_hint
    icon_class = InternalLink.icon_class

    href = 'add-internal-link.html'


@ajax_form_config(name='add-internal-link.html',
                  context=IAssociationContainer, layer=IPyAMSLayer)
class InternalLinkAddForm(LinkAddFormMixin, AdminModalAddForm):
    """Internal link add form"""

    subtitle = _("New internal link")
    legend = _("New internal link properties")

    fields = Fields(IInternalLink).select('reference', 'force_canonical_url', 'title',
                                          'description', 'pictogram_name')
    fields['pictogram_name'].widget_factory = PictogramSelectFieldWidget
    content_factory = IInternalLink


@ajax_form_config(name='properties.html',
                  context=IInternalLink, layer=IPyAMSLayer)
class InternalLinkPropertiesEditForm(LinkEditFormMixin, AdminModalEditForm):
    """internal link properties edit form"""

    fields = Fields(IInternalLink).select('reference', 'force_canonical_url', 'title',
                                          'description', 'pictogram_name')
    fields['pictogram_name'].widget_factory = PictogramSelectFieldWidget


#
# External links management
#

@viewlet_config(name='add-external-link.menu',
                context=ILinkContainerTarget, layer=IAdminLayer, view=IAssociationsTable,
                manager=IContextAddingsViewletManager, weight=55)
class ExternalLinkAddMenu(ProtectedViewObjectMixin, AssociationItemAddMenuMixin, MenuItem):
    """External link add menu"""

    label = ExternalLink.icon_hint
    icon_class = ExternalLink.icon_class

    href = 'add-external-link.html'


@ajax_form_config(name='add-external-link.html',
                  context=IAssociationContainer, layer=IPyAMSLayer)
class ExternalLinkAddForm(LinkAddFormMixin, AdminModalAddForm):
    """External link add form"""

    subtitle = _("New external link")
    legend = _("New external link properties")

    fields = Fields(IExternalLink).select('url', 'title', 'description',
                                          'language', 'pictogram_name')
    fields['pictogram_name'].widget_factory = PictogramSelectFieldWidget
    content_factory = IExternalLink


@ajax_form_config(name='properties.html',
                  context=IExternalLink, layer=IPyAMSLayer)
class ExternalLinkPropertiesEditForm(LinkEditFormMixin, AdminModalEditForm):
    """external link properties edit form"""

    fields = Fields(IExternalLink).select('url', 'title', 'description',
                                          'language', 'pictogram_name')
    fields['pictogram_name'].widget_factory = PictogramSelectFieldWidget


@subscriber(IDataExtractedEvent, form_selector=ExternalLinkAddForm)
@subscriber(IDataExtractedEvent, form_selector=ExternalLinkPropertiesEditForm)
def extract_external_link_data(event):
    """External link data extraction event"""
    form = event.form
    request = form.request
    settings = IExternalLinksManagerInfo(request.root, None)
    if (settings is None) or not settings.check_external_links:
        return
    url = event.data.get('url')
    for host in settings.forbidden_hosts or ():
        if host and url.startswith(host):
            form.widgets.errors += (Invalid(_("You can't create an external link to this site! "
                                              "Use an internal link instead...")),)
            return


#
# Mailto links management
#

@viewlet_config(name='add-mailto-link.menu',
                context=ILinkContainerTarget, layer=IAdminLayer, view=IAssociationsTable,
                manager=IContextAddingsViewletManager, weight=60)
class MailtoLinkAddMenu(ProtectedViewObjectMixin, AssociationItemAddMenuMixin, MenuItem):
    """Mailto link add menu"""

    label = MailtoLink.icon_hint
    icon_class = MailtoLink.icon_class

    href = 'add-mailto-link.html'


@ajax_form_config(name='add-mailto-link.html',
                  context=IAssociationContainer, layer=IPyAMSLayer)
class MailtoLinkAddForm(LinkAddFormMixin, AdminModalAddForm):
    """Mailto link add form"""

    subtitle = _("New mailto link")
    legend = _("New mailto link properties")

    fields = Fields(IMailtoLink).select('address', 'address_name', 'title',
                                        'description', 'pictogram_name')
    fields['pictogram_name'].widget_factory = PictogramSelectFieldWidget
    content_factory = IMailtoLink


@ajax_form_config(name='properties.html',
                  context=IMailtoLink, layer=IPyAMSLayer)
class MailtoLinkPropertiesEditForm(LinkEditFormMixin, AdminModalEditForm):
    """mailto link properties edit form"""

    fields = Fields(IMailtoLink).select('address', 'address_name', 'title',
                                        'description', 'pictogram_name')
    fields['pictogram_name'].widget_factory = PictogramSelectFieldWidget


#
# Links getter API
#

@view_config(name='get-links-list.json',
             request_type=IPyAMSLayer,
             permission=VIEW_SYSTEM_PERMISSION,
             renderer='json', xhr=True)
def get_links_list(request):
    """Links list getter"""
    result = []
    context = request.context
    links = IAssociationContainer(context, None)
    if not links:
        return result
    for link in links.values():
        if not (IInternalLink.providedBy(link) or IExternalLink.providedBy(link)):
            continue
        link_info = IAssociationInfo(link)
        result.append({
            'title': link_info.user_title,
            'value': link.get_editor_url()
        })
    return result
