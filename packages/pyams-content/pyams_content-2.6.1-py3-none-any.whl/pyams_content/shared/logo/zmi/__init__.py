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
from pyams_content.shared.logo.interfaces import IWfLogo
from pyams_form.ajax import AJAXFormRenderer, ajax_form_config
from pyams_form.interfaces.form import IAJAXFormRenderer
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_utils.adapter import adapter_config
from pyams_zmi.helper.event import get_json_widget_refresh_callback
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IContentManagementMenu, IMenuHeader

__docformat__ = 'restructuredtext'

from pyams_content import _  # pylint: disable=ungrouped-imports


@adapter_config(required=(IWfLogo, IAdminLayer, Interface, IContentManagementMenu),
                provides=IMenuHeader)
def logo_management_menu_header(context, request, view, manager):
    """Logo management menu header"""
    return request.localizer.translate(_("Logo management"))


@ajax_form_config(name='properties.html',
                  context=IWfLogo, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class LogoPropertiesEditForm(SharedContentPropertiesEditForm):
    """Logo properties edit form"""
    
    interface = IWfLogo
    fieldnames = ('title', 'short_name', 'alt_title', 'content_url', 'header',
                  'description', 'acronym', 'image', 'monochrome_image', 'url',
                  'reference', 'notepad')
    
    
@adapter_config(required=(IWfLogo, IAdminLayer, LogoPropertiesEditForm),
                provides=IAJAXFormRenderer)
class LogoPropertiesEditFormRenderer(AJAXFormRenderer):
    """Logo properties edit form renderer"""
    
    def render(self, changes):
        result = super().render(changes)
        if 'image' in changes.get(IWfLogo, ()):
            result.setdefault('callbacks', []).append(
                    get_json_widget_refresh_callback(self.form, 'image', self.request))
        if 'monochrome_image' in changes.get(IWfLogo, ()):
            result.setdefault('callbacks', []).append(
                    get_json_widget_refresh_callback(self.form, 'monochrome_image', self.request))
        return result
    