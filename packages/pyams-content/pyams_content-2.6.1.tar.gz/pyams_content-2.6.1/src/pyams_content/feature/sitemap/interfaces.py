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

"""PyAMS_content.feature.sitemap.interfaces module

This module defines sitemap feature interfaces.
"""

__docformat__ = 'restructuredtext'

from zope.interface import Attribute, Interface


class IRobotsExtension(Interface):
    """Robots.txt extension interface"""
    
    disallowed = Attribute("Disallowed sources")
    allowed = Attribute("Allowed sources")
    
    
class ISitemapExtension(Interface):
    """Sitemap extension interface"""

    source = Attribute("Sitemap source")
