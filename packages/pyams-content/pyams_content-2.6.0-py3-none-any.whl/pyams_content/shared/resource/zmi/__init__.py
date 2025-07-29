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

from pyams_content.shared.common.zmi import SharedContentPropertiesEditForm
from pyams_content.shared.common.zmi.types.content import TypedSharedContentCustomInfoEditForm
from pyams_content.shared.resource import IResourceInfo, IWfResource
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IFormContent
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_skin.interfaces.widget import IHTMLEditorConfiguration
from pyams_utils.adapter import adapter_config
from pyams_utils.traversing import get_parent
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IContentManagementMenu, IMenuHeader, IPropertiesMenu
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(required=(IWfResource, IAdminLayer, Interface, IContentManagementMenu),
                provides=IMenuHeader)
def resource_management_menu_header(context, request, view, manager):
    """Resource management menu header"""
    return request.localizer.translate(_("Resource management"))


@ajax_form_config(name='properties.html',
                  context=IWfResource, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class ResourcePropertiesEditForm(SharedContentPropertiesEditForm):
    """Resource properties edit form"""

    interface = IWfResource


@viewlet_config(name='resource-info.menu',
                context=IWfResource, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=15,
                permission=VIEW_SYSTEM_PERMISSION)
class ResourceInformationMenu(NavigationMenuItem):
    """Resource information menu"""

    label = _("Resource details")
    href = '#resource-info.html'


@ajax_form_config(name='resource-info.html',
                  context=IWfResource, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class ResourceInformationEditForm(TypedSharedContentCustomInfoEditForm):
    """Resource information edit form"""

    title = _("Resource information")
    legend = _("Custom properties")

    @property
    def fields(self):
        """Form fields getter"""
        datatype = self.datatype
        if datatype is None:
            return Fields(Interface)
        return Fields(IResourceInfo).select(*datatype.field_names)

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        for fieldname in ('summary', 'synopsis', 'publisher_words'):
            widget = self.widgets.get(fieldname)
            if widget is not None:
                widget.add_class('h-200px')


@adapter_config(required=(IWfResource, IPyAMSLayer, ResourceInformationEditForm),
                provides=IFormContent)
def resource_info_edit_form_content(context, request, form):
    """Resource information edit form content getter"""
    return IResourceInfo(context)


@adapter_config(required=(IResourceInfo, IAdminLayer, ResourceInformationEditForm),
                provides=IViewContextPermissionChecker)
def resource_info_permission_checker(context, request, view):
    """Resource activity info permission checker"""
    resource = get_parent(context, IWfResource)
    return IViewContextPermissionChecker(resource)


@adapter_config(name='summary',
                required=(IResourceInfo, IAdminLayer, ResourceInformationEditForm),
                provides=IHTMLEditorConfiguration)
@adapter_config(name='synopsis',
                required=(IResourceInfo, IAdminLayer, ResourceInformationEditForm),
                provides=IHTMLEditorConfiguration)
@adapter_config(name='publisher_words',
                required=(IResourceInfo, IAdminLayer, ResourceInformationEditForm),
                provides=IHTMLEditorConfiguration)
def resource_html_editor_configuration(context, request, view):
    """Resource HTML editor configuration"""
    return {
        'menubar': False,
        'plugins': 'paste textcolor lists charmap link pyams_link',
        'toolbar': 'undo redo | pastetext | h3 h4 | bold italic superscript | '
                   'forecolor backcolor | bullist numlist | '
                   'charmap pyams_link link',
        'toolbar1': False,
        'toolbar2': False,
        'height': 200
    }
