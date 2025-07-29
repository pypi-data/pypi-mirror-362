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

"""PyAMS_content.component.paragraph.portlet.skin.interfaces module

This module defines a single interface which can be used to define custom
paragraph container portlet renderers.
"""

from zope.interface import Attribute

from pyams_portal.interfaces import IPortletContentProvider


__docformat__ = 'restructuredtext'


class IParagraphContainerPortletRenderer(IPortletContentProvider):
    """Paragraph container portlet renderer interface

    This interface is used to create custom paragraphs container portlet
    renderers, which may be registered with a view name.
    """

    use_portlets_cache = Attribute("Use portlets cache?")
