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

"""PyAMS_content.feature.seo module

This module provides SEO related classes and default adapters.
"""

from persistent import Persistent
from zope.container.contained import Contained
from zope.schema.fieldproperty import FieldProperty

from pyams_content.feature.seo.interfaces import ISEOContentInfo, SEO_INFO_ANNOTATION_KEY
from pyams_content.shared.common import IWfSharedContent
from pyams_utils.adapter import adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config

__docformat__ = 'restructuredtext'


@factory_config(ISEOContentInfo)
class SEOContentInfo(Persistent, Contained):
    """SEO content info"""

    include_sitemap = FieldProperty(ISEOContentInfo['include_sitemap'])


@adapter_config(required=IWfSharedContent,
                provides=ISEOContentInfo)
def shared_content_seo_info(context):
    """Shared content SEO info"""
    return get_annotation_adapter(context, SEO_INFO_ANNOTATION_KEY,
                                  ISEOContentInfo)
