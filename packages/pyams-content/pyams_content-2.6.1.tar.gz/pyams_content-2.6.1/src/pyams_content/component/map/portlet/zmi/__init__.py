# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from zope.interface import Interface

from pyams_content.component.map.portlet.interfaces import IMapPortletSettings
from pyams_form.field import Fields
from pyams_form.interfaces.form import IInnerSubForm
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import IPortletPreviewer
from pyams_portal.zmi import PortletPreviewer
from pyams_portal.zmi.interfaces import IPortletConfigurationEditor
from pyams_portal.zmi.portlet import PortletConfigurationEditForm
from pyams_portal.zmi.widget import RendererSelectFieldWidget
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_zmi.interfaces import IAdminLayer

__docformat__ = 'restructuredtext'


@adapter_config(name='configuration',
                required=(IMapPortletSettings, IAdminLayer, IPortletConfigurationEditor),
                provides=IInnerSubForm)
class MapPortletSettingsEditForm(PortletConfigurationEditForm):
    """Map portlet settings edit form"""

    fields = Fields(IMapPortletSettings).select('title', 'position',
                                                'renderer', 'devices_visibility', 'css_class')
    fields['renderer'].widget_factory = RendererSelectFieldWidget


@adapter_config(required=(Interface, IPyAMSLayer, Interface, IMapPortletSettings),
                provides=IPortletPreviewer)
@template_config(template='templates/map-preview.pt', layer=IPyAMSLayer)
class MapPortletPreviewer(PortletPreviewer):
    """Map portlet previewer"""
