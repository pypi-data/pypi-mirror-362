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

"""PyAMS_content.skin.interfaces module

this module defines common contents rendering interfaces.
"""

__docformat__ = 'restructuredtext'

from zope.interface import Attribute, Interface

from pyams_layer.interfaces import IPyAMSUserLayer


class IPyAMSDefaultLayer(IPyAMSUserLayer):
    """PyAMS default skin layer interface"""


class IContentTitle(Interface):
    """Content title getter interface"""


class IContentIllustration(Interface):
    """Content illustration getter interface"""


class IContentBannerIllustration(Interface):
    """Content banner illustration getter interface"""


class IContentNavigationIllustration(Interface):
    """Content navigation illustration getter interface"""


class IContentNavigationTitle(Interface):
    """Content navigation title getter interface"""


class IContentTag(Interface):
    """Shared content data type tag getter interface"""


class IContentDate(Interface):
    """Content date getter interface"""


class IContentHeader(Interface):
    """Content header getter interface"""


class IContentSummaryInfo(Interface):
    """Content summary info getter interface"""

    context = Attribute("Link to adapted context")
    title = Attribute("Content title")
    header = Attribute("Content header")
    button_title = Attribute("Button title")


class IPublicURL(Interface):
    """Public URL target getter interface"""
