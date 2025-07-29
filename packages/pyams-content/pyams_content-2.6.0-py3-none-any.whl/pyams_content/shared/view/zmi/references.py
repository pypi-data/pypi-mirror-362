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

"""PyAMS_content.shared.view.zmi.references module

This module defines component used for view references management interface.
"""

from pyams_content.shared.view import IWfView
from pyams_content.shared.view.interfaces.settings import IViewInternalReferencesSettings
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminEditForm
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IPropertiesMenu
from pyams_zmi.zmi.viewlet.menu import NavigationMenuDivider, NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_content import _


@viewlet_config(name='references.divider',
                context=IWfView, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=299,
                permission=VIEW_SYSTEM_PERMISSION)
class ViewReferencesMenuDivider(NavigationMenuDivider):
    """View references menu divider"""


@viewlet_config(name='references.menu',
                context=IWfView, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=300,
                permission=VIEW_SYSTEM_PERMISSION)
class ViewReferencesMenu(NavigationMenuItem):
    """View references menu"""

    label = _("References")
    href = '#references.html'


@ajax_form_config(name='references.html',
                  context=IWfView, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class ViewReferencesEditForm(AdminEditForm):
    """View references settings edit form"""

    title = _("References settings")
    legend = _("View internal references settings")

    fields = Fields(IViewInternalReferencesSettings)
