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

"""PyAMS_content.shared.view.interfaces module

This module defines views interfaces.
"""

from collections import OrderedDict

from zope.interface import Attribute
from zope.schema import Bool, Choice, Int, Set
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_content.shared.common.interfaces import ISharedContent, ISharedTool, IWfSharedContent, \
    VIEWS_SHARED_CONTENT_TYPES_VOCABULARY
from pyams_content.shared.common.interfaces.types import ALL_DATA_TYPES_VOCABULARY

__docformat__ = 'restructuredtext'

from pyams_content import _


VIEW_CONTENT_TYPE = 'view'
VIEW_CONTENT_NAME = _('View')


RELEVANCE_ORDER = 'relevance'
TITLE_ORDER = 'title'
CREATION_DATE_ORDER = 'created_date'
UPDATE_DATE_ORDER = 'modified_date'
PUBLICATION_DATE_ORDER = 'publication_date'
FIRST_PUBLICATION_DATE_ORDER = 'first_publication_date'
CONTENT_PUBLICATION_DATE_ORDER = 'content_publication_date'
VISIBLE_PUBLICATION_DATE_ORDER = 'visible_publication_date'
EXPIRATION_DATE_ORDER = 'expiration_date'


VIEW_ORDERS = OrderedDict((
    (TITLE_ORDER, _("Alphabetical")),
    (CREATION_DATE_ORDER, _("Published version creation date")),
    (UPDATE_DATE_ORDER, _("Published version last update date")),
    (PUBLICATION_DATE_ORDER, _("Current version publication date")),
    (FIRST_PUBLICATION_DATE_ORDER, _("Current version first publication date")),
    (CONTENT_PUBLICATION_DATE_ORDER, _("Content first publication date")),
    (VISIBLE_PUBLICATION_DATE_ORDER, _("Visible publication date")),
    (EXPIRATION_DATE_ORDER, _("Expiration date"))
))

VIEW_ORDER_VOCABULARY = SimpleVocabulary([
    SimpleTerm(v, title=t)
    for v, t in VIEW_ORDERS.items()
])


USER_VIEW_ORDERS = OrderedDict((
    (RELEVANCE_ORDER, _("Relevance (on user search; if not on visible publication date)")),
    (TITLE_ORDER, _("Alphabetical")),
    (CREATION_DATE_ORDER, _("Published version creation date")),
    (UPDATE_DATE_ORDER, _("Published version last update date")),
    (PUBLICATION_DATE_ORDER, _("Current version publication date")),
    (FIRST_PUBLICATION_DATE_ORDER, _("Current version first publication date")),
    (CONTENT_PUBLICATION_DATE_ORDER, _("Content first publication date")),
    (VISIBLE_PUBLICATION_DATE_ORDER, _("Visible publication date")),
    (EXPIRATION_DATE_ORDER, _("Expiration date"))
))

USER_VIEW_ORDER_VOCABULARY = SimpleVocabulary([
    SimpleTerm(v, title=t)
    for v, t in USER_VIEW_ORDERS.items()
])


class IWfView(IWfSharedContent):
    """View interface"""

    select_context_path = Bool(title=_("Select context path?"),
                               description=_("If 'yes', only contents located inside context "
                                             "will be selected"),
                               required=True,
                               default=False)

    def get_content_path(self, context):
        """Get context path internal ID"""

    select_context_type = Bool(title=_("Select context type?"),
                               description=_("If 'yes', content type will be extracted from "
                                             "context"),
                               required=True,
                               default=False)

    selected_content_types = Set(title=_("Other content types"),
                                 description=_("Selected content types; leave empty for all"),
                                 value_type=Choice(vocabulary=VIEWS_SHARED_CONTENT_TYPES_VOCABULARY),
                                 required=False)

    def get_ignored_types(self):
        """Get content typed which are excluded from views (except if specified explicitly at runtime)"""

    def get_content_types(self, context):
        """Get content types for given context"""

    select_context_datatype = Bool(title=_("Select context data type?"),
                                   description=_("If 'yes', content data type (if available) "
                                                 "will be extracted from context"),
                                   required=True,
                                   default=False)

    selected_datatypes = Set(title=_("Other data types"),
                             description=_("Selected data types; leave empty for all"),
                             value_type=Choice(vocabulary=ALL_DATA_TYPES_VOCABULARY),
                             required=False)

    def get_data_types(self, context):
        """Get data types for given context"""

    excluded_content_types = Set(title=_("Excluded content types"),
                                 description=_("Excluded content types; leave empty for all"),
                                 value_type=Choice(vocabulary=VIEWS_SHARED_CONTENT_TYPES_VOCABULARY),
                                 required=False)

    def get_excluded_content_types(self, context):
        """Get excluded content types for given context"""

    excluded_datatypes = Set(title=_("Excluded data types"),
                             description=_("Excluded data types; leave empty for all"),
                             value_type=Choice(vocabulary=ALL_DATA_TYPES_VOCABULARY),
                             required=False)

    allow_user_params = Bool(title=_("Allow user params?"),
                             description=_("If 'no', additional user params provided through request "
                                           "URL will not be analyzed"),
                             required=True,
                             default=True)

    def get_excluded_data_types(self, context):
        """Get excluded data types for given context"""

    order_by = Choice(title=_("Order by"),
                      description=_("Property to use to sort results; publication date can be "
                                    "different from first publication date for contents which "
                                    "have been retired and re-published with a different "
                                    "publication date"),
                      vocabulary=VIEW_ORDER_VOCABULARY,
                      required=True,
                      default=VISIBLE_PUBLICATION_DATE_ORDER)

    reversed_order = Bool(title=_("Reversed order?"),
                          description=_("If 'yes', items order will be reversed"),
                          required=True,
                          default=True)

    limit = Int(title=_("Results count limit"),
                description=_("Maximum number of results that the view may retrieve"),
                max=1000,
                required=False)

    age_limit = Int(title=_("Results age limit"),
                    description=_("If specified, contents whose publication date (given in "
                                  "days) is older than this limit will be ignored"),
                    required=False)

    is_using_context = Attribute("Check if view is using context settings")

    def get_results(self, context, sort_index=None, reverse=True, limit=None,
                    start=0, length=999, ignore_cache=False, get_count=False,
                    request=None, **kwargs):
        """Get query results"""


class IView(ISharedContent):
    """Workflow managed view interface"""


class IViewManager(ISharedTool):
    """View manager interface"""
