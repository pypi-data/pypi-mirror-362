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

"""PyAMS_content.shared.form.zmi module

This module defines forms management components.
"""

from zope.interface import Interface

from pyams_content.shared.common.zmi.types.content import TypedSharedContentPropertiesEditForm
from pyams_content.shared.form import IWfForm
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IGroup
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_utils.adapter import adapter_config
from pyams_zmi.form import FormGroupSwitcher
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IContentManagementMenu, IMenuHeader


__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(required=(IWfForm, IAdminLayer, Interface, IContentManagementMenu),
                provides=IMenuHeader)
def form_management_menu_header(context, request, view, manager):
    """Form management menu header"""
    return request.localizer.translate(_("Form management"))


@ajax_form_config(name='properties.html',
                  context=IWfForm, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class FormPropertiesEditForm(TypedSharedContentPropertiesEditForm):
    """Form properties edit form"""

    interface = IWfForm


@adapter_config(required=(IWfForm, IAdminLayer, FormPropertiesEditForm),
                provides=IGroup)
class FormPropertiesEditFormHeaderGroup(FormGroupSwitcher):
    """Form properties edit form header group"""

    legend = _("Form header")
    fields = Fields(IWfForm).select('alt_title', 'form_header', 'form_legend')

    weight = 1
