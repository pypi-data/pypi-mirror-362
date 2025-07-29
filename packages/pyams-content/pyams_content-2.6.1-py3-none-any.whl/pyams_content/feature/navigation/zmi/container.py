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

"""PyAMS_content.feature.navigation.zmi.container module

"""

from zope.interface import implementer

from pyams_content.component.association.zmi.container import AssociationsTable
from pyams_content.feature.navigation import IMenusContainer
from pyams_content.feature.navigation.interfaces import IMenusContainerTarget
from pyams_content.feature.navigation.zmi.interfaces import IMenusContainerEditForm, IMenusTable
from pyams_form.ajax import ajax_form_config
from pyams_form.interfaces.form import IInnerSubForm
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_skin.interfaces.viewlet import IContentSuffixViewletManager
from pyams_table.interfaces import IColumn, IValues
from pyams_utils.adapter import ContextRequestViewAdapter, NullAdapter, adapter_config
from pyams_utils.factory import factory_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalDisplayForm
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.form import IPropertiesEditForm
from pyams_zmi.table import IconColumn, InnerTableAdminView, TableGroupSwitcher

__docformat__ = 'restructuredtext'

from pyams_content import _


@ajax_form_config(name='menus-modal.html',
                  context=IMenusContainerTarget, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
@implementer(IMenusContainerEditForm)
class MenusModalEditForm(AdminModalDisplayForm):
    """Menus modal edit form"""

    modal_class = 'modal-xl'
    subtitle = _("Navigation menus")


@factory_config(IMenusTable)
class MenusTable(AssociationsTable):
    """Menus table"""

    container_class = IMenusContainer


@adapter_config(required=(IMenusContainerTarget, IAdminLayer, IMenusTable),
                provides=IValues)
class MenusTableValues(ContextRequestViewAdapter):
    """Menus table values"""

    @property
    def values(self):
        """Menus container values getter"""
        yield from IMenusContainer(self.context).values()


@adapter_config(name='icon',
                required=(IMenusContainer, IAdminLayer, IMenusTable),
                provides=IColumn)
class MenusIconColumn(NullAdapter):
    """Menus table icon column"""


@adapter_config(name='size',
                required=(IMenusContainer, IAdminLayer, IMenusTable),
                provides=IColumn)
class MenusSizeColumn(NullAdapter):
    """Menus table size column"""


@adapter_config(name='dynamic',
                required=(IMenusContainer, IAdminLayer, IMenusTable),
                provides=IColumn)
class MenusDynamicColumn(IconColumn):
    """Menus table dynamic column"""

    icon_class = 'fab fa-elementor'
    hint = _("Dynamic menu")

    weight = 45

    def get_icon_class(self, item):
        """Icon class getter"""
        return self.icon_class if item.dynamic_menu else None


#
# Main menus table
#

@viewlet_config(name='associations-table',
                context=IMenusContainerTarget, layer=IAdminLayer,
                view=IMenusContainerEditForm,
                manager=IContentSuffixViewletManager, weight=20)
class MenusTableView(InnerTableAdminView):
    """Menus table view"""

    table_class = IMenusTable
    table_label = _("Navigation menus")

    container_intf = IMenusContainer


@adapter_config(name='associations-group',
                required=(IMenusContainerTarget, IAdminLayer, IPropertiesEditForm),
                provides=IInnerSubForm, force_implements=False)
class MenusGroup(TableGroupSwitcher):
    """Menus table group"""

    legend = _("Navigation menus")

    table_class = IMenusTable
    container_intf = IMenusContainer

    weight = 30
