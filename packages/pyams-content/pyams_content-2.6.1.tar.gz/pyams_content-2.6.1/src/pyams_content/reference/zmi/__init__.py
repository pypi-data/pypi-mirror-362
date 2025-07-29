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

from zope.interface import Interface

from pyams_content.reference import IReferenceManager, IReferenceTable
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_skin.interfaces.viewlet import IBreadcrumbItem
from pyams_skin.viewlet.breadcrumb import BreadcrumbItem
from pyams_utils.adapter import adapter_config
from pyams_zmi.interfaces import IAdminLayer, IObjectLabel


__docformat__ = 'restructuredtext'

from pyams_content import _


REFERENCE_MANAGER_LABEL = _("References")


@adapter_config(required=(IReferenceManager, IPyAMSLayer, Interface),
                provides=IObjectLabel)
def reference_manager_label(context, request, view):
    """Reference manager label"""
    return request.localizer.translate(REFERENCE_MANAGER_LABEL)


@adapter_config(required=(IReferenceManager, IAdminLayer, Interface),
                provides=IBreadcrumbItem)
class ReferenceManagerBreadcrumbAdapter(BreadcrumbItem):
    """References tables manager breadcrumb adapter"""

    label = _("References tables")
    view_name = None


@adapter_config(required=(IReferenceTable, IAdminLayer, Interface),
                provides=IBreadcrumbItem)
class ReferenceTableBreadcrumbs(BreadcrumbItem):
    """Reference table breadcrumb item"""

    @property
    def label(self):
        return II18n(self.context).query_attribute('short_name', request=self.request)

    view_name = 'admin'
