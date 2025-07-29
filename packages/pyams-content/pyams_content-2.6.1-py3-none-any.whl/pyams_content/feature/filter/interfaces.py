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

from collections import OrderedDict
from enum import Enum

from zope.annotation.interfaces import IAttributeAnnotatable
from zope.container.constraints import contains
from zope.container.interfaces import IContainer
from zope.interface import Attribute, Interface
from zope.schema import Bool, Choice, Int
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_i18n.schema import I18nTextLineField
from pyams_portal.interfaces import IPortletRendererSettings
from pyams_thesaurus.interfaces import THESAURUS_EXTRACTS_VOCABULARY, THESAURUS_NAMES_VOCABULARY
from pyams_thesaurus.interfaces.thesaurus import IThesaurusContextManager

__docformat__ = 'restructuredtext'

from pyams_content import _


FILTER_CONTAINER_ANNOTATION_KEY = 'pyams_content.filters'


#
# Filter sorting
#

class FILTER_SORTING(Enum):
    """Filter modes enumeration"""
    ALPHA = 'alpha_asc'
    ALPHA_DESC = 'alpha_desc'
    COUNT = 'count_asc'
    COUNT_DESC = 'count_desc'
    MANUAL = 'manual'


FILTER_SORTING_LABEL = OrderedDict((
    (FILTER_SORTING.ALPHA.value, _("Alphabetical")),
    (FILTER_SORTING.ALPHA_DESC.value, _("Alphabetical (reversed)")),
    (FILTER_SORTING.COUNT.value, _("Results count")),
    (FILTER_SORTING.COUNT_DESC.value, _("Results count (reversed)"))
))

FILTER_SORTING_VOCABULARY = SimpleVocabulary([
    SimpleTerm(k, title=v)
    for k, v in FILTER_SORTING_LABEL.items()
])


MANUAL_FILTER_SORTING_LABEL = FILTER_SORTING_LABEL.copy()
MANUAL_FILTER_SORTING_LABEL[FILTER_SORTING.MANUAL.value] = _("Manual")

MANUAL_FILTER_SORTING_VOCABULARY = SimpleVocabulary([
    SimpleTerm(k, title=v)
    for k, v in MANUAL_FILTER_SORTING_LABEL.items()
])


#
# Filter display mode
#

class FILTER_DISPLAY_MODE(Enum):
    """Filter display modes enumeration"""
    LIST = 'list'
    SELECT = 'select'


FILTER_DISPLAY_MODE_LABEL = OrderedDict((
    (FILTER_DISPLAY_MODE.LIST.value, _("List")),
    (FILTER_DISPLAY_MODE.SELECT.value, _("Choice")),
))

FILTER_DISPLAY_MODE_VOCABULARY = SimpleVocabulary([
    SimpleTerm(key, title=value)
    for key, value in FILTER_DISPLAY_MODE_LABEL.items()
])


class FILTER_ALIGNMENT(Enum):
    """Filter label alignment enumeration"""
    LEFT = 'left'
    RIGHT = 'right'
    CENTER = 'center'


FILTER_ALIGNMENT_LABEL = OrderedDict((
    (FILTER_ALIGNMENT.LEFT.value, _("Left")),
    (FILTER_ALIGNMENT.RIGHT.value, _("Right")),
    (FILTER_ALIGNMENT.CENTER.value, _("Center"))
))

FILTER_ALIGNMENT_VOCABULARY = SimpleVocabulary([
    SimpleTerm(key, title=value)
    for key, value in FILTER_ALIGNMENT_LABEL.items()
])


#
# Content-type filter mode
#

class CONTENT_TYPE_FILTER_MODE(Enum):
    """Content-type filter modes enumeration"""
    FACET_LABEL = 'facet_label'
    FACET_TYPE_LABEL = 'facet_type_label'


CONTENT_TYPE_FILTER_MODE_LABEL = {
    CONTENT_TYPE_FILTER_MODE.FACET_LABEL.value: _("Content-type label"),
    CONTENT_TYPE_FILTER_MODE.FACET_TYPE_LABEL.value: _("Data type label")
}

CONTENT_TYPE_FILTER_MODE_VOCABULARY = SimpleVocabulary([
    SimpleTerm(key, title=value)
    for key, value in CONTENT_TYPE_FILTER_MODE_LABEL.items()
])


#
# Filters interfaces
#

class IFilterValues(Interface):
    """Filter value interface"""


class IFilterIndexInfo(Interface):
    """Filter index info base interface"""

    facets = Attribute("Filter facets")


