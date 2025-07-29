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

from pyams_content.interfaces import CREATE_CONTENT_PERMISSION
from pyams_content.shared.common.zmi import SharedContentAddForm, SharedContentPropertiesEditForm
from pyams_content.shared.file.interfaces import IFileManager, IWfFile
from pyams_form.ajax import AJAXFormRenderer, ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer
from pyams_layer.interfaces import IFormLayer, IPyAMSLayer
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_utils.adapter import adapter_config
from pyams_zmi.helper.event import get_json_widget_refresh_callback
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IContentManagementMenu, IMenuHeader

__docformat__ = 'restructuredtext'

from pyams_content import _


@ajax_form_config(name='add-shared-content.html',
                  context=IFileManager, layer=IFormLayer,
                  permission=CREATE_CONTENT_PERMISSION)
class FileAddForm(SharedContentAddForm):
    """Shared file add form"""
    
    fields = Fields(IWfFile).select('title', 'data', 'filename', 'notepad')


@adapter_config(required=(IWfFile, IAdminLayer, Interface, IContentManagementMenu),
                provides=IMenuHeader)
def file_management_menu_header(context, request, view, manager):
    """File management menu header"""
    return request.localizer.translate(_("File management"))


@ajax_form_config(name='properties.html',
                  context=IWfFile, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class FilePropertiesEditForm(SharedContentPropertiesEditForm):
    """File properties edit form"""
    
    interface = IWfFile
    fieldnames = ('title', 'short_name', 'content_url', 'data', 'filename', 'notepad')


@adapter_config(required=(IWfFile, IAdminLayer, FilePropertiesEditForm),
                provides=IAJAXFormRenderer)
class FilePropertiesEditFormRenderer(AJAXFormRenderer):
    """File properties edit form renderer"""
    
    def render(self, changes):
        result = super().render(changes)
        if 'data' in changes.get(IWfFile, ()):
            result.setdefault('callbacks', []).append(
                    get_json_widget_refresh_callback(self.form, 'data', self.request))
        return result
