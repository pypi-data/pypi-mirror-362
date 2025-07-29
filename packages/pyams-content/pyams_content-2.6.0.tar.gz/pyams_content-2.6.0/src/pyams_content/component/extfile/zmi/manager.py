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

"""PyAMS_content.component.extfile.zmi.manager module

This module provides management components to external files manager.
"""

from pyams_content.component.extfile import IExtFileManagerInfo
from pyams_content.component.extfile.interfaces import IExtFileManagerTarget
from pyams_content.interfaces import MANAGE_SITE_ROOT_PERMISSION
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IFormContent
from pyams_layer.interfaces import IPyAMSLayer
from pyams_utils.adapter import adapter_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminEditForm
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IPropertiesMenu
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem


__docformat__ = 'restructuredtext'

from pyams_content import _


@viewlet_config(name='extfile-manager.menu',
                context=IExtFileManagerTarget, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=770,
                permission=MANAGE_SITE_ROOT_PERMISSION)
class ExtFileManagerMenu(NavigationMenuItem):
    """External files manager menu"""

    label = _("External files settings")
    href = '#extfile-manager.html'


@ajax_form_config(name='extfile-manager.html',
                  context=IExtFileManagerTarget, layer=IPyAMSLayer,
                  permission=MANAGE_SITE_ROOT_PERMISSION)
class ExtFileManagerPropertiesEditForm(AdminEditForm):
    """External files manager properties edit form"""

    title = _("External files settings")
    legend = _("Default prefix")

    fields = Fields(IExtFileManagerInfo)


@adapter_config(required=(IExtFileManagerTarget, IPyAMSLayer, ExtFileManagerPropertiesEditForm),
                provides=IFormContent)
def extfile_manager_properties_form_content(context, request, form):
    """External file manager properties edit form content getter"""
    return IExtFileManagerInfo(context)
