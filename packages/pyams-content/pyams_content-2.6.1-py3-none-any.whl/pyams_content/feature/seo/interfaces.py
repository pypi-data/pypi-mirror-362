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

"""PyAMS_content.feature.seo.interfaces module

This module provides interfaces related to search engines optimization (SEO).
"""

from zope.interface import Interface
from zope.schema import Bool

__docformat__ = 'restructuredtext'

from pyams_content import _


SEO_INFO_ANNOTATION_KEY = 'pyams_content.seo'


class ISEOContentInfo(Interface):
    """SEO content information interface"""

    include_sitemap = Bool(title=_("Include sitemap"),
                           description=_("If unchecked, this content will be excluded from "
                                         "sitemap"),
                           required=True,
                           default=True)
