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

"""PyAMS_content.feature.script.zmi.settings module

This module defines management components for scripts container settings.
"""

from zope.interface import alsoProvides

from pyams_content.feature.script import IScriptContainerTarget
from pyams_content.feature.script.interfaces import IScriptContainerSettings
from pyams_content.feature.script.zmi.interfaces import IScriptContainerNavigationMenu
from pyams_content.interfaces import MANAGE_SITE_ROOT_PERMISSION
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IFormContent
from pyams_layer.interfaces import IPyAMSLayer
from pyams_utils.adapter import adapter_config
from pyams_utils.interfaces.data import IObjectData
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminEditForm
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_content import _


@viewlet_config(name='scripts-settings.menu',
                context=IScriptContainerTarget, layer=IAdminLayer,
                manager=IScriptContainerNavigationMenu, weight=10,
                permission=MANAGE_SITE_ROOT_PERMISSION)
class ScriptSettingsNavigationMenuItem(NavigationMenuItem):
    """Scripts settings navigation menu item"""

    label = _("Scripts variables")
    href = '#scripts-settings.html'


@ajax_form_config(name='scripts-settings.html',
                  context=IScriptContainerTarget, layer=IPyAMSLayer,
                  permission=MANAGE_SITE_ROOT_PERMISSION)
class ScriptSettingsEditForm(AdminEditForm):
    """Scripts settings edit form"""

    title = _("External scripts settings")
    legend = _("Scripts variables")

    fields = Fields(IScriptContainerSettings)

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        variables = self.widgets.get('variables')
        if variables is not None:
            variables.add_class('height-100')
            variables.widget_css_class = 'editor height-400px'
            variables.object_data = {
                'ams-filename': 'scripts.ini'
            }
            alsoProvides(variables, IObjectData)


@adapter_config(required=(IScriptContainerTarget, IAdminLayer, ScriptSettingsEditForm),
                provides=IFormContent)
def script_settings_edit_form_content(context, request, form):
    """Script settings edit form content getter"""
    return IScriptContainerSettings(context)
