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

"""PyAMS_content.shared.alert.zmi module

This module defines components used for alerts management interface.
"""

from zope.interface import Interface

from pyams_content.interfaces import CREATE_CONTENT_PERMISSION
from pyams_content.shared.alert import IAlertManager, IWfAlert
from pyams_content.shared.common.zmi import SharedContentAddForm, SharedContentPropertiesEditForm
from pyams_content.zmi.interfaces import IDashboardColumn, IDashboardContentType
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IGroup
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IFormLayer, IPyAMSLayer
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_utils.adapter import adapter_config
from pyams_zmi.form import FormGroupSwitcher
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IContentManagementMenu, IMenuHeader

__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(required=(IWfAlert, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentType)
def wf_alert_content_type(context, request, column):
    """Alert content type"""
    alert_type = context.get_alert_type()
    if alert_type is not None:
        i18n = II18n(alert_type)
        return i18n.query_attributes_in_order(('dashboard_label', 'label'),
                                              request=request)


@adapter_config(required=(IWfAlert, IAdminLayer, Interface, IContentManagementMenu),
                provides=IMenuHeader)
def alert_management_menu_header(context, request, view, manager):
    """Alert management menu header"""
    return request.localizer.translate(_("Alert management"))


@ajax_form_config(name='add-shared-content.html',
                  context=IAlertManager, layer=IFormLayer,
                  permission=CREATE_CONTENT_PERMISSION)
class AlertAddForm(SharedContentAddForm):
    """Alert add form"""

    fields = Fields(IWfAlert).select('title', 'alert_type', 'notepad')


@ajax_form_config(name='properties.html',
                  context=IWfAlert, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class AlertPropertiesEditForm(SharedContentPropertiesEditForm):
    """Alert properties edit form"""

    interface = IWfAlert


@adapter_config(name='alert-properties',
                required=(IWfAlert, IAdminLayer, AlertPropertiesEditForm),
                provides=IGroup)
class AlertPropertiesGroup(FormGroupSwitcher):
    """Alert properties group"""

    legend = _("Alert settings")

    fields = Fields(IWfAlert).select('alert_type', 'body', 'reference', 'external_url',
                                     'references', 'maximum_interval')
