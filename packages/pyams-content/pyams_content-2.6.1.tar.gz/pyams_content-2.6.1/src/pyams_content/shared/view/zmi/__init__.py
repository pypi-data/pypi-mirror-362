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

"""PyAMS_content.shared.view.zmi module

This module defines components used for view properties management.
"""

import json

from zope.interface import Interface, alsoProvides

from pyams_content.shared.common.types import get_all_data_types
from pyams_content.shared.common.zmi import SharedContentPropertiesEditForm
from pyams_content.shared.view import IWfView
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IGroup
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_skin.interfaces.viewlet import IHelpViewletManager
from pyams_skin.viewlet.help import AlertMessage
from pyams_utils.adapter import adapter_config
from pyams_utils.interfaces.data import IObjectData
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import FormGroupSwitcher
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IContentManagementMenu, IMenuHeader

__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(required=(IWfView, IAdminLayer, Interface, IContentManagementMenu),
                provides=IMenuHeader)
def view_management_menu_header(context, request, view, manager):
    """View management menu header"""
    return request.localizer.translate(_("View management"))


@ajax_form_config(name='properties.html',
                  context=IWfView, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class ViewPropertiesEditForm(SharedContentPropertiesEditForm):
    """View properties edit form"""

    interface = IWfView


@adapter_config(name='view-properties',
                required=(IWfView, IAdminLayer, ViewPropertiesEditForm),
                provides=IGroup)
class ViewPropertiesGroup(FormGroupSwitcher):
    """View properties group"""

    legend = _("View settings")

    fields = Fields(IWfView).select('select_context_path', 'select_context_type',
                                    'selected_content_types', 'select_context_datatype',
                                    'selected_datatypes', 'excluded_content_types',
                                    'excluded_datatypes', 'allow_user_params',
                                    'order_by', 'reversed_order', 'limit', 'age_limit')
    switcher_mode = 'always'

    def update_widgets(self, prefix=None, use_form_mode=True):
        super().update_widgets(prefix, use_form_mode)
        for field in ('selected_datatypes', 'excluded_datatypes'):
            all_datatypes = get_all_data_types(self.request, self.context, field)
            datatypes = self.widgets.get(field)
            if datatypes is not None:
                datatypes.object_data = {
                    'data': json.dumps(all_datatypes)
                }
                alsoProvides(datatypes, IObjectData)


@viewlet_config(name='view-properties.help',
                context=IWfView, layer=IAdminLayer, view=ViewPropertiesGroup,
                manager=IHelpViewletManager, weight=10)
class ViewPropertiesHelp(AlertMessage):
    """View properties help"""

    status = 'info'
    _message = _("These settings apply to search made by the view.\n"
                 "If you select the option \"Include ONLY selected references\", "
                 "via the \"References\" menu, only selected references will be selected "
                 "(if published) and no real search will be made !\n"
                 "In other modes, and if no search criteria is defined (in this form, or "
                 "in other settings forms), ALL published contents will be selected by the view !!")

    message_renderer = 'text'
