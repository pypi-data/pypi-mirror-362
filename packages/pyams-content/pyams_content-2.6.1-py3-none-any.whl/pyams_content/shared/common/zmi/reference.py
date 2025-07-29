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

"""PyAMS_content.shared.common.zmi.reference module

This module provides management components which are used to handle
internal components which can be used to feed views.
"""
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_sequence.interfaces import IInternalReferencesList
from pyams_skin.interfaces.viewlet import IFormHeaderViewletManager
from pyams_skin.viewlet.help import AlertMessage
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminEditForm
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IPropertiesMenu
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_content import _


@viewlet_config(name='internal-references.menu',
                context=IInternalReferencesList, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=300,
                permission=VIEW_SYSTEM_PERMISSION)
class InternalReferencesMenu(NavigationMenuItem):
    """Internal references menu"""

    label = _("Internal references")
    href = '#internal-references.html'

    def __new__(cls, context, request, view, manager=None):
        references = IInternalReferencesList(context, None)
        if not getattr(references, 'use_references_for_views', True):
            return None
        return NavigationMenuItem.__new__(cls)


@ajax_form_config(name='internal-references.html',
                  context=IInternalReferencesList, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class InternalReferencesEditForm(AdminEditForm):
    """Internal references edit form"""

    title = _("Internal references")
    legend = _("Internal references settings")

    fields = Fields(IInternalReferencesList)


@viewlet_config(name='internal-references.help',
                context=IInternalReferencesList, layer=IAdminLayer, view=InternalReferencesEditForm,
                manager=IFormHeaderViewletManager, weight=1)
class InternalReferencesEditFormHelp(AlertMessage):
    """Internal references edit form help"""

    status = 'info'

    _message = _("Selected contents can be used to feed views which are using their "
                 "context internal references.")
    message_renderer = 'markdown'
