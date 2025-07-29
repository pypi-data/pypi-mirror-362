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

"""PyAMS_content.zmi.dashboard module

This module provides components which are used in all dashboards.
"""

from zope.interface import Interface, implementer

from pyams_content.interfaces import MANAGE_CONTENT_PERMISSION
from pyams_content.shared.site.interfaces import ISiteLink
from pyams_content.zmi.interfaces import IDashboardColumn, IDashboardContentLabel, \
    IDashboardContentModifier, IDashboardContentNumber, IDashboardContentOwner, \
    IDashboardContentStatus, IDashboardContentStatusDatetime, IDashboardContentTimestamp, \
    IDashboardContentType, IDashboardContentVersion, IDashboardContentVisibility, IDashboardTable
from pyams_sequence.interfaces import ISequentialIntIds
from pyams_table.column import GetAttrColumn
from pyams_table.interfaces import IColumn
from pyams_utils.adapter import adapter_config
from pyams_utils.data import ObjectDataManagerMixin
from pyams_utils.interfaces import ICacheKeyValue, MISSING_INFO
from pyams_utils.registry import get_utility
from pyams_utils.request import request_property
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.table import I18nColumnMixin, NameColumn, VisibilityColumn
from pyams_zmi.utils import get_object_label


__docformat__ = 'restructuredtext'

from pyams_content import _


@implementer(IDashboardColumn)
class DashboardColumnMixin(ObjectDataManagerMixin):  # pylint: disable=no-member
    """Base dashboard column mixin"""

    interface = None

    @request_property(key=None)
    def get_target(self, obj):
        """Row target getter"""
        item_key = ICacheKeyValue(obj)
        target = self.table.rows_state.get(item_key)
        if target is None:
            target = obj
        return target

    def get_value(self, obj):
        """Column value getter"""
        target = self.get_target(obj)
        registry = self.request.registry
        value = registry.queryMultiAdapter((target, self.request, self), self.interface)
        if value is None:
            value = registry.queryAdapter(target, self.interface)
        return value or MISSING_INFO


@adapter_config(required=IDashboardColumn,
                provides=ICacheKeyValue)
def dashboard_column_cache_key(column: IDashboardColumn):
    """Dashboard column cache key"""
    return ICacheKeyValue(column.table)


class DashboardVisibilityColumn(DashboardColumnMixin, VisibilityColumn):
    """Dashboard visibility column"""

    interface = IDashboardContentVisibility
    permission = MANAGE_CONTENT_PERMISSION

    weight = 5

    active_icon_hint = _("Switch element visibility")
    inactive_icon_hint = _("Visible element?")

    def get_icon(self, item):
        """Icon getter"""
        return self.get_value(item)[1]

    def get_icon_hint(self, item):
        """Icon hint getter"""
        translate = self.request.localizer.translate
        if ISiteLink.providedBy(item) and self.has_permission(item):
            return translate(self.active_icon_hint)
        return translate(self.inactive_icon_hint)

    def render_cell(self, item):
        """Cell renderer"""
        active, icon = self.get_value(item)
        if not active:
            return self.get_icon(item)
        return super().render_cell(item)


@adapter_config(name='name',
                required=(Interface, IAdminLayer, IDashboardTable),
                provides=IColumn)
class DashboardLabelColumn(DashboardColumnMixin, NameColumn):
    """Dashboard label column"""

    i18n_header = _("Title")
    interface = IDashboardContentLabel

    css_classes = {
        'td': 'text-truncate'
    }

    def get_value(self, obj):
        label = super().get_value(obj)
        if label == MISSING_INFO:
            target = self.get_target(obj)
            label = get_object_label(target, self.request, self.table)
        return label or MISSING_INFO


@adapter_config(name='content-type',
                required=(Interface, IAdminLayer, IDashboardTable),
                provides=IColumn)
class DashboardContentTypeColumn(DashboardColumnMixin, I18nColumnMixin, GetAttrColumn):
    """Dashboard content type column"""

    i18n_header = _("Data type")
    interface = IDashboardContentType
    weight = 15


@adapter_config(name='sequence',
                required=(Interface, IAdminLayer, IDashboardTable),
                provides=IColumn)
class DashboardContentNumberColumn(DashboardColumnMixin, I18nColumnMixin, GetAttrColumn):
    """Dashboard content number column"""

    @property
    def i18n_header(self):
        """Header getter"""
        sequence = get_utility(ISequentialIntIds)
        return self.request.localizer.translate(_('#{}')).format(sequence.prefix)

    interface = IDashboardContentNumber
    weight = 20


@adapter_config(name='status',
                required=(Interface, IAdminLayer, IDashboardTable),
                provides=IColumn)
class DashboardContentStatusColumn(DashboardColumnMixin, I18nColumnMixin, GetAttrColumn):
    """Dashboard content status column"""

    i18n_header = _("Status")
    css_classes = {
        'td': 'text-nowrap'
    }
    interface = IDashboardContentStatus
    weight = 25


@adapter_config(name='status-datetime',
                required=(Interface, IAdminLayer, IDashboardTable),
                provides=IColumn)
class DashboardContentStatusDatetimeColumn(DashboardColumnMixin, I18nColumnMixin, GetAttrColumn):
    """Dashboard content status datetime column"""

    i18n_header = _("Status datetime")
    css_classes = {
        'td': 'text-nowrap'
    }
    interface = IDashboardContentStatusDatetime
    weight = 30


@adapter_config(name='version',
                required=(Interface, IAdminLayer, IDashboardTable),
                provides=IColumn)
class DashboardContentVersionColumn(DashboardColumnMixin, I18nColumnMixin, GetAttrColumn):
    """Dashboard content status version column"""

    i18n_header = _("Version")
    interface = IDashboardContentVersion
    weight = 35


@adapter_config(name='status-principal',
                required=(Interface, IAdminLayer, IDashboardTable),
                provides=IColumn)
class DashboardContentStatusPrincipalColumn(DashboardColumnMixin, I18nColumnMixin, GetAttrColumn):
    """Dashboard content status modifier column"""

    i18n_header = _("Modifier")
    css_classes = {
        'td': 'text-nowrap'
    }
    interface = IDashboardContentModifier
    weight = 40


@adapter_config(name='owner',
                required=(Interface, IAdminLayer, IDashboardTable),
                provides=IColumn)
class DashboardContentOwnerColumn(DashboardColumnMixin, I18nColumnMixin, GetAttrColumn):
    """Dashboard content owner column"""

    i18n_header = _("Owner")
    css_classes = {
        'td': 'text-nowrap'
    }
    interface = IDashboardContentOwner
    weight = 45


@adapter_config(name='timestamp',
                required=(Interface, IAdminLayer, IDashboardTable),
                provides=IColumn)
class DashboardContentTimestampColumn(DashboardColumnMixin, I18nColumnMixin, GetAttrColumn):
    """Dashboard content timestamp column"""

    i18n_header = _("Last update")
    css_classes = {
        'td': 'text-nowrap'
    }
    interface = IDashboardContentTimestamp
    weight = 50
