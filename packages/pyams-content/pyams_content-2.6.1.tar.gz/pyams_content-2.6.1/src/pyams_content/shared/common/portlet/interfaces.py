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

"""PyAMS_content.shared.common.portlet.interfaces module

This module defines interfaces of shared contents portlets settings.
"""

__docformat__ = 'restructuredtext'

from zope.contentprovider.interfaces import IContentProvider
from zope.schema import Bool

from pyams_i18n.schema import I18nTextLineField
from pyams_portal.interfaces import IPortletSettings

from pyams_content import _


TITLE_PORTLET_NAME = 'pyams_content.portlet.title'


class ISharedContentTitlePortletSettings(IPortletSettings):
    """Shared content title portlet settings interface"""

    display_publication_date = Bool(title=_("Display publication date?"),
                                    description=_("If 'yes', content publication date will be "
                                                  "displayed; the selected publication date is "
                                                  "those which is selected while publishing the "
                                                  "content"),
                                    required=True,
                                    default=False)

    publication_date_prefix = I18nTextLineField(title=_("Publication date prefix"),
                                                description=_("This text will be displayed "
                                                              "before publication date"),
                                                required=False)

    display_specificities = Bool(title=_("Display specificities?"),
                                 description=_("If 'no', specific content's information will not "
                                               "be displayed..."),
                                 required=True,
                                 default=True)


HEADER_PORTLET_NAME = 'pyams_content.portlet.header'


class ISharedContentHeaderPortletSettings(IPortletSettings):
    """Shared content header portlet settings"""

    display_illustration = Bool(title=_("Display illustration?"),
                                description=_("If enabled, and if a header illustration is "
                                              "associated with the content, it's selected ratio "
                                              "may vary according to the selected renderer"),
                                required=True,
                                default=True)

    display_breadcrumbs = Bool(title=_("Display breadcrumbs?"),
                               required=True,
                               default=True)

    display_title = Bool(title=_("Display title?"),
                         required=True,
                         default=True)

    display_tags = Bool(title=_("Display tags?"),
                        required=True,
                        default=True)

    display_header = Bool(title=_("Display header?"),
                          required=True,
                          default=True)

    display_publication_date = Bool(title=_("Display publication date?"),
                                    description=_("If 'yes', content publication date will be "
                                                  "displayed; the selected publication date is "
                                                  "those which is selected while publishing the "
                                                  "content"),
                                    required=True,
                                    default=False)

    publication_date_prefix = I18nTextLineField(title=_("Publication date prefix"),
                                                description=_("This text will be displayed "
                                                              "before publication date"),
                                                required=False)

    display_alerts = Bool(title=_("Display alerts?"),
                          description=_("If 'no', alerts which are linked to a specific content "
                                        "will not be displayed"),
                          required=True,
                          default=True)

    display_specificities = Bool(title=_("Display specificities?"),
                                 description=_("If 'no', specific content's information will not "
                                               "be displayed..."),
                                 required=True,
                                 default=True)


SPECIFICITIES_PORTLET_NAME = 'pyams_content.portlet.specificities'


class ISharedContentSpecificitiesPortletSettings(IPortletSettings):
    """Shared content specificities portlet settings interface"""


class ISpecificitiesRenderer(IContentProvider):
    """Specificities renderer interface"""
