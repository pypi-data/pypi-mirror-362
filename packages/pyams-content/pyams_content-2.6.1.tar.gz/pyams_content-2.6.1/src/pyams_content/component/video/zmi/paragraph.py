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

"""PyAMS_content.component.video.zmi.paragraph module

This module defines components which are required to handle external
videos paragraphs management interface.
"""

from pyramid.decorator import reify
from pyramid.events import subscriber
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.response import Response
from pyramid.view import view_config
from zope.interface import Interface, Invalid, alsoProvides

from pyams_content.component.paragraph import IParagraphContainer, IParagraphContainerTarget
from pyams_content.component.paragraph.zmi import BaseParagraphAddForm, BaseParagraphAddMenu, \
    IInnerParagraphEditForm, IParagraphContainerBaseTable, InnerParagraphPropertiesEditForm, \
    ParagraphPropertiesEditFormMixin
from pyams_content.component.video import IExternalVideoProvider, IExternalVideoSettings, external_video_settings
from pyams_content.component.video.interfaces import EXTERNAL_VIDEO_PARAGRAPH_ICON_CLASS, EXTERNAL_VIDEO_PARAGRAPH_NAME, \
    EXTERNAL_VIDEO_PARAGRAPH_TYPE, IExternalVideoParagraph
from pyams_content.interfaces import MANAGE_CONTENT_PERMISSION
from pyams_form.ajax import ajax_form_config
from pyams_form.button import Buttons
from pyams_form.field import Fields
from pyams_form.group import Group
from pyams_form.interfaces.form import IDataExtractedEvent, IGroup
from pyams_layer.interfaces import IPyAMSLayer
from pyams_layer.skin import apply_skin
from pyams_portal.zmi.widget import RendererSelectFieldWidget
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_utils.adapter import adapter_config
from pyams_utils.interfaces import ICacheKeyValue
from pyams_utils.interfaces.data import IObjectData
from pyams_utils.interfaces.form import NO_VALUE_STRING
from pyams_utils.registry import get_utility
from pyams_utils.traversing import get_parent
from pyams_utils.url import absolute_url
from pyams_viewlet.viewlet import RawContentProvider, viewlet_config
from pyams_zmi.form import AdminAddForm, AdminEditForm, AdminModalEditForm
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager
from pyams_zmi.skin import AdminSkin

__docformat__ = 'restructuredtext'

from pyams_content import _


@viewlet_config(name='add-external-video-paragraph.menu',
                context=IParagraphContainerTarget, layer=IAdminLayer,
                view=IParagraphContainerBaseTable,
                manager=IContextAddingsViewletManager, weight=75)
class ExternalVideoParagraphAddMenu(BaseParagraphAddMenu):
    """External video paragraph add menu"""

    label = EXTERNAL_VIDEO_PARAGRAPH_NAME
    icon_class = EXTERNAL_VIDEO_PARAGRAPH_ICON_CLASS

    factory_name = EXTERNAL_VIDEO_PARAGRAPH_TYPE
    href = 'add-external-video-paragraph.html'


@ajax_form_config(name='add-external-video-paragraph.html',
                  context=IParagraphContainer, layer=IPyAMSLayer)
class ExternalVideoParagraphAddForm(BaseParagraphAddForm):
    """External video paragraph add form"""

    @property
    def fields(self):
        fields = Fields(IExternalVideoParagraph).select('title', 'author', 'description',
                                                        'provider_name', 'renderer')
        provider_name = self.request.params.get('addform.widgets.provider_name')
        if provider_name:
            provider = get_utility(IExternalVideoProvider, name=provider_name)
            fields += Fields(provider.settings_interface)
        return fields

    content_factory = IExternalVideoParagraph

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        provider_name = self.widgets.get('provider_name')
        if provider_name is not None:
            provider_name.required = True
            provider_name.prompt = True
            provider_name.prompt_message = _("Select video provider...")
            provider_name.object_data = {
                'ams-change-handler': 'MyAMS.helpers.select2ChangeHelper',
                'ams-stop-propagation': 'true',
                'ams-select2-helper-type': 'html',
                'ams-select2-helper-url': absolute_url(self.context, self.request,
                                                       'get-video-provider-settings-add-form.html'),
                'ams-select2-helper-argument': 'provider_name',
                'ams-select2-helper-target': '#video-settings-helper'
            }
            provider_name.suffix = RawContentProvider(html='<div id="video-settings-helper" '
                                                      '     class="py-2 no-footer"></div>')
            alsoProvides(provider_name, IObjectData)


@subscriber(IDataExtractedEvent, form_selector=ExternalVideoParagraphAddForm)
def handle_video_paragraph_add_form_data_extraction(event):
    """Handle provider name data extraction"""
    data = event.data
    if not data.get('provider_name'):
        event.form.widgets.errors += (Invalid(_("Video provider is required")),)


class ExternalVideoProviderSettingsAddForm(AdminAddForm):
    """External video provider settings add form"""

    buttons = Buttons(Interface)

    def __init__(self, context, request, provider):
        super().__init__(context, request)
        self.provider = provider


@adapter_config(required=(IParagraphContainer, IPyAMSLayer, ExternalVideoProviderSettingsAddForm),
                provides=IGroup)
