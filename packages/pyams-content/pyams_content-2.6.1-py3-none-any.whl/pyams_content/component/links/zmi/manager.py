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

"""PyAMS_content.component.links.zmi.manager module

This module defines management components for external links manager info.
"""

from zope.interface import Interface

from pyams_content.component.links.interfaces import IExternalLinksManagerInfo, IExternalLinksManagerTarget
from pyams_content.interfaces import MANAGE_SITE_ROOT_PERMISSION
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IFormContent, IGroup
from pyams_layer.interfaces import IPyAMSLayer
from pyams_utils.adapter import adapter_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminEditForm, FormGroupChecker
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IPropertiesMenu
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_content import _


@viewlet_config(name='external-links-manager.menu',
                context=IExternalLinksManagerTarget, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=780,
                permission=MANAGE_SITE_ROOT_PERMISSION)
class ExternalLinksManagerMenu(NavigationMenuItem):
    """External links manager menu"""

    label = _("External links settings")
    href = '#external-links-manager.html'


@ajax_form_config(name='external-links-manager.html',
                  context=IExternalLinksManagerTarget, layer=IPyAMSLayer,
                  permission=MANAGE_SITE_ROOT_PERMISSION)
class ExternalLinksManagerPropertiesEditForm(AdminEditForm):
    """External links manager properties edit form"""

    title = _("External links settings")

    fields = Fields(Interface)


@adapter_config(name='check-external-links.group',
                required=(IExternalLinksManagerTarget, IAdminLayer, ExternalLinksManagerPropertiesEditForm),
                provides=IGroup)
class ExternalLinksManagerPropertiesCheckGroup(FormGroupChecker):
    """External links manager properties checker group"""

    fields = Fields(IExternalLinksManagerInfo)

    def update_widgets(self, prefix=None, use_form_mode=True):
        super().update_widgets(prefix, use_form_mode)
        hosts = self.widgets.get('forbidden_hosts')
        if hosts is not None:
            hosts.rows = 10


@adapter_config(required=(IExternalLinksManagerTarget, IPyAMSLayer, ExternalLinksManagerPropertiesCheckGroup),
                provides=IFormContent)
def external_links_manager_properties_form_content(context, request, form):
    """External links manager properties edit form content getter"""
    return IExternalLinksManagerInfo(context)