class IFilter(Interface):
    """Base filter interface"""

    visible = Bool(title=_("Visible?"),
                   description=_("Is this filter visible in front-office?"),
                   required=True,
                   default=True)

    label = I18nTextLineField(title=_("Label"),
                              description=_("This is the label displayed in filter header"),
                              required=True)

    display_mode = Choice(title=_("Display mode"),
                          description=_("Filter entries display mode"),
                          vocabulary=FILTER_DISPLAY_MODE_VOCABULARY,
                          default=FILTER_DISPLAY_MODE.LIST.value,
                          required=True)

    open_state = Bool(title=_("Default open state"),
                      description=_("If 'no', options list will be collapsed by default"),
                      required=True,
                      default=True)

    displayed_entries = Int(title=_("Displayed entries"),
                            description=_("Number of entries displayed in search filter"),
                            required=True,
                            default=5)

    labels_alignment = Choice(title=_("Labels alignment"),
                              description=_("Labels display alignment for search filter in "
                                            "list mode"),
                              required=True,
                              vocabulary=FILTER_ALIGNMENT_VOCABULARY,
                              default=FILTER_ALIGNMENT.LEFT.value)

    truncate_labels = Bool(title=_("Truncated labels"),
                           description=_("Activate this option to truncate labels and "
                                         "remove line breaks"),
                           required=True,
                           default=True)

    display_count = Bool(title=_("Display results count"),
                         description=_("In 'list' mode, display number of entries matching "
                                       "each search filter value"),
                         required=True,
                         default=True)

    select_placeholder = I18nTextLineField(title=_("Select placeholder"),
                                           description=_("Placeholder text displayed in the "
                                                         "select widget"),
                                           required=False)

    sorting_mode = Choice(title=_("Sorting mode"),
                          description=_("Filter entries sorting mode"),
                          vocabulary=FILTER_SORTING_VOCABULARY,
                          default=FILTER_SORTING.ALPHA.value,
                          required=True)

    filter_type = Attribute("Filter type")
    
    filter_name = Attribute("Filter name")

    def is_visible(self, request=None):
        """Is association item published?"""


class IContentTypesFilter(IFilter):
    """Content-types filter interface"""

    content_mode = Choice(title=_("Content-type display mode"),
                          description=_("Filter entries display mode"),
                          vocabulary=CONTENT_TYPE_FILTER_MODE_VOCABULARY,
                          default=CONTENT_TYPE_FILTER_MODE.FACET_LABEL.value,
                          required=True)


class ITitleFilter(IFilter):
    """Title filter"""


class IThesaurusFilter(IFilter, IThesaurusContextManager):
    """Thesaurus-based filter interface"""

    sorting_mode = Choice(title=_("Sorting mode"),
                          description=_("Filter entries sorting mode"),
                          vocabulary=MANUAL_FILTER_SORTING_VOCABULARY,
                          default=FILTER_SORTING.MANUAL.value,
                          required=True)

    thesaurus_name = Choice(title=_("Thesaurus name"),
                            description=_("Name of thesaurus used to get filter terms"),
                            vocabulary=THESAURUS_NAMES_VOCABULARY,
                            required=True)

    extract_name = Choice(title=_("Thesaurus extract"),
                          description=_("Name of thesaurus extract containing terms used by this filter"),
                          vocabulary=THESAURUS_EXTRACTS_VOCABULARY,
                          required=False)


class ITagsFilter(IThesaurusFilter):
    """Tags filter Interface"""


class IThemesFilter(IThesaurusFilter):
    """Themes filter Interface"""


class ICollectionsFilter(IThesaurusFilter):
    """Collections filter Interface"""


class IFilterType(Interface):
    """Filter type interface"""


class IFiltersContainer(IContainer):
    """Filters container interface"""

    contains(IFilter)

    def add(self, obj):
        """Add filter to container"""

    def get_visible_filters(self):
        """Visible filters iterator"""

    def get_processed_filters(self, context, request, aggregations):
        """Iterator over processed filters aggregations"""


class IFiltersContainerTarget(IAttributeAnnotatable):
    """Filters container target marker interface"""


class IAggregatedPortletRendererSettings(IPortletRendererSettings):
    """Aggregated portlet renderer settings marker interface"""


class IFilterAggregate(Interface):
    """Filter aggregate getter"""


class IFilterProcessor(Interface):
    """Filter processor interface"""

    def process(self, aggregations, filter_type=None):
        """Process the filter and return relevant data"""

    def get_aggregations(self, aggregations):
        """Return aggregations from search results"""


class IFilterProcessorAggregationsHandler(Interface):
    """Filter processor aggregations handler interface"""

    def get_aggregations(self, aggregations):
        """Convert search aggregations in renderer format"""
