#
# Copyright (c) 2015-2022 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.component.association.zmi module

This module provides base associations management components.
"""

from zope.interface import Interface, implementer

from pyams_content.component.association import IAssociationContainer, \
    IAssociationContainerTarget, IAssociationItem
from pyams_content.component.association.interfaces import IAssociationInfo
from pyams_content.component.association.zmi.interfaces import IAssociationItemAddForm, \
    IAssociationItemEditForm, IAssociationsTable
from pyams_content.component.paragraph.zmi import get_json_paragraph_toolbar_refresh_event
from pyams_form.interfaces.form import IAJAXFormRenderer
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.traversing import get_parent
from pyams_utils.url import absolute_url
from pyams_zmi.helper.event import get_json_table_row_add_callback, \
    get_json_table_row_refresh_callback
from pyams_zmi.interfaces import IAdminLayer, IObjectHint, IObjectIcon, IObjectLabel
from pyams_zmi.interfaces.form import IFormTitle
from pyams_zmi.interfaces.table import ITableElementEditor
from pyams_zmi.table import TableElementEditor
from pyams_zmi.utils import get_object_hint, get_object_label


__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(required=(IAssociationContainer, IAdminLayer, Interface),
                provides=IObjectLabel)
def association_container_label(context, request, view):  # pylint: disable=unused-argument
    """Association container label getter"""
    target = get_parent(context, IAssociationContainerTarget)
    return get_object_label(target, request, view)


class AssociationItemAddMenuMixin:
    """Link add menu mixin class"""

    modal_target = True

    def get_href(self):
        """Menu URL target getter"""
        container = IAssociationContainer(self.context)
        return absolute_url(container, self.request, self.href)


@implementer(IAssociationItemAddForm)
class AssociationItemAddFormMixin:
    """Association item add form mixin class"""

    def add(self, obj):
        """Add file to container"""
        IAssociationContainer(self.context).append(obj)


@adapter_config(required=(IAssociationContainer, IAdminLayer, IAssociationItemAddForm),
                provides=IAJAXFormRenderer)
class AssociationItemAddFormRenderer(ContextRequestViewAdapter):
    """Association item add form renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        result = {
            'status': 'success',
            'callbacks': [
                get_json_table_row_add_callback(self.context, self.request,
                                                IAssociationsTable, changes)
            ]
        }
        event = get_json_paragraph_toolbar_refresh_event(changes, self.request)
        if event is not None:
            result.setdefault('callbacks', []).append(event)
        return result


@adapter_config(required=(IAssociationItem, IAdminLayer, Interface),
                provides=IObjectLabel)
def association_item_label(context, request, view):  # pylint: disable=unused-argument
    """Association item label getter"""
    return IAssociationInfo(context).user_title


@adapter_config(required=(IAssociationItem, IAdminLayer, Interface),
                provides=IObjectIcon)
def association_item_icon(context, request, view):
    """Association item icon getter"""
    return f'fa-fw {context.icon_class}'


@adapter_config(required=(IAssociationItem, IAdminLayer, Interface),
                provides=IObjectHint)
def association_item_hint(context, request, view):
    """Association item hint getter"""
    return request.localizer.translate(context.icon_hint)


@adapter_config(required=(IAssociationItem, IAdminLayer, Interface),
                provides=ITableElementEditor)
class AssociationItemTableElementEditor(TableElementEditor):
    """Association item table element editor"""


@adapter_config(required=(IAssociationItem, IAdminLayer, IAssociationItemEditForm),
                provides=IFormTitle)
def association_item_edit_form_title(context, request, view):
    """Association item properties edit form title getter"""
    translate = request.localizer.translate
    parent = get_parent(context, IAssociationContainerTarget)
    hint = get_object_hint(parent, request, view)
    label = get_object_label(parent, request, view)
    parent_label = translate(_("{}: {}")).format(hint, label) if hint else label
    label = translate(_("{}: {}")).format(get_object_hint(context, request, view),
                                          get_object_label(context, request, view))
    return f'<small>{parent_label}</small><br />{label}'


@adapter_config(required=(IAssociationItem, IAdminLayer, IAssociationItemEditForm),
                provides=IAJAXFormRenderer)
class AssociationItemEditFormRenderer(ContextRequestViewAdapter):
    """Link edit form AJAX renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        parent = get_parent(self.context, IAssociationContainer)
        return {
            'callbacks': [
                get_json_table_row_refresh_callback(parent, self.request,
                                                    IAssociationsTable, self.context)
            ]
        }
