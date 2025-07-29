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

"""PyAMS_content.reference.pictogram.zmi.manager module

This module defines components which are used to handle pictograms selection in a
pictograms *manager*, which is used to select pictograms which will be available in a
given context.
"""

from pyams_content.interfaces import MANAGE_TOOL_PERMISSION
from pyams_content.reference.pictogram.interfaces import IPictogramManager, \
    IPictogramManagerTarget
from pyams_content.reference.pictogram.zmi.widget.manager import \
    PictogramManagerSelectionFieldWidget
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_layer.interfaces import IPyAMSLayer
from pyams_skin.interfaces.viewlet import IHelpViewletManager
from pyams_skin.viewlet.help import AlertMessage
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminEditForm
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IPropertiesMenu
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem


__docformat__ = 'restructuredtext'

from pyams_content import _


@viewlet_config(name='pictograms-manager.menu',
                context=IPictogramManagerTarget, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=760,
                permission=MANAGE_TOOL_PERMISSION)
class PictogramManagerMenu(NavigationMenuItem):
    """Pictogram manager menu"""

    label = _("Pictograms selection")
    href = '#pictograms-selection.html'


@ajax_form_config(name='pictograms-selection.html',
                  context=IPictogramManagerTarget, layer=IPyAMSLayer,
                  permission=MANAGE_TOOL_PERMISSION)
class PictogramManagerEditForm(AdminEditForm):
    """Pictogram manager selection form"""

    title = _("Pictograms management")
    legend = _("Selection of available pictograms")

    fields = Fields(IPictogramManager)
    fields['selected_pictograms'].widget_factory = PictogramManagerSelectionFieldWidget

    _edit_permission = MANAGE_TOOL_PERMISSION


@viewlet_config(name='languages.help',
                context=IPictogramManagerTarget, layer=IAdminLayer, view=PictogramManagerEditForm,
                manager=IHelpViewletManager, weight=10)
class PictogramManagerEditFormHelp(AlertMessage):
    """Pictogram manager edit form help"""

    _message = _("You can select which pictograms will be made available to contents published "
                 "inside this context.\n\n"
                 "To include a pictogram, you can move it from *available pictograms* list to "
                 "*selected pictograms* list by just doing a double click onto it; the reverse "
                 "operation is working in the same way...")

    message_renderer = 'markdown'
