# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from persistent import Persistent
from zope.container.contained import Contained
from zope.interface import Interface, implementer
from zope.location.interfaces import ILocation
from zope.schema import getFieldNames
from zope.schema.fieldproperty import FieldProperty

from pyams_content.feature.header.interfaces import HEADER_DISPLAY_MODE
from pyams_content.shared.site.interfaces import ISiteContainer, ISiteElement
from pyams_content.shared.site.portlet import ISiteContainerSummaryPortletSettings
from pyams_content.shared.site.portlet.skin.interfaces import ISiteContainerSummaryItemButtonTitle, \
    ISiteContainerSummaryItemHeader, ISiteContainerSummaryItemRenderer, ISiteContainerSummaryItemTitle, \
    ISiteContainerSummaryItemURL, ISiteContainerSummaryPortletBaseRendererSettings, \
    ISiteContainerSummaryPortletCardsRendererSettings, ISiteContainerSummaryPortletDefaultRendererSettings, \
    ISiteContainerSummaryPortletMasonryCardsRendererSettings, ISiteContainerSummaryPortletPanelsRendererSettings
from pyams_content.skin.interfaces import IContentNavigationIllustration
from pyams_content.shared.site.skin.interfaces import ISiteContainerSummaryView
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer, IPyAMSUserLayer
from pyams_portal.interfaces import IPortalContext, IPortletRenderer
from pyams_portal.skin import PortletRenderer
from pyams_skin.interfaces.viewlet import IBreadcrumbs
from pyams_template.template import template_config
from pyams_utils.adapter import NullAdapter, adapter_config
from pyams_utils.factory import factory_config
from pyams_utils.text import get_text_start
from pyams_viewlet.viewlet import ViewContentProvider

__docformat__ = 'restructuredtext'

from pyams_content import _


#
# Site summary items adapters
#

@adapter_config(required=(ILocation, IPyAMSUserLayer, ISiteContainerSummaryView),
                provides=IBreadcrumbs)
class LocationBreadcrumbsAdapter(NullAdapter):
    """Disable breadcrumbs in site container summary view"""


#
# Site container summary portlet base renderer
#

class SiteContainerSummaryPortletBaseRendererSettings(Persistent, Contained):
    """Site container summary portlet base renderer settings"""
    
    header_display_mode = FieldProperty(ISiteContainerSummaryPortletBaseRendererSettings['header_display_mode'])
    start_length = FieldProperty(ISiteContainerSummaryPortletBaseRendererSettings['start_length'])
    display_illustrations = FieldProperty(ISiteContainerSummaryPortletBaseRendererSettings['display_illustrations'])
    thumb_selection = FieldProperty(ISiteContainerSummaryPortletBaseRendererSettings['thumb_selection'])
    
    
@implementer(ISiteContainerSummaryView)
class SiteContainerSummaryPortletBaseRenderer(PortletRenderer):
    """Site container summary portlet base renderer"""

    @property
    def visible_items(self):
        container = ISiteContainer(self.context, None)
        if container is not None:
            yield from container.get_visible_items(self.request)

    def render_item(self, item, template_name=''):
        renderer = self.request.registry.queryMultiAdapter((item, self.request, self),
                                                           ISiteContainerSummaryItemRenderer)
        if renderer is not None:
            renderer.update()
            return renderer.render(template_name)
        return ''
    
    
#
# Default site container summary portlet renderer
#

@factory_config(ISiteContainerSummaryPortletDefaultRendererSettings)
class SiteContainerSummaryPortletDefaultRendererSettings(SiteContainerSummaryPortletBaseRendererSettings):
    """Site container summary portlet default renderer settings"""
    

