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

"""PyAMS_*** module

"""

from pyramid.events import subscriber
from zope.interface import Invalid

from pyams_content.feature.filter.interfaces import IAggregatedPortletRendererSettings
from pyams_content.shared.view.portlet.interfaces import IViewItemsPortletSettings
from pyams_form.interfaces.form import IDataExtractedEvent
from pyams_portal.interfaces import IPortletRenderer
from pyams_portal.zmi.portlet import PortletConfigurationEditForm
from pyams_utils.factory import create_object

__docformat__ = 'restructuredtext'

from pyams_content import _


@subscriber(IDataExtractedEvent, form_selector=PortletConfigurationEditForm)
def handle_view_items_portlet_settings_configuration_data(event):
    """Handle view items portlet settings configuration data extraction"""
    form = event.form
    settings = IViewItemsPortletSettings(form.form_content, None)
    if settings is None:
        return
    if len(event.data.get('views', ())) < 2:
        return
    request = form.request
    registry = request.registry
    renderer_name = event.data.get('renderer')
    renderer = registry.queryMultiAdapter((request.root, request, None, settings),
                                          IPortletRenderer, name=renderer_name)
    if renderer is not None:
        renderer_settings = create_object(renderer.settings_interface)
        if IAggregatedPortletRendererSettings.providedBy(renderer_settings):
            form.widgets.errors += (Invalid(_("Multiple views are not supported with aggregated "
                                              "portlets renderers!")),)
