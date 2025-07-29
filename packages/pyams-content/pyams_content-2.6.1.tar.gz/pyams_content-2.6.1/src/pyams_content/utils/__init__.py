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

"""PyAMS_content.utils module

"""

from zope.interface import Interface


__docformat__ = 'restructuredtext'

from pyams_content.interfaces import IObjectType, IObjectTypes
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.registry import get_current_registry


@adapter_config(required=Interface,
                provides=IObjectTypes)
class ObjectTypesAdapter(ContextAdapter):
    """Object_types adapter"""

    @property
    def object_types(self):
        result = set()
        registry = get_current_registry()
        for name, object_type in registry.getAdapters((self.context,), IObjectType):
            result.add(object_type)
        return result