class ExternalVideoProviderSettingsAddFormGroup(Group):
    """External video provider settings add form group"""

    legend = _("Provider settings")
    prefix = BaseParagraphAddForm.prefix

    @reify
    def fields(self):
        return Fields(self.parent_form.provider.settings_interface)


@view_config(name='get-video-provider-settings-add-form.html',
             context=IParagraphContainer, request_type=IPyAMSLayer,
             permission=MANAGE_CONTENT_PERMISSION, xhr=True)
def video_provider_settings_add_form(request):
    """Video provider settings add form"""
    apply_skin(request, AdminSkin)
    provider_name = request.params.get('provider_name')
    if provider_name is None:
        raise HTTPBadRequest("Missing provider name argument")
    if (not provider_name) or (provider_name == NO_VALUE_STRING):
        return Response('')
    provider = get_utility(IExternalVideoProvider, name=provider_name)
    form = ExternalVideoProviderSettingsAddForm(request.context, request, provider)
    form.update()
    return Response(form.render())


#
# External video paragraph edit form
#

class ExternalVideoParagraphPropertiesEditFormMixin(ParagraphPropertiesEditFormMixin):
    """External video paragraph propertied edit form mixin"""

    @reify
    def fields(self):
        fields = Fields(IExternalVideoParagraph).select('title', 'author', 'description', 'provider_name',
                                                        'renderer')
        fields['renderer'].widget_factory = RendererSelectFieldWidget
        provider_name = self.request.params.get(f'{self.prefix}widgets.provider_name')
        if provider_name:
            provider = get_utility(IExternalVideoProvider, name=provider_name)
            fields += Fields(provider.settings_interface)
        return fields

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        provider_name = self.widgets.get('provider_name')
        if provider_name is not None:
            key = ICacheKeyValue(self.context)
            provider_name.required = True
            provider_name.prompt = True
            provider_name.prompt_message = _("Select video provider...")
            provider_name.object_data = {
                'ams-change-handler': 'MyAMS.helpers.select2ChangeHelper',
                'ams-stop-propagation': 'true',
                'ams-select2-helper-type': 'html',
                'ams-select2-helper-url': absolute_url(self.context, self.request,
                                                       'get-video-provider-settings-edit-form.html'),
                'ams-select2-helper-argument': 'provider_name',
                'ams-select2-helper-target': f'#video-settings-helper-{key}'
            }
            alsoProvides(provider_name, IObjectData)
            provider = self.context.get_provider()
            group = ExternalVideoProviderSettingsEditFormGroup(self.context, self.request, self, provider)
            group.update()
            provider_name.suffix = RawContentProvider(html=f'<div id="video-settings-helper-{key}" '
                                                           f'     class="py-2 no-footer">'
                                                           f'    {group.render()}'
                                                           f'</div>')


class ExternalVideoProviderSettingsEditForm(AdminEditForm):
    """External video provider settings edit form"""

    buttons = Buttons(Interface)
    hide_section = True

    def __init__(self, context, request, provider):
        super().__init__(context, request)
        self.provider = provider

    @property
    def prefix(self):
        return f'form_{self.context.__name__}.'


@adapter_config(required=(IExternalVideoSettings, IPyAMSLayer, ExternalVideoProviderSettingsEditForm),
                provides=IGroup)
class ExternalVideoProviderSettingsEditFormGroup(Group):
    """External video provider settings edit form group"""

    legend = _("Provider settings")

    def __init__(self, context, request, parent_form, provider=None):
        super().__init__(context, request, parent_form)
        self.provider = provider if provider is not None else parent_form.provider

    @property
    def prefix(self):
        video = get_parent(self.context, IExternalVideoParagraph)
        return f'form_{video.__name__}.'

    @reify
    def fields(self):
        return Fields(self.provider.settings_interface)


@adapter_config(required=(IExternalVideoParagraph, IAdminLayer),
                provides=IInnerParagraphEditForm)
class ExternalVideoParagraphInnerPropertiesEditForm(ExternalVideoParagraphPropertiesEditFormMixin,
                                                    InnerParagraphPropertiesEditForm):
    """External video paragraph inner properties edit form"""


@ajax_form_config(name='properties.html',
                  context=IExternalVideoParagraph, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class ExternalVideoParagraphPropertiesEditForm(ExternalVideoParagraphPropertiesEditFormMixin,
                                               AdminModalEditForm):
    """External video paragraph properties edit form"""

    @property
    def provider(self):
        return self.context.get_provider()


@view_config(name='get-video-provider-settings-edit-form.html',
             context=IExternalVideoParagraph, request_type=IPyAMSLayer,
             permission=MANAGE_CONTENT_PERMISSION, xhr=True)
def video_provider_settings_edit_form(request):
    """Video provider settings edit form"""
    apply_skin(request, AdminSkin)
    provider_name = request.params.get('provider_name')
    if provider_name is None:
        raise HTTPBadRequest("Missing provider name argument")
    if (not provider_name) or (provider_name == NO_VALUE_STRING):
        return Response('')
    settings = external_video_settings(request.context, provider_name)
    provider = get_utility(IExternalVideoProvider, name=provider_name)
    form = ExternalVideoProviderSettingsEditForm(settings, request, provider)
    form.update()
    return Response(form.render())
