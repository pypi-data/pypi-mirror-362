#
# Copyright (c) 2015-2024 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.component.links.manager module

"""

from persistent import Persistent
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.links.interfaces import EXTERNAL_LINKS_MANAGER_INFO_KEY, IExternalLinksManagerInfo, \
    IExternalLinksManagerTarget
from pyams_utils.adapter import adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config

__docformat__ = 'restructuredtext'


@factory_config(IExternalLinksManagerInfo)
class ExternalLinksManagerInfo(Persistent):
    """External links manager settings"""

    check_external_links = FieldProperty(IExternalLinksManagerInfo['check_external_links'])
    forbidden_hosts = FieldProperty(IExternalLinksManagerInfo['forbidden_hosts'])


@adapter_config(required=IExternalLinksManagerTarget,
                provides=IExternalLinksManagerInfo)
def external_links_manager_info(context):
    """External links manager factory"""
    return get_annotation_adapter(context, EXTERNAL_LINKS_MANAGER_INFO_KEY, IExternalLinksManagerInfo)
