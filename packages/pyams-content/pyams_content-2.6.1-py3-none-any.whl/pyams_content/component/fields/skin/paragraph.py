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

"""PyAMS_content.component.fields.skin.paragraph module

This module provides components for rendering of form fields paragraphs.
"""

from zope.interface import Interface

from pyams_content.component.fields.interfaces import IFormFieldsParagraph
from pyams_content.component.paragraph.portlet.skin import IParagraphContainerPortletRenderer
from pyams_content.feature.renderer import DefaultContentRenderer, IContentRenderer
from pyams_portal.interfaces import DEFAULT_RENDERER_NAME
from pyams_content.shared.form import IWfForm
from pyams_fields.interfaces import IFormFieldContainerTarget, IFormHandlersInfo
from pyams_fields.skin import FormFieldContainerInputForm
from pyams_fields.skin.interfaces import IFormFieldContainerInputForm
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer, IPyAMSUserLayer
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_utils.traversing import get_parent
from pyams_viewlet.viewlet import ViewContentProvider


__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(name='preview.html',
                required=(IFormFieldContainerTarget, IPyAMSLayer),
                provides=IFormFieldContainerInputForm)
class FormFieldContainerInputFormPreview(FormFieldContainerInputForm):
    """Form field container input form fields preview"""


@adapter_config(name=DEFAULT_RENDERER_NAME,
                required=(IFormFieldsParagraph, IPyAMSLayer),
                provides=IContentRenderer)
@template_config(template='templates/paragraph-default.pt', layer=IPyAMSLayer)
class FormFieldsParagraphDefaultRenderer(DefaultContentRenderer):
    """Form fields paragraph default renderer"""

    label = _("Form fields list (default)")

    input_form = None

    def __init__(self, context, request, view=None):
        super().__init__(context, request, view)
        target = get_parent(context, IFormFieldContainerTarget)
        if target is not None:
            form = self.input_form = request.registry.queryMultiAdapter((target, request),
                                                                        IFormFieldContainerInputForm,
                                                                        name=request.view_name)
            if (form is not None) and IWfForm.providedBy(form.context):
                form.legend = II18n(form.context).query_attribute('form_legend', request=request)

    def update(self):
        """Paragraph update"""
        super().update()
        if self.input_form is not None:
            self.input_form.update()

    def render(self, template_name=''):
        """Paragraph render"""
        if self.input_form is None:
            return ''
        return super().render(template_name)


@adapter_config(name='submit.html',
                required=(IFormFieldContainerTarget, IPyAMSUserLayer, Interface),
                provides=IParagraphContainerPortletRenderer)
@template_config(template='templates/form-submit.pt', layer=IPyAMSUserLayer)
class FormSubmitPortletRenderer(ViewContentProvider):
    """Form submit message portlet renderer"""

    use_portlets_cache = False

    @property
    def submit_message(self):
        """Submit message getter"""
        handlers_info = IFormHandlersInfo(self.context, None)
        if handlers_info is None:
            return None
        message = II18n(handlers_info).query_attribute('submit_message', request=self.request)
        reference = self.request.annotations.get('submit.reference')
        if reference:
            message = message.replace('{_reference}', reference)
        return message

    def render(self, template_name=''):
        form = self.view.input_form
        if form.widgets.errors:
            return form.render()
        return super().render(template_name)
