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

"""PyAMS_*** module

"""

from pyramid.decorator import reify
from zope.interface import Interface

from pyams_content.reference.pictogram import IPictogramTable
from pyams_content.reference.zmi.table import ReferenceTableContainerTable
from pyams_file.skin import render_image
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_table.interfaces import IColumn
from pyams_utils.adapter import adapter_config
from pyams_utils.interfaces import MISSING_INFO
from pyams_viewlet.manager import viewletmanager_config
from pyams_zmi.interfaces import IAdminLayer, IObjectLabel
from pyams_zmi.interfaces.form import IFormTitle, IPropertiesEditForm
from pyams_zmi.interfaces.viewlet import IPropertiesMenu, ISiteManagementMenu
from pyams_zmi.table import ActionColumn, TableAdminView
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_content import _


PICTOGRAM_TABLE_LABEL = _("Pictograms")


@adapter_config(required=(IPictogramTable, IPyAMSLayer, Interface),
                provides=IObjectLabel)
def pictogram_table_label(context, request, view):
    """Pictograms table label"""
    return request.localizer.translate(PICTOGRAM_TABLE_LABEL)


@viewletmanager_config(name='contents.menu',
                       context=IPictogramTable, layer=IAdminLayer,
                       manager=ISiteManagementMenu, weight=10,
                       permission=VIEW_SYSTEM_PERMISSION,
                       provides=IPropertiesMenu)
class PictogramTableContentsMenu(NavigationMenuItem):
    """Pictogram table contents menu"""

    label = _("Table contents")
    icon_class = 'fas fa-table'
    href = '#contents.html'


class PictogramTableContainerTable(ReferenceTableContainerTable):
    """Pictogram container table"""

    @reify
    def data_attributes(self):
        attributes = super().data_attributes
        attributes['table'].update({
            'data-ams-order': '1,asc'
        })
        return attributes


@adapter_config(name='image',
                required=(IPictogramTable, IAdminLayer, PictogramTableContainerTable),
                provides=IColumn)
class PictogramTableImageColumn(ActionColumn):
    """Pictogram table image column"""

    css_classes = {
        'th': 'action',
        'td': 'action p-1'
    }
    weight = 5

    def render_cell(self, item):
        image = II18n(item).query_attribute('image', request=self.request)
        if image:
            return render_image(image, 32, 32, self.request, timestamp=True)
        return MISSING_INFO


@pagelet_config(name='contents.html',
                context=IPictogramTable, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class PictogramTableContentsView(TableAdminView):
    """Pictograms table contents view"""

    title = _("Pictograms")

    table_class = PictogramTableContainerTable
    table_label = _("Pictograms list")


@adapter_config(required=(IPictogramTable, IAdminLayer, IPropertiesEditForm),
                provides=IFormTitle)
def pictograms_table_title(context, request, form):
    """Pictograms table edit form title getter"""
    translate = request.localizer.translate
    return translate(_("Pictograms table"))
