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

"""PyAMS_content.shared.view.portlet.skin module

This module defines several renderers of view items portlet.
"""

from persistent import Persistent
from zope.container.contained import Contained
from zope.interface import Interface, implementer
from zope.location.interfaces import ILocation
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.links import IInternalLink
from pyams_content.feature.filter.container import FilterContainer
from pyams_content.feature.filter.interfaces import IAggregatedPortletRendererSettings
from pyams_content.feature.header.interfaces import HEADER_DISPLAY_MODE
from pyams_content.shared.common import IWfSharedContent
from pyams_content.shared.view.portlet import IViewItemsPortletSettings
from pyams_content.shared.view.portlet.skin.interfaces import IViewItemHeader, IViewItemRenderer, IViewItemTargetURL, \
    IViewItemTitle, IViewItemURL, IViewItemsPortletBaseRendererSettings, IViewItemsPortletCardsRendererSettings, \
    IViewItemsPortletMasonryCardsRendererSettings, IViewItemsPortletPanelsRendererSettings, \
    IViewItemsPortletThumbnailsRendererSettings, IViewItemsPortletVerticalRendererSettings
from pyams_content.shared.view.skin.interfaces import IViewItemsView
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer, IPyAMSUserLayer
from pyams_portal.interfaces import IPortalContext, IPortletRenderer
from pyams_portal.skin import PortletRenderer
from pyams_sequence.reference import InternalReferenceMixin
from pyams_skin.interfaces.viewlet import IBreadcrumbs
from pyams_template.template import template_config
from pyams_utils.adapter import NullAdapter, adapter_config
from pyams_utils.factory import factory_config
from pyams_utils.text import get_text_start
from pyams_utils.url import canonical_url, relative_url
from pyams_viewlet.viewlet import ViewContentProvider

__docformat__ = 'restructuredtext'

from pyams_content import _


@implementer(IAggregatedPortletRendererSettings)
class BaseViewItemsPortletRendererSettings(FilterContainer):
    """Base view items portlet renderer settings"""

    paginate = FieldProperty(IViewItemsPortletBaseRendererSettings['paginate'])
    page_size = FieldProperty(IViewItemsPortletBaseRendererSettings['page_size'])
    filters_css_class = FieldProperty(IViewItemsPortletBaseRendererSettings['filters_css_class'])
    results_css_class = FieldProperty(IViewItemsPortletBaseRendererSettings['results_css_class'])
    display_illustrations = FieldProperty(IViewItemsPortletBaseRendererSettings['display_illustrations'])

    
@implementer(IViewItemsView)
class BaseViewItemsPortletRenderer(PortletRenderer):
    """Base view items portlet renderer"""

    @staticmethod
    def is_internal_link(link):
        """Internal link checker"""
        return IInternalLink.providedBy(link)

    def get_url(self, target, view_name=None, query=None):
        """Item URL getter"""
        target_url = self.request.registry.queryMultiAdapter((target, self.request),
                                                             IViewItemTargetURL)
        if target_url is not None:
            if target_url.target is None:
                return target_url.url
            target = target_url.target
        if self.settings.force_canonical_url:
            return canonical_url(target, self.request, view_name, query)
        return relative_url(target, self.request, view_name=view_name, query=query)

    def render(self, template_name=''):
        result = super().render(template_name)
        if self.settings.first_page_only:
            start = int(self.request.params.get('start', 0))
            if start:
                return ''
        return result

    def render_item(self, item, template_name=''):
        renderer = self.request.registry.queryMultiAdapter((item, self.request, self),
                                                           IViewItemRenderer)
        if renderer is not None:
            renderer.update()
            return renderer.render(template_name)
        return ''


#
# Vertical list view items renderer
#

