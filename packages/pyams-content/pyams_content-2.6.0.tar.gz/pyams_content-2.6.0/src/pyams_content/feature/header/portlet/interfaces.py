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

"""PyAMS_*** module

"""

from zope.schema import Bool

from pyams_portal.interfaces import IPortletSettings

__docformat__ = 'restructuredtext'

from pyams_content import _


PAGE_HEADER_PORTLET_NAME = 'pyams_content.portlet.page_header'
PAGE_HEADER_ICON_CLASS = 'fas fa-user-circle'


class IPageHeaderPortletSettings(IPortletSettings):
    """Page header portlet settings interface"""

    display_logo = Bool(title=_("Display logo"),
                        description=_("Uncheck option to disable logo display"),
                        required=True,
                        default=True)

    display_context_title = Bool(title=_("Display context title"),
                                 description=_("Title is extracted from context"),
                                 required=True,
                                 default=True)

    display_profile_link = Bool(title=_("Display profile link"),
                                description=_("Display link to get access to login form "
                                              "or user profile"),
                                required=True,
                                default=True)
