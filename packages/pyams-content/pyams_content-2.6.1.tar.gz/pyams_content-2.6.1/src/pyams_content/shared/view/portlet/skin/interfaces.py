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

"""PyAMS_content.shared.view.portlet.skin.interfaces module

This module defines interfaces of view items portlet renderers settings.
"""

from zope.contentprovider.interfaces import IContentProvider
from zope.interface import Attribute, Interface
from zope.schema import Bool, Choice, Int, TextLine

from pyams_content.feature.header.interfaces import HEADER_DISPLAY_MODE, HEADER_DISPLAY_MODES_VOCABULARY
from pyams_i18n.schema import I18nTextLineField
from pyams_sequence.interfaces import IInternalReference
from pyams_sequence.schema import InternalReferenceField
from pyams_skin.schema import BootstrapThumbnailsSelectionField

__docformat__ = 'restructuredtext'

from pyams_content import _


class IViewItemTargetURL(Interface):
    """View item target URL"""

    target = Attribute("Reference target")

    url = Attribute("Reference URL")


class IViewItemsPortletBaseRendererSettings(Interface):
    """View items portlet base renderer settings interface"""

    paginate = Bool(title=_("Paginate?"),
                    description=_("If 'no', results pagination will be disabled"),
                    required=True,
                    default=True)

    page_size = Int(title=_("Page size"),
                    description=_("Number of items per page, if pagination is enabled"),
                    required=False,
                    default=10)

    filters_css_class = TextLine(title=_('Filters CSS class'),
                                 description=_("CSS class used for filters column"),
                                 default='col col-12 col-md-4 col-lg-3 col-xl-2 float-left text-md-right')

    results_css_class = TextLine(title=_('Results CSS class'),
                                 description=_("CSS class used for view items container"),
                                 default='row mx-0 col col-12 col-md-8 col-lg-9 col-xl-10 float-right')

    display_illustrations = Bool(title=_("Display illustrations?"),
                                 description=_("If 'no', view contents will not display "
                                               "illustrations"),
                                 required=True,
                                 default=True)


class IViewItemsPortletVerticalRendererSettings(IViewItemsPortletBaseRendererSettings, IInternalReference):
    """View items portlet vertical renderer settings interface"""

    thumb_selection = BootstrapThumbnailsSelectionField(
        title=_("Thumbnails selection"),
        description=_("Selection used to display images thumbnails"),
        default_width={
            'xs': 12,
            'sm': 12,
            'md': 4,
            'lg': 4,
            'xl': 4
        },
        required=False)

    display_breadcrumbs = Bool(title=_("Display breadcrumbs?"),
                               description=_("If 'no', view items breadcrumbs will not be "
                                             "displayed"),
                               required=True,
                               default=True)

    display_tags = Bool(title=_("Display tags?"),
                        description=_("If 'no', view items tags will not be displayed"),
                        required=True,
                        default=True)

    reference = InternalReferenceField(title=_("'See all' link target"),
                                       description=_("Internal reference to site or search "
                                                     "folder displaying full list of view's "
                                                     "contents"),
                                       required=False)

    link_label = I18nTextLineField(title=_("Link label"),
                                   description=_("Label of the link to full list page"),
                                   required=False)


class IViewItemsPortletThumbnailsRendererSettings(IViewItemsPortletBaseRendererSettings):
    """View items portlet thumbnails renderer settings interface"""

    paginate = Attribute("Removed attribute")
    page_size = Attribute("Removed attribute")
    
    thumb_selection = BootstrapThumbnailsSelectionField(
        title=_("Thumbnails selection"),
        description=_("Selection used to display images thumbnails"),
        default_width={
            'xs': 3,
            'sm': 3,
            'md': 2,
            'lg': 1,
            'xl': 1
        },
        required=True)


class IViewItemsPortletPanelsRendererSettings(IViewItemsPortletBaseRendererSettings):
    """View items portlet panels renderer settings interface"""

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

    header_display_mode = Choice(title=_("Header display mode"),
                                 description=_("Defines how results headers will be rendered"),
                                 required=True,
                                 vocabulary=HEADER_DISPLAY_MODES_VOCABULARY,
                                 default=HEADER_DISPLAY_MODE.FULL.value)

    start_length = Int(title=_("Start length"),
                       description=_("If you choose to display only header start, you can specify "
                                     "maximum text length"),
                       required=True,
                       default=120)


class IViewItemsPortletCardsRendererSettings(IViewItemsPortletPanelsRendererSettings):
    """View items portlet cards renderer settings interface"""


class IViewItemsPortletMasonryCardsRendererSettings(IViewItemsPortletCardsRendererSettings):
    """View items portlet Masonry cards renderer settings interface"""


#
# View items renderers interfaces
#

class IViewItemTitle(Interface):
    """View item title interface"""


class IViewItemHeader(Interface):
    """View item header interface"""


class IViewItemURL(Interface):
    """View item target URL interface"""


class IViewItemRenderer(IContentProvider):
    """View item renderer interface"""

    title = Attribute("View item title")
    header = Attribute("View item header")
    url = Attribute("View item URL")
