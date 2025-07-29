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

"""PyAMS_content.feature.search.portlet.skin.interfaces module

"""

from zope.contentprovider.interfaces import IContentProvider
from zope.interface import Attribute, Interface
from zope.schema import Bool, Choice, Int, TextLine

from pyams_content.feature.filter.interfaces import IAggregatedPortletRendererSettings
from pyams_content.feature.header.interfaces import HEADER_DISPLAY_MODE, HEADER_DISPLAY_MODES_VOCABULARY
from pyams_i18n.schema import I18nTextLineField
from pyams_skin.schema import BootstrapThumbnailsSelectionField

__docformat__ = 'restructuredtext'

from pyams_content import _


SEARCH_RESULTS_RENDERER_SETTINGS_KEY = 'pyams_content.search.renderer::search-results'


class ISearchResultsPortletBaseRendererSettings(IAggregatedPortletRendererSettings):
    """Search results portlet renderer base settings interface"""

    display_if_empty = Bool(title=_("Display if empty?"),
                            description=_("If 'no', and if no result is found, the portlet "
                                          "will not display anything"),
                            required=True,
                            default=True)

    display_results_count = Bool(title=_("Display results count?"),
                                 description=_("If 'no', results count will not be displayed"),
                                 required=True,
                                 default=True)

    allow_sorting = Bool(title=_("Allow results sorting?"),
                         description=_("If 'no', results will not be sortable"),
                         required=True,
                         default=True)

    allow_pagination = Bool(title=_("Allow pagination?"),
                            description=_("If 'no', results will not be paginated"),
                            required=True,
                            default=True)

    filters_css_class = TextLine(title=_('Filters CSS class'),
                                 description=_("CSS class used for filters column"),
                                 default='col col-12 col-md-4 col-lg-3 col-xl-2 float-left text-md-right')

    results_css_class = TextLine(title=_('Results CSS class'),
                                 description=_("CSS class used for view items container"),
                                 default='row mx-0 col col-12 col-md-8 col-lg-9 col-xl-10 float-right')
    
    header_display_mode = Choice(title=_("Header display mode"),
                                 description=_("Defines how results headers will be rendered"),
                                 required=True,
                                 vocabulary=HEADER_DISPLAY_MODES_VOCABULARY,
                                 default=HEADER_DISPLAY_MODE.FULL.value)

    start_length = Int(title=_("Start length"),
                       description=_("If you choose to display only header start, you can "
                                     "specify maximum text length"),
                       required=True,
                       default=120)
    
    display_tags = Bool(title=_("Display tags?"),
                        description=_("If 'no', tags attached to result items will not be displayed"),
                        required=True,
                        default=True)
    
    display_publication_date = Bool(title=_("Display publication date?"),
                                    description=_("If 'yes', publication date will be displayed for "
                                                  "each search result"),
                                    required=True,
                                    default=False)
    
    display_illustrations = Bool(title=_("Display illustrations?"),
                                 description=_("If 'no', view contents will not display "
                                               "illustrations"),
                                 required=True,
                                 default=True)

    thumb_selection = BootstrapThumbnailsSelectionField(
        title=_("Thumbnails selection"),
        description=_("Selection used to display images thumbnails"),
        default_selection='pano',
        change_selection=True,
        default_width=3,
        change_width=True,
        required=False)


class ISearchResultsPortletDefaultRendererSettings(ISearchResultsPortletBaseRendererSettings):
    """Search results portlet default renderer settings interface"""


class ISearchResultsPortletPanelsRendererSettings(ISearchResultsPortletBaseRendererSettings):
    """Search results portlet panels renderer settings interface"""

    thumb_selection = BootstrapThumbnailsSelectionField(
        title=_("Thumbnails selection"),
        description=_("Selection used to display images thumbnails"),
        default_selection='pano',
        change_selection=True,
        default_width=12,
        change_width=False,
        required=False)

    columns_count = BootstrapThumbnailsSelectionField(
         title=_("Columns count"),
         description=_("Select the number of panels columns for all available devices"),
         required=True,
         change_selection=False,
         default_width={
             'xs': 1,
             'sm': 2,
             'md': 3,
             'lg': 3,
             'xl': 4
         })

    button_title = I18nTextLineField(title=_("Button's title"),
                                     description=_("Optional navigation button's title"),
                                     required=False)


class ISearchResultsPortletCardsRendererSettings(ISearchResultsPortletBaseRendererSettings):
    """Search results portlet cards renderer settings interface"""

    thumb_selection = BootstrapThumbnailsSelectionField(
        title=_("Thumbnails selection"),
        description=_("Selection used to display images thumbnails"),
        default_selection='pano',
        change_selection=True,
        default_width=12,
        change_width=False,
        required=False)

    columns_count = BootstrapThumbnailsSelectionField(
         title=_("Columns count"),
         description=_("Select the number of panels columns for all available devices"),
         required=True,
         change_selection=False,
         default_width={
             'xs': 1,
             'sm': 2,
             'md': 3,
             'lg': 3,
             'xl': 4
         })

    button_title = I18nTextLineField(title=_("Button's title"),
                                     description=_("Optional navigation button's title"),
                                     required=False)


class ISearchResultsPortletMasonryCardsRendererSettings(ISearchResultsPortletCardsRendererSettings):
    """Search results portlet Masonry cards renderer settings interface"""


#
# Search results renderers interfaces
#

class ISearchResultTitle(Interface):
    """Search result title interface"""


class ISearchResultHeader(Interface):
    """Search result header interface"""


class ISearchResultURL(Interface):
    """Search result target URL interface"""


class ISearchResultRenderer(IContentProvider):
    """Search result renderer interface"""

    title = Attribute("Search result title")
    header = Attribute("Search result header")
    url = Attribute("Search result URL")
