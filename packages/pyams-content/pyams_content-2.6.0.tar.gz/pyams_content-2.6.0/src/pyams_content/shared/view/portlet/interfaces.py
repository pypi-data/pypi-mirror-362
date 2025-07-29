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

"""PyAMS_content.shared.view.portlet.interfaces module

This module defines interfaces of view items portlet settings.
"""

from collections import OrderedDict

from zope.interface import Interface
from zope.schema import Bool, Choice, Int
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_content.shared.view.interfaces import VIEW_CONTENT_TYPE
from pyams_content.shared.view.interfaces.query import MergeModes, VIEWS_MERGERS_VOCABULARY
from pyams_i18n.schema import I18nTextLineField
from pyams_portal.interfaces import IPortletSettings
from pyams_sequence.schema import InternalReferencesListField

__docformat__ = 'restructuredtext'

from pyams_content import _


#
# Views display contexts
#

VIEW_DISPLAY_CONTEXT = 'display'
VIEW_CONTENT_CONTEXT = 'content'

VIEW_CONTEXTS = OrderedDict((
    (VIEW_DISPLAY_CONTEXT, _("Display context")),
    (VIEW_CONTENT_CONTEXT, _("Content context"))
))

VIEW_CONTEXT_VOCABULARY = SimpleVocabulary([
    SimpleTerm(v, title=t)
    for v, t in VIEW_CONTEXTS.items()
])

SEARCH_EXCLUDED_ITEMS = 'search.excluded'


#
# Views merge modes
#

VIEW_ITEMS_PORTLET_NAME = 'pyams_content.portlet.view'


class IViewItemsAggregates(Interface):
    """View items aggregates interface"""


class IViewItemsPortletSettings(IPortletSettings):
    """View items portlet settings interface"""

    title = I18nTextLineField(title=_("Title"),
                              required=False)

    views = InternalReferencesListField(title=_("Selected views"),
                                        description=_("Reference to the view(s) from which items are extracted; "
                                                      "you can combine several views together and specify in which "
                                                      "order they should be mixed"),
                                        content_type=VIEW_CONTENT_TYPE,
                                        required=True)

    def get_views(self):
        """Get iterator over selected views"""

    views_context = Choice(title=_("Views context"),
                           description=_("When searching for items, a view receives a \"context\" which is the object "
                                         "from which settings can be extracted; this context can be the \"display\" "
                                         "context or the \"content\" context: when the portlet is used to display the "
                                         "site root, a site manager or a site folder, both are identical; when the "
                                         "portlet is used to display a shared content, the \"content\" context is the "
                                         "displayed content, while the \"display\" context is the container (site "
                                         "root, site manager or site folder) into which content is displayed"),
                           vocabulary=VIEW_CONTEXT_VOCABULARY,
                           default=VIEW_DISPLAY_CONTEXT,
                           required=True)

    views_merge_mode = Choice(title=_("Views merge mode"),
                              description=_("If you select several views, you can select \"merge\" mode, which is "
                                            "the way used to merge items from several views"),
                              vocabulary=VIEWS_MERGERS_VOCABULARY,
                              default=MergeModes.CONCAT.value,
                              required=True)

    def get_merger(self):
        """Get selected views merger utility"""

    limit = Int(title=_("Results count limit"),
                description=_("Maximum number of results that the component may extract from merged views"),
                required=False)

    start = Int(title=_("Starting from..."),
                description=_("You can skip several results if specifying an integer value here..."),
                required=False,
                default=1)

    def get_items(self):
        """Get iterator over items returned by selected views, using selected merger"""

    force_canonical_url = Bool(title=_("Force canonical URL?"),
                               description=_("By default, internal links use a \"relative\" URL, which tries to "
                                             "display link target in the current context; by using a canonical URL, "
                                             "you can display target in it's attachment context (if defined)"),
                               required=False,
                               default=False)

    exclude_from_search = Bool(title=_("Exclude from search results"),
                               description=_("If 'yes', and if this portlet is associated with a search engine in the "
                                             "same page template, items displayed by this portlet will be excluded "
                                             "from search results"),
                               required=True,
                               default=False)

    first_page_only = Bool(title=_("Display on first page only"),
                           description=_("If 'yes', and if this portlet is associated with a search engine in the "
                                         "same page template, view contents will only be displayed on the first page "
                                         "of search results"),
                           required=True,
                           default=False)
