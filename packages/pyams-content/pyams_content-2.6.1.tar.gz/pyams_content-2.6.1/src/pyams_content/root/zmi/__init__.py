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

"""PyAMS_content.root.zmi module

Site root management components.
"""

from zope.interface import Interface

from pyams_content.root import ISiteRootInfos
from pyams_content.zmi.properties import PropertiesEditForm
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer, IFormContent
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_site.interfaces import ISiteRoot
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_viewlet.manager import viewletmanager_config
from pyams_zmi.interfaces import IAdminLayer, IObjectLabel
from pyams_zmi.interfaces.configuration import IZMIConfiguration
from pyams_zmi.interfaces.viewlet import IMenuHeader, IPropertiesMenu, ISiteManagementMenu
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem


__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(required=(ISiteRoot, IAdminLayer, Interface, ISiteManagementMenu),
                provides=IMenuHeader)
def site_root_management_menu_header(context, request, view, manager):
    """Site root management menu header adapter"""
    return _("Main site management")


@adapter_config(required=(ISiteRoot, IAdminLayer, Interface),
                provides=IObjectLabel)
def site_root_label(context, request, view):
    """Site root label"""
    return IZMIConfiguration(request.root).site_name


@viewletmanager_config(name='properties.menu',
                       context=ISiteRoot, layer=IAdminLayer,
                       manager=ISiteManagementMenu, weight=10,
                       provides=IPropertiesMenu,
                       permission=VIEW_SYSTEM_PERMISSION)
class SiteRootPropertiesMenu(NavigationMenuItem):
    """Site root properties menu"""

    label = _("Properties")
    icon_class = 'fas fa-edit'
    href = '#properties.html'


@ajax_form_config(name='properties.html',
                  context=ISiteRoot, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class SiteRootPropertiesEditForm(PropertiesEditForm):
    """Site root properties edit form"""

    title = _("Main site properties")
    legend = _("Site information")

    fields = Fields(ISiteRootInfos)

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        description = self.widgets.get('description')
        if description is not None:
            description.set_widgets_attr('rows', 5)


@adapter_config(required=(ISiteRoot, IPyAMSLayer, SiteRootPropertiesEditForm),
                provides=IFormContent)
def site_root_properties_form_content(context, request, form):
    """Site root properties edit form content getter"""
    return ISiteRootInfos(context)


@adapter_config(required=(ISiteRoot, IAdminLayer, SiteRootPropertiesEditForm),
                provides=IAJAXFormRenderer)
class SiteRootPropertiesEditFormRenderer(ContextRequestViewAdapter):
    """Site root properties edit form renderer"""

    def render(self, changes):
        """Form renderer"""
        if changes is None:
            return None
        return {
            'status': 'reload',
            'smallbox': {
                'status': 'success',
                'message': self.request.localizer.translate(self.view.success_message)
            }
        }
