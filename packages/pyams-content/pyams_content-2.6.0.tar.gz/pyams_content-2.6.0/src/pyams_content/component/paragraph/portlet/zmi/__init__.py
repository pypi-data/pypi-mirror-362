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

"""PyAMS_*** module

"""

__docformat__ = 'restructuredtext'

from zope.interface import Interface

from pyams_content import _
from pyams_content.component.paragraph import IParagraphContainerTarget
from pyams_content.component.paragraph.portlet import IParagraphContainerPortletSettings, \
    IParagraphNavigationPortletSettings
from pyams_form.interfaces.form import IInnerSubForm
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import IPortletPreviewer
from pyams_portal.zmi import PortletPreviewer
from pyams_portal.zmi.interfaces import IPortletConfigurationEditor
from pyams_portal.zmi.portlet import PortletConfigurationEditForm
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_utils.traversing import get_parent
from pyams_zmi.interfaces import IAdminLayer


class ParagraphPortletSettingsEditFormMixin:
    """Paragraph portlet settings edit form mixin class"""

    @property
    def fields(self):
        fields = super().fields
        container = get_parent(self.context, IParagraphContainerTarget)
        if container is None:
            fields = fields.omit('paragraphs')
        return fields

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        paragraphs = self.widgets.get('paragraphs')
        if paragraphs is not None:
            paragraphs.no_value_message = _("No filter, all paragraphs are selected")
            paragraphs.prompt_message = _("No filter, all paragraphs are selected")
            paragraphs.placeholder = _("No filter, all paragraphs are selected")
        factories = self.widgets.get('factories')
        if factories is not None:
            factories.no_value_message = _("No filter, all paragraphs types are selected")
            factories.prompt_message = _("No filter, all paragraphs are selected")
            factories.placeholder = _("No filter, all paragraphs are selected")


#
# Paragraph container portlet settings configuration
#

@adapter_config(name='configuration',
                required=(IParagraphContainerPortletSettings, IAdminLayer,
                          IPortletConfigurationEditor),
                provides=IInnerSubForm)
class ParagraphContainerPortletSettingsEditForm(ParagraphPortletSettingsEditFormMixin,
                                                PortletConfigurationEditForm):
    """Paragraph container portlet settings edit form"""


@adapter_config(required=(Interface, IPyAMSLayer, Interface, IParagraphContainerPortletSettings),
                provides=IPortletPreviewer)
@template_config(template='templates/container-preview.pt', layer=IPyAMSLayer)
class ParagraphContainerPortletPreviewer(PortletPreviewer):
    """Paragraph container portlet previewer"""


#
# Paragraph navigation portlet settings configuration
#

@adapter_config(name='configuration',
                required=(IParagraphNavigationPortletSettings, IAdminLayer,
                          IPortletConfigurationEditor),
                provides=IInnerSubForm)
class ParagraphNavigationPortletSettingsEditForm(ParagraphPortletSettingsEditFormMixin,
                                                 PortletConfigurationEditForm):
    """Paragraph navigation portlet settings edit form"""


@adapter_config(required=(Interface, IPyAMSLayer, Interface, IParagraphNavigationPortletSettings),
                provides=IPortletPreviewer)
@template_config(template='templates/navigation-preview.pt', layer=IPyAMSLayer)
class ParagraphNavigationPortletPreviewer(PortletPreviewer):
    """Paragraph navigation portlet previewer"""