@factory_config(IViewItemsPortletVerticalRendererSettings)
class ViewItemsPortletVerticalRendererSettings(InternalReferenceMixin, BaseViewItemsPortletRendererSettings):
    """View items portlet vertical renderer settings"""

    thumb_selection = FieldProperty(IViewItemsPortletVerticalRendererSettings['thumb_selection'])
    display_breadcrumbs = FieldProperty(IViewItemsPortletVerticalRendererSettings['display_breadcrumbs'])
    display_tags = FieldProperty(IViewItemsPortletVerticalRendererSettings['display_tags'])
    reference = FieldProperty(IViewItemsPortletVerticalRendererSettings['reference'])
    link_label = FieldProperty(IViewItemsPortletVerticalRendererSettings['link_label'])


@adapter_config(required=(IPortalContext, IPyAMSLayer, Interface, IViewItemsPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/view-list-default.pt', layer=IPyAMSLayer)
class ViewItemsPortletVerticalRenderer(BaseViewItemsPortletRenderer):
    """View items portlet vertical renderer"""

    label = _("Simple vertical list (default)")
    weight = 1

    settings_interface = IViewItemsPortletVerticalRendererSettings


#
# Horizontal list view items renderer
#

@factory_config(IViewItemsPortletThumbnailsRendererSettings)
class ViewItemsPortletThumbnailsRendererSettings(BaseViewItemsPortletRendererSettings):
    """View items portlet thumbnails renderer settings"""

    paginate = None
    page_size = None
    
    thumb_selection = FieldProperty(IViewItemsPortletThumbnailsRendererSettings['thumb_selection'])


@adapter_config(name='thumbnails',
                required=(IPortalContext, IPyAMSLayer, Interface, IViewItemsPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/view-list-thumbnails.pt', layer=IPyAMSLayer)
class ViewItemsPortletThumbnailsRenderer(BaseViewItemsPortletRenderer):
    """View items portlet horizontal renderer"""

    label = _("Horizontal thumbnails list")
    weight = 10

    settings_interface = IViewItemsPortletThumbnailsRendererSettings


#
# Panels view items renderer
#

@factory_config(IViewItemsPortletPanelsRendererSettings)
class ViewItemsPortletPanelsRendererSettings(BaseViewItemsPortletRendererSettings):
    """View items portlet panels renderer settings"""

    thumb_selection = FieldProperty(IViewItemsPortletPanelsRendererSettings['thumb_selection'])
    columns_count = FieldProperty(IViewItemsPortletPanelsRendererSettings['columns_count'])
    header_display_mode = FieldProperty(IViewItemsPortletPanelsRendererSettings['header_display_mode'])
    start_length = FieldProperty(IViewItemsPortletPanelsRendererSettings['start_length'])

    def get_css_class(self):
        columns = self.columns_count
        return ' '.join((
            f'row-cols-{selection.cols}' if device == 'xs' else f'row-cols-{device}-{selection.cols}'
            for device, selection in columns.items()
        ))


@adapter_config(name='panels',
                required=(IPortalContext, IPyAMSLayer, Interface, IViewItemsPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/view-list-panels.pt', layer=IPyAMSLayer)
class ViewItemsPortletPanelsRenderer(BaseViewItemsPortletRenderer):
    """View items portlet panels renderer"""

    label = _("Vertical panels with illustrations")
    weight = 30

    settings_interface = IViewItemsPortletPanelsRendererSettings

    def get_header(self, item):
        settings = self.renderer_settings
        display_mode = settings.header_display_mode
        if display_mode == HEADER_DISPLAY_MODE.HIDDEN.value:
            return ''
        header = II18n(item).query_attribute('header', request=self.request)
        if display_mode == HEADER_DISPLAY_MODE.START.value:
            header = get_text_start(header, settings.start_length)
        return header


#
# Cards view items renderer
#

@factory_config(IViewItemsPortletCardsRendererSettings)
class ViewItemsPortletCardsRendererSettings(ViewItemsPortletPanelsRendererSettings):
    """View items portlet cards renderer settings"""


@adapter_config(name='cards',
                required=(IPortalContext, IPyAMSLayer, Interface, IViewItemsPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/view-list-cards.pt', layer=IPyAMSLayer)
class ViewItemsPortletCardsRenderer(BaseViewItemsPortletRenderer):
    """View items portlet cards renderer"""

    label = _("Bootstrap cards grid")
    weight = 40

    settings_interface = IViewItemsPortletCardsRendererSettings


#
# Masonry cards view items renderer
#

@factory_config(IViewItemsPortletMasonryCardsRendererSettings)
class ViewItemsPortletMasonryCardsRendererSettings(ViewItemsPortletCardsRendererSettings):
    """View items portlet Masonry cards renderer settings"""

    def get_css_class(self):
        columns = self.columns_count
        return ' '.join((
            f'columns-{selection.cols}' if device == 'xs' else f'columns-{device}-{selection.cols}'
            for device, selection in columns.items()
        ))


@adapter_config(name='cards::masonry',
                required=(IPortalContext, IPyAMSLayer, Interface, IViewItemsPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/view-list-cards-masonry.pt', layer=IPyAMSLayer)
class ViewItemsPortletMasonryCardsRenderer(BaseViewItemsPortletRenderer):
    """View items portlet Masonry cards renderer"""

    label = _("Bootstrap cards grid, Masonry style")
    weight = 50

    settings_interface = IViewItemsPortletMasonryCardsRendererSettings


#
# View items adapters
#

@adapter_config(required=(ILocation, IPyAMSUserLayer, IViewItemsView),
                provides=IBreadcrumbs)
class LocationBreadcrumbsAdapter(NullAdapter):
    """Disable breadcrumbs in view items view"""


@adapter_config(required=(IWfSharedContent, IPyAMSUserLayer, IViewItemsView),
                provides=IViewItemTitle)
def shared_content_result_title_adapter(context, request, view):
    """Shared content result title adapter"""
    return II18n(context).query_attribute('title', request=request)


@adapter_config(required=(IWfSharedContent, IPyAMSUserLayer, IViewItemsView),
                provides=IViewItemHeader)
def shared_content_result_header_adapter(context, request, view):
    """Shared content result header adapter"""
    return II18n(context).query_attribute('header', request=request)


@adapter_config(required=(IWfSharedContent, IPyAMSUserLayer, IViewItemsView),
                provides=IViewItemURL)
def shared_content_result_target_adapter(context, request, view):
    """Shared content result target URL adapter"""
    if view.settings.force_canonical_url:
        return canonical_url(context, request)
    return relative_url(context, request)


#
# View items renderers
#

@adapter_config(required=(IWfSharedContent, IPyAMSUserLayer, IViewItemsView),
                provides=IViewItemRenderer)
@template_config(template='templates/view-item.pt', layer=IPyAMSUserLayer)
@template_config(name='thumbnail',
                 template='templates/view-item-thumbnail.pt', layer=IPyAMSUserLayer)
@template_config(name='panel',
                 template='templates/view-item-panel.pt', layer=IPyAMSUserLayer)
@template_config(name='card',
                 template='templates/view-item-card.pt', layer=IPyAMSUserLayer)
@template_config(name='masonry',
                 template='templates/view-item-masonry.pt', layer=IPyAMSUserLayer)
class WfSharedContentViewItemRenderer(ViewContentProvider):
    """Shared content view item renderer"""

    @property
    def title(self):
        return self.request.registry.queryMultiAdapter((self.context, self.request, self.view),
                                                       IViewItemTitle)

    @property
    def header(self):
        display_mode = HEADER_DISPLAY_MODE.FULL.value
        settings = self.view.renderer_settings
        if IViewItemsPortletPanelsRendererSettings.providedBy(settings):
            display_mode = settings.header_display_mode
        if display_mode == HEADER_DISPLAY_MODE.HIDDEN.value:
            return ''
        header = self.request.registry.queryMultiAdapter((self.context, self.request, self.view),
                                                         IViewItemHeader)
        if display_mode == HEADER_DISPLAY_MODE.START.value:
            header = get_text_start(header, settings.start_length)
        return header

    @property
    def url(self):
        return self.request.registry.queryMultiAdapter((self.context, self.request, self.view),
                                                       IViewItemURL)