@adapter_config(required=(IPortalContext, IPyAMSLayer, Interface, ISiteContainerSummaryPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/container-summary-default.pt', layer=IPyAMSLayer)
class SiteContainerSummaryPortletDefaultRenderer(SiteContainerSummaryPortletBaseRenderer):
    """Site container summary portlet default renderer"""
    
    label = _("Simple items list (default)")
    weight = 1
    
    settings_interface = ISiteContainerSummaryPortletDefaultRendererSettings


#
# Site container summary portlet panels renderer
#

@factory_config(ISiteContainerSummaryPortletPanelsRendererSettings)
class SiteContainerSummaryPortletPanelsRendererSettings(SiteContainerSummaryPortletBaseRendererSettings):
    """Site container summary portlet default renderer settings"""
    
    thumb_selection = FieldProperty(ISiteContainerSummaryPortletPanelsRendererSettings['thumb_selection'])
    columns_count = FieldProperty(ISiteContainerSummaryPortletPanelsRendererSettings['columns_count'])
    button_title = FieldProperty(ISiteContainerSummaryPortletPanelsRendererSettings['button_title'])

    def get_css_class(self):
        columns = self.columns_count
        return ' '.join((
            f'row-cols-{selection.cols}' if device == 'xs' else f'row-cols-{device}-{selection.cols}'
            for device, selection in columns.items()
        ))


@adapter_config(name='panels',
                required=(IPortalContext, IPyAMSLayer, Interface, ISiteContainerSummaryPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/container-summary-panels.pt', layer=IPyAMSLayer)
class SiteContainerSummaryPortletPanelsRenderer(SiteContainerSummaryPortletBaseRenderer):
    """Site container summary portlet panels renderer"""
    
    label = _("Paneled items list")
    weight = 10
    
    settings_interface = ISiteContainerSummaryPortletPanelsRendererSettings


#
# Site container summary portlet cards renderer
#

@factory_config(ISiteContainerSummaryPortletCardsRendererSettings)
class SiteContainerSummaryPortletCardsRendererSettings(SiteContainerSummaryPortletBaseRendererSettings):
    """Site container summary portlet cards renderer settings"""
    
    thumb_selection = FieldProperty(ISiteContainerSummaryPortletCardsRendererSettings['thumb_selection'])
    columns_count = FieldProperty(ISiteContainerSummaryPortletCardsRendererSettings['columns_count'])
    button_title = FieldProperty(ISiteContainerSummaryPortletCardsRendererSettings['button_title'])

    def get_css_class(self):
        columns = self.columns_count
        return ' '.join((
            f'row-cols-{selection.cols}' if device == 'xs' else f'row-cols-{device}-{selection.cols}'
            for device, selection in columns.items()
        ))


@adapter_config(name='cards',
                required=(IPortalContext, IPyAMSLayer, Interface, ISiteContainerSummaryPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/container-summary-cards.pt', layer=IPyAMSLayer)
class SiteContainerSummaryPortletCardsRenderer(SiteContainerSummaryPortletBaseRenderer):
    """Site container summary portlet cards renderer"""
    
    label = _("Bootstrap cards list")
    weight = 20
    
    settings_interface = ISiteContainerSummaryPortletCardsRendererSettings


#
# Site container summary portlet masonry renderer
#

@factory_config(ISiteContainerSummaryPortletMasonryCardsRendererSettings)
class SiteContainerSummaryPortletMasonryCardsRendererSettings(SiteContainerSummaryPortletCardsRendererSettings):
    """Site container summary portlet Masonry cards renderer settings"""

    def get_css_class(self):
        columns = self.columns_count
        return ' '.join((
            f'columns-{selection.cols}' if device == 'xs' else f'columns-{device}-{selection.cols}'
            for device, selection in columns.items()
        ))


@adapter_config(name='cards::masonty',
                required=(IPortalContext, IPyAMSLayer, Interface, ISiteContainerSummaryPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/container-summary-masonry.pt', layer=IPyAMSLayer)
class SiteContainerSummaryPortletMasonryCardsRenderer(SiteContainerSummaryPortletBaseRenderer):
    """Site container summary portlet Masonry cards renderer"""
    
    label = _("Bootstrap Masonry cards list")
    weight = 30
    
    settings_interface = ISiteContainerSummaryPortletMasonryCardsRendererSettings


#
# Base site container summary item renderer
#

@adapter_config(required=(ISiteElement, IPyAMSUserLayer, ISiteContainerSummaryView),
                provides=ISiteContainerSummaryItemRenderer)
@template_config(template='templates/container-item.pt', layer=IPyAMSUserLayer)
@template_config(name='panel',
                 template='templates/container-item-panel.pt', layer=IPyAMSUserLayer)
@template_config(name='card',
                 template='templates/container-item-card.pt', layer=IPyAMSUserLayer)
@template_config(name='masonry',
                 template='templates/container-item-masonry.pt', layer=IPyAMSUserLayer)
class BaseSiteContainerSummaryItemRenderer(ViewContentProvider):
    """Base site container item summary renderer"""

    @property
    def title(self):
        return self.request.registry.queryMultiAdapter((self.context, self.request, self.view),
                                                       ISiteContainerSummaryItemTitle)

    @property
    def header(self):
        display_mode = HEADER_DISPLAY_MODE.FULL.value
        settings = self.view.renderer_settings
        if ISiteContainerSummaryPortletBaseRendererSettings.providedBy(settings):
            display_mode = settings.header_display_mode
        if display_mode == HEADER_DISPLAY_MODE.HIDDEN.value:
            return ''
        header = self.request.registry.queryMultiAdapter((self.context, self.request, self.view),
                                                         ISiteContainerSummaryItemHeader)
        if display_mode == HEADER_DISPLAY_MODE.START.value:
            header = get_text_start(header, settings.start_length)
        return header
    
    @property
    def illustration(self):
        return self.request.registry.queryMultiAdapter((self.context, self.request),
                                                       IContentNavigationIllustration)

    @property
    def button_title(self):
        title = self.request.registry.queryMultiAdapter((self.context, self.request),
                                                        ISiteContainerSummaryItemButtonTitle)
        if (not title) and ('button_title' in getFieldNames(self.view.settings_interface)):
            title = II18n(self.view.renderer_settings).query_attribute('button_title',
                                                                       request=self.request)
        if not title:
            title = II18n(self.view.settings).query_attribute('button_title', request=self.request)
        return title
    
    @property
    def url(self):
        return self.request.registry.queryMultiAdapter((self.context, self.request, self.view),
                                                       ISiteContainerSummaryItemURL)
    