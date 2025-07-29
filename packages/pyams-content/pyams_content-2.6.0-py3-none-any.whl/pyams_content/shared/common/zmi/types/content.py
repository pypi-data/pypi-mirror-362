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

"""PyAMS_content.shared.common.zmi.types module

This module define components which are used for management of typed
shared contents.
"""

__docformat__ = 'restructuredtext'

from pyramid.decorator import reify
from zope.interface import Interface

from pyams_content.shared.common.interfaces import ISharedTool
from pyams_content.shared.common.interfaces.types import IWfTypedSharedContent
from pyams_content.shared.common.zmi import SharedContentPropertiesEditForm
from pyams_form.field import Fields
from pyams_form.interfaces.form import IFormContent
from pyams_utils.adapter import adapter_config
from pyams_utils.registry import get_utility
from pyams_zmi.form import AdminEditForm
from pyams_zmi.interfaces import IAdminLayer


class TypedSharedContentPropertiesEditForm(SharedContentPropertiesEditForm):
    """Typed shared content properties edit form"""

    interface = IWfTypedSharedContent
    fieldnames = ('title', 'short_name', 'content_url', 'data_type',
                  'header', 'description', 'notepad')


class TypedSharedContentCustomInfoEditForm(AdminEditForm):
    """Typed shared content custom information edit form"""

    @reify
    def datatype(self):
        """Form context datatype getter"""
        context = self.context
        if IWfTypedSharedContent.providedBy(context):
            return context.get_data_type()
        return None

    @property
    def fields(self):
        """Form fields getter"""
        datatype = self.datatype
        if datatype is None:
            return Fields(Interface)
        manager = get_utility(ISharedTool, name=self.context.content_type)
        return Fields(manager.shared_content_info_factory).select(*datatype.field_names)


@adapter_config(required=(IWfTypedSharedContent, IAdminLayer, TypedSharedContentCustomInfoEditForm),
                provides=IFormContent)
def typed_shared_content_custom_info_edit_form_content(context, request, layer):
    """Typed shared content custom info edit content getter"""
    manager = get_utility(ISharedTool, name=context.content_type)
    return manager.shared_content_info_factory(context)
