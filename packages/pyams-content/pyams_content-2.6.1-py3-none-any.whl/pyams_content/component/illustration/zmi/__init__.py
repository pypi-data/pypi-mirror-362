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

"""PyAMS_content.component.illustration.zmi module

This module provides management interface components for illustrations.
"""

from pyramid.events import subscriber

from pyams_content.component.illustration import IIllustrationTargetBase, ILinkIllustration
from pyams_content.component.illustration.interfaces import IBaseIllustration, \
    IBaseIllustrationTarget, IIllustration, IIllustrationTarget, ILinkIllustrationTarget
from pyams_content.component.paragraph.interfaces import IBaseParagraph
from pyams_portal.interfaces import IPortletSettings
from pyams_zmi.interfaces.form import IPropertiesEditForm
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer, IFormContent, IFormUpdatedEvent, IInnerSubForm
from pyams_portal.zmi.portlet import PortletRendererSettingsEditForm
from pyams_portal.zmi.widget import RendererSelectFieldWidget
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_zmi.form import FormGroupSwitcher
from pyams_zmi.helper.event import get_json_widget_refresh_callback
from pyams_zmi.interfaces import IAdminLayer


__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(name='illustration',
                required=(IBaseIllustrationTarget, IAdminLayer, IPropertiesEditForm),
                provides=IInnerSubForm)
class BasicIllustrationPropertiesEditForm(FormGroupSwitcher):
    """Basic illustration properties edit form"""

    legend = _("Main illustration")
    weight = 10

    fields = Fields(IBaseIllustration)
    prefix = 'illustration.'

    @property
    def mode(self):
        """Form mode getter"""
        return self.parent_form.mode

    @property
    def state(self):
        """Form state getter"""
        return 'open' if self.get_content().has_data() else 'closed'


@adapter_config(required=(IIllustrationTargetBase, IAdminLayer, BasicIllustrationPropertiesEditForm),
                provides=IFormContent)
def base_illustration_edit_form_content(context, request, form):
    """Base illustration properties edit form content getter"""
    return IIllustration(context)


@adapter_config(name='illustration',
                required=(IIllustrationTarget, IAdminLayer, IPropertiesEditForm),
                provides=IInnerSubForm, force_implements=False)
class IllustrationPropertiesEditForm(BasicIllustrationPropertiesEditForm):
    """Illustration properties edit form"""

    fields = Fields(IIllustration)
    fields['renderer'].widget_factory = RendererSelectFieldWidget

    def update_widgets(self, prefix=None, use_form_mode=True):
        super().update_widgets(prefix, use_form_mode)
        renderer = self.widgets.get('renderer')
        if (renderer is not None) and IPortletSettings.providedBy(self.context):
            renderer.format_renderers = False

    @property
    def state(self):
        """Form state getter"""
        return super().state if IBaseParagraph.providedBy(self.context) else 'open'


@adapter_config(name='link-illustration',
                required=(ILinkIllustrationTarget, IAdminLayer, IPropertiesEditForm),
                provides=IInnerSubForm, force_implements=False)
class LinkIllustrationPropertiesEditForm(BasicIllustrationPropertiesEditForm):
    """Link illustration properties edit form"""

    legend = _("Navigation link illustration")
    weight = 15

    prefix = 'link_illustration.'


@adapter_config(required=(ILinkIllustrationTarget, IAdminLayer, LinkIllustrationPropertiesEditForm),
                provides=IFormContent)
def link_illustration_edit_form_content(context, request, form):
    """Link illustration properties edit form content getter"""
    return ILinkIllustration(context)


@adapter_config(required=(IBaseIllustrationTarget, IAdminLayer,
                          BasicIllustrationPropertiesEditForm),
                provides=IAJAXFormRenderer)
class BasicIllustrationPropertiesEditFormRenderer(ContextRequestViewAdapter):
    """Basic illustration properties AJAX form renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if changes is None:
            return None
        result = {
            'status': 'success',
            'message': self.request.localizer.translate(self.view.parent_form.success_message)
        }
        if 'data' in changes.get(IBaseIllustration, ()):
            result['callbacks'] = [
                get_json_widget_refresh_callback(self.view, 'data', self.request)
            ]
        return result


@subscriber(IFormUpdatedEvent,
            context_selector=IBaseIllustration,
            form_selector=PortletRendererSettingsEditForm)
def handle_illustration_renderer_settings_edit_form_update(event):
    """Illustration renderer settings edit form update"""
    widgets = event.form.widgets
    thumb_selection = widgets.get('thumb_selection')
    if thumb_selection is not None:
        thumb_selection.no_value_message = _("Use responsive selection")
