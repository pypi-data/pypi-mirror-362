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

"""PyAMS_content.component.extfile.manager module

This module provides components to handle external files managers.
"""

from persistent import Persistent
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.extfile.interfaces import EXTFILE_MANAGER_INFO_KEY, \
    IExtFileManagerInfo, IExtFileManagerTarget
from pyams_site.interfaces import ISiteRoot
from pyams_utils.adapter import adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config


__docformat__ = 'restructuredtext'


@factory_config(IExtFileManagerInfo)
class ExtFileManagerInfo(Persistent):
    """External files manager settings"""

    default_title_prefix = FieldProperty(IExtFileManagerInfo['default_title_prefix'])


@adapter_config(required=IExtFileManagerTarget,
                provides=IExtFileManagerInfo)
def extfile_manager_info_factory(context):
    """External files manager factory"""
    return get_annotation_adapter(context, EXTFILE_MANAGER_INFO_KEY, IExtFileManagerInfo)
