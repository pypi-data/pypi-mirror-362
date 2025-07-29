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

"""PyAMS_fields.zmi.mail module

Management interface components for 'mailto' form handler.
"""

from pyams_content.component.fields.handler.interfaces import IMailtoHandlerInfo
from pyams_content.shared.common.zmi import ISharedContentPropertiesMenu
from pyams_fields.interfaces import IFormHandlersInfo, IFormHandlersTarget
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IFormContent
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_utils.adapter import adapter_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminEditForm
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem


__docformat__ = 'restructuredtext'

from pyams_content import _


@viewlet_config(name='mailto-handler.menu',
                context=IFormHandlersTarget, layer=IAdminLayer,
                manager=ISharedContentPropertiesMenu, weight=10,
                permission=VIEW_SYSTEM_PERMISSION)
class MailtoFormHandlerSettingsMenu(NavigationMenuItem):
    """Mailto form handler settings menu"""

    label = _("Mailto handler settings")
    href = '#mailto-handler.html'

    def __new__(cls, context, request, view, manager):
        handlers = IFormHandlersInfo(context, None)
        if handlers is None:
            return None
        mailto_info = IMailtoHandlerInfo(handlers, None)
        if mailto_info is None:
            return None
        return NavigationMenuItem.__new__(cls)


@ajax_form_config(name='mailto-handler.html',
                  context=IFormHandlersTarget, layer=IPyAMSLayer)
class MailtoFormHandlerSettingsEditForm(AdminEditForm):
    """Mailto form handlers settings form"""

    title = _("Mailto notifications")
    legend = _("Mailto form handler settings")

    fields = Fields(IMailtoHandlerInfo)


@adapter_config(required=(IFormHandlersTarget, IPyAMSLayer, MailtoFormHandlerSettingsEditForm),
                provides=IFormContent)
def form_handlers_settings_edit_form_content(context, request, form):
    """Form handlers settings edit form content getter"""
    handlers = IFormHandlersInfo(context)
    return IMailtoHandlerInfo(handlers, None)
