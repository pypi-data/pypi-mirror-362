#
# Copyright (c) 2015-2023 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.component.illustration.portlet.interfaces module

This module provides interfaces of illustration portlet settings.
"""

from zope.interface import Interface

from pyams_portal.interfaces import IPortletSettings


__docformat__ = 'restructuredtext'


class IIllustrationPortletSettings(IPortletSettings):
    """Illustration portlet settings interface"""


class IIllustrationPortletContent(Interface):
    """Illustration portlet content getter interface

    This interface can be used by components which doesn't provide an illustration
    directly, but can provide an illustration by other methods.
    """
