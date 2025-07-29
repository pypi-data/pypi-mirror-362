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

"""PyAMS_content.feature.search.portlet.interfaces module

"""

from zope.schema import Bool

from pyams_i18n.schema import I18nTextLineField
from pyams_portal.interfaces import IPortletSettings

__docformat__ = 'restructuredtext'

from pyams_content import _


SEARCH_RESULTS_PORTLET_NAME = 'pyams_content.portlet.search.results'
SEARCH_RESULTS_ICON_CLASS = 'fas fa-search'

SEARCH_RESULTS_PORTLET_FLAG = 'pyams_content.portlet.search.has_results'
"""Request annotations flag for portlet search results"""


class ISearchResultsPortletSettings(IPortletSettings):
    """Search results portlet settings"""

    title = I18nTextLineField(title=_("Title"),
                              description=_("Portlet main title"),
                              required=False)

    allow_empty_query = Bool(title=_("Allow empty query?"),
                             description=_("If 'no', no result will be displayed if user didn't "
                                           "entered a search string"),
                             required=True,
                             default=True)

    force_canonical_url = Bool(title=_("Force canonical URL?"),
                               description=_("By default, internal links use a \"relative\" URL, "
                                             "which tries to display link target in the current "
                                             "context; by using a canonical URL, you can display "
                                             "target in it's attachment context (if defined)"),
                               required=False,
                               default=False)

    def has_user_query(self):
        """Check if user entered custom search arguments"""

    def get_items(self, request=None, limit=None, ignore_cache=False):
        """Get search results"""
