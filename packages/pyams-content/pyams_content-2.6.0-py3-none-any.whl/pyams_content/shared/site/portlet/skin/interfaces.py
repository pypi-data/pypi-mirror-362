# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from zope.contentprovider.interfaces import IContentProvider
from zope.interface import Attribute, Interface
from zope.schema import Bool, Choice, Int

from pyams_content.feature.header.interfaces import HEADER_DISPLAY_MODE, HEADER_DISPLAY_MODES_VOCABULARY
from pyams_i18n.schema import I18nTextLineField
from pyams_portal.interfaces import IPortletRendererSettings
from pyams_skin.schema import BootstrapThumbnailsSelectionField

__docformat__ = 'restructuredtext'

from pyams_content import _


class ISiteContainerSummaryPortletBaseRendererSettings(IPortletRendererSettings):
    """Site container summary portlet base renderer settings interface"""
    
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
    

class ISiteContainerSummaryPortletDefaultRendererSettings(ISiteContainerSummaryPortletBaseRendererSettings):
    """Site container summary portlet default renderer settings interface"""


class ISiteContainerSummaryPortletPanelsRendererSettings(ISiteContainerSummaryPortletBaseRendererSettings):
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
    
    def get_css_class(self):
        """CSS class getter"""


class ISiteContainerSummaryPortletCardsRendererSettings(ISiteContainerSummaryPortletBaseRendererSettings):
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


class ISiteContainerSummaryPortletMasonryCardsRendererSettings(ISiteContainerSummaryPortletCardsRendererSettings):
    """Search results portlet Masonry cards renderer settings interface"""


#
# Site container items renderers interfaces
#

class ISiteContainerSummaryItemTitle(Interface):
    """Site container summary item title interface"""


class ISiteContainerSummaryItemHeader(Interface):
    """Site container summary item header interface"""


class ISiteContainerSummaryItemButtonTitle(Interface):
    """Site container summary item button title interface"""
    
    
class ISiteContainerSummaryItemURL(Interface):
    """Site container summary item target URL interface"""


class ISiteContainerSummaryItemRenderer(IContentProvider):
    """Site container summary item renderer interface"""
    
    title = Attribute("Site container summary item title")
    header = Attribute("Site container summary item header")
    illustration = Attribute("Site container summary item illustration")
    url = Attribute("Site container summary item URL")
    button_title = Attribute("Site container summary item button title")
