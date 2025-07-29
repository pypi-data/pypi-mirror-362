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

"""PyAMS_content.component.frame.portlet.skin.zmi module

This module defines components for framed text portlet renderers settings management interface.
"""

from pyams_content.component.frame.skin import IFrameDefaultRendererSettings, IFrameLateralRendererSettings
from pyams_content.reference.pictogram.zmi.widget import PictogramSelectFieldWidget
from pyams_form.field import Fields
from pyams_form.interfaces.form import IFormFields
from pyams_portal.zmi.interfaces import IPortletRendererSettingsEditForm
from pyams_utils.adapter import adapter_config
from pyams_zmi.interfaces import IAdminLayer

__docformat__ = 'restructuredtext'


@adapter_config(required=(IFrameDefaultRendererSettings, IAdminLayer, IPortletRendererSettingsEditForm),
                provides=IFormFields)
def frame_portlet_default_settings_form_fields(context, request, view):
    """Frame portlet default settings form fields"""
    fields = Fields(IFrameDefaultRendererSettings)
    fields['pictogram_name'].widget_factory = PictogramSelectFieldWidget
    return fields


@adapter_config(required=(IFrameLateralRendererSettings, IAdminLayer, IPortletRendererSettingsEditForm),
                provides=IFormFields)
def frame_portlet_lateral_settings_form_fields(context, request, view):
    """Frame portlet lateral settings form fields"""
    fields = Fields(IFrameLateralRendererSettings).select('position', 'width',
                                                          'status', 'pictogram_name')
    fields['pictogram_name'].widget_factory = PictogramSelectFieldWidget
    return fields
