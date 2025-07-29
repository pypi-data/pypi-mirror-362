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

__docformat__ = 'restructuredtext'

import locale

from pyams_content.reference.pictogram import IPictogramTable
from pyams_content.reference.pictogram.interfaces import IPictogramManager, \
    IPictogramManagerTarget
from pyams_form.browser.select import SelectWidget
from pyams_form.template import widget_layout_config, widget_template_config
from pyams_form.widget import FieldWidget
from pyams_i18n.interfaces import II18n
from pyams_utils.registry import query_utility
from pyams_utils.traversing import get_parent
from pyams_zmi.interfaces import IAdminLayer


@widget_layout_config(template='templates/selection-layout.pt', layer=IAdminLayer)
@widget_template_config(template='templates/selection.pt', layer=IAdminLayer)
class PictogramManagerSelectionWidget(SelectWidget):
    """Pictogram manager selection widget"""

    pictogram_table = None
    pictogram_manager = None

    def update(self):
        super().update()
        self.pictogram_table = query_utility(IPictogramTable)
        target = get_parent(self.context, IPictogramManagerTarget)
        if target is not None:
            self.pictogram_manager = IPictogramManager(target)

    @property
    def sorted_pictograms(self):
        yield from sorted(self.pictogram_table.values(),
                          key=lambda x: locale.strxfrm(
                              (II18n(x).query_attribute('title',
                                                        request=self.request) or '').lower()))

    @property
    def available_pictograms(self):
        manager = self.pictogram_manager
        if manager is not None:
            for pictogram in self.sorted_pictograms:
                if pictogram.__name__ not in (manager.selected_pictograms or ()):
                    yield pictogram

    @property
    def selected_pictograms(self):
        manager = self.pictogram_manager
        if manager is not None:
            for name in (manager.selected_pictograms or ()):
                pictogram = self.pictogram_table.get(name)
                if pictogram is not None:
                    yield pictogram


def PictogramManagerSelectionFieldWidget(field, request):  # pylint: disable=invalid-name
    """Pictogram manager selection field widget factory"""
    return FieldWidget(field, PictogramManagerSelectionWidget(request))
