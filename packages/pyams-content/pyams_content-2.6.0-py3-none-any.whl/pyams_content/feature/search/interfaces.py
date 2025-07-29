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

"""PyAMS_content.feature.search.interfaces module

"""

from zope.interface import Attribute, Interface, Invalid, invariant
from zope.schema import Bool, Choice, Set

from pyams_content.interfaces import IBaseContent
from pyams_content.shared.common import VIEWS_SHARED_CONTENT_TYPES_VOCABULARY
from pyams_content.shared.common.interfaces.types import ALL_DATA_TYPES_VOCABULARY
from pyams_content.shared.site.interfaces import IBaseSiteItem, ISiteElement
from pyams_content.shared.view.interfaces import IWfView, RELEVANCE_ORDER, USER_VIEW_ORDER_VOCABULARY
from pyams_content.shared.view.interfaces.query import IViewQuery
from pyams_i18n.schema import I18nTextLineField
from pyams_sequence.interfaces import IInternalReferencesList, ISequentialIdTarget
from pyams_sequence.schema import InternalReferenceField

__docformat__ = 'restructuredtext'

from pyams_content import _


class ISearchManagerInfo(IInternalReferencesList):
    """Search manager interface"""

    reference = InternalReferenceField(title=_("Main search engine"),
                                       description=_("Search folder handling main site search. "
                                                     "You can search a reference using '+' "
                                                     "followed by internal number, or by "
                                                     "entering text matching content title."),
                                       required=False)

    search_target = Attribute("Search target object")

    name = I18nTextLineField(title=_("Search engine name"),
                             description=_("Name given to the search engine"),
                             required=False)

    description = I18nTextLineField(title=_("Description"),
                                    description=_("Description given to the search engine"),
                                    required=False)

    enable_tags_search = Bool(title=_("Enable search by tag?"),
                              description=_("If 'yes', displayed tags will lead to a search "
                                            "engine displaying contents matching given tag"),
                              required=True,
                              default=False)

    tags_search_target = InternalReferenceField(title=_("Tags search target"),
                                                description=_("Site or folder where tags search "
                                                              "is displayed"),
                                                required=False)

    tags_target = Attribute("Tags search target object reference")

    @invariant
    def check_tags_search_target(self):
        """Check that target is defined to enable tags search"""
        if self.enable_tags_search and not self.tags_search_target:
            raise Invalid(_("You must specify search target when activating search by tags!"))

    enable_collections_search = Bool(title=_("Enable search by collection?"),
                                     description=_("If 'yes', displayed collections will lead to "
                                                   "a search engine displaying contents matching "
                                                   "given collection"),
                                     required=True,
                                     default=False)

    collections_search_target = InternalReferenceField(title=_("Collections search target"),
                                                       description=_("Site or folder where collections "
                                                                     "search is displayed"),
                                                       required=False)

    collections_target = Attribute("Collections search target object reference")

    @invariant
    def check_collections_search_target(self):
        """Check that target is defined to enable collections search"""
        if self.enable_collections_search and not self.collections_search_target:
            raise Invalid(_("You must specify search target when activating search by "
                            "collections!"))


class ISearchFolder(IBaseContent, IBaseSiteItem, ISiteElement, IWfView, ISequentialIdTarget):
    """Search folder interface"""

    order_by = Choice(title=_("Order by"),
                      description=_("Property to use to sort results; publication date can be "
                                    "different from first publication date for contents which "
                                    "have been retired and re-published with a different "
                                    "publication date"),
                      vocabulary=USER_VIEW_ORDER_VOCABULARY,
                      required=False,
                      default=RELEVANCE_ORDER)

    visible_in_list = Bool(title=_("Visible in folders list"),
                           description=_("If 'no', search folder will not be displayed into "
                                         "parent's contents list"),
                           required=True,
                           default=True)

    navigation_title = I18nTextLineField(title=_("Navigation title"),
                                         description=_("Folder's title displayed in navigation "
                                                       "pages; original title will be used if "
                                                       "none is specified"),
                                         required=False)

    selected_content_types = Set(title=_("Selected content types"),
                                 description=_("Searched content types; leave empty for all"),
                                 value_type=Choice(vocabulary=VIEWS_SHARED_CONTENT_TYPES_VOCABULARY),
                                 required=False)

    selected_datatypes = Set(title=_("Selected data types"),
                             description=_("Searched data types; leave empty for all"),
                             value_type=Choice(vocabulary=ALL_DATA_TYPES_VOCABULARY),
                             required=False)


class ISearchFolderQuery(IViewQuery):
    """Search folder query interface"""


class IContextUserSearchSettings(Interface):
    """Context user search settings interface

    This interface is used to get user search settings from context.
    """

    def get_settings(self):
        """Get matching context settings

        :return dict: user search settings mapping
        """


class ISearchFormRequestParams(Interface):
    """User search request params

    This interface is used to get user request params which can be included into
    search forms.
    """

    def get_params(self):
        """Get request params

        :return iterator: iterator over list of request params; each element may be a mapping
        containing param attributes 'name' and 'value'
        """
