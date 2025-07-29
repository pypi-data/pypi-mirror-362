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

"""PyAMS_content.features.renderer.interfaces module

This module defines base interfaces of content renderers.
"""

from zope.annotation import IAttributeAnnotatable
from zope.contentprovider.interfaces import IContentProvider
from zope.interface import Attribute, Interface


__docformat__ = 'restructuredtext'


RENDERER_SETTINGS_KEY = 'pyams_content.renderer.settings'


class IRenderedContent(IAttributeAnnotatable):
    """Generic interface for any rendered content"""

    renderer = Attribute("Selected renderer name")

    def get_renderer(self, request=None):
        """Get selected renderer implementation"""


class IContentRenderer(IContentProvider):
    """Content renderer interface"""

    label = Attribute("Renderer label")
    weight = Attribute("Renderer weight, used for ordering")

    settings_interface = Attribute("Renderer settings interface")
    resources = Attribute("Iterable of needed Fanstatic resources")

    language = Attribute("Renderer language (if forced)")


class ISharedContentRenderer(IContentRenderer):
    """Shared content renderer interface"""


class IRendererSettings(Interface):
    """Base renderer settings interface"""
