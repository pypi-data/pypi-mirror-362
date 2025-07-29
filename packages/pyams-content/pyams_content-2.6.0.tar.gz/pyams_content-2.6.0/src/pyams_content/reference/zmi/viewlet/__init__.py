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

"""PyAMS_content.reference.zmi.viewlet module

"""
import locale

from zope.interface import Interface

from pyams_content.reference import IReferenceTable
from pyams_content.zmi.viewlet.toplinks import TopTabsViewletManager
from pyams_i18n.interfaces import II18n
from pyams_skin.viewlet.menu import MenuItem
from pyams_utils.registry import get_all_utilities_registered_for
from pyams_utils.url import absolute_url
from pyams_viewlet.manager import viewletmanager_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.zmi.viewlet.toplinks import TopMenuViewletManager


__docformat__ = 'restructuredtext'

from pyams_content import _


@viewletmanager_config(name='reference-tables.menu',
                       context=Interface, layer=IAdminLayer,
                       manager=TopTabsViewletManager, weight=40)
class ReferencesTablesMenu(TopMenuViewletManager):
    """Reference tables menu"""

    label = _("Reference tables")

    def update(self):
        super().update()
        context = self.context
        request = self.request
        parent = self.__parent__
        for table in sorted(get_all_utilities_registered_for(IReferenceTable),
                            key=lambda x: locale.strxfrm(II18n(x).query_attribute('title',
                                                                                  request=request)
                                                         or '')):
            self.add_menu(context, request, parent, table)
