#
# Copyright (c) 2015-2022 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.component.paragraph.portlet.skin module

This module defines paragraph container portlet renderer.
"""

from zope.interface import Interface

from pyams_content.component.paragraph.interfaces import IParagraphContainer
from pyams_content.component.paragraph.portlet import IParagraphNavigationPortletSettings
from pyams_content.component.paragraph.portlet.interfaces import \
    IParagraphContainerPortletSettings
from pyams_content.component.paragraph.portlet.skin.interfaces import \
    IParagraphContainerPortletRenderer
from pyams_content.feature.renderer.interfaces import ISharedContentRenderer
from pyams_content.shared.site.interfaces import ISiteContainer
from pyams_content.skin.interfaces import IContentSummaryInfo
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import IPortalContext, IPortletRenderer
from pyams_portal.skin import PortletRenderer
from pyams_sequence.interfaces import IInternalReference, ISequentialIdInfo
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_utils.list import is_not_none


__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(required=(IPortalContext, IPyAMSLayer, Interface,
                          IParagraphContainerPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/container-default.pt', layer=IPyAMSLayer)
class ParagraphsContainerPortletRenderer(PortletRenderer):
    """Paragraphs container portlet renderer

    By default, this renderer is applying the renderer selected on each of its
    context container paragraphs.

    But you can define a custom renderer providing *IParagraphContainerPortletRenderer*,
    which will be registered with a view name; if used, and if this view name is
    matching the current request view name, this renderer will be used instead of the default
    one.

    For an example, look at form shared content submit rendering...
    """

    label = _("Paragraphs list (default)")
    weight = 1

    renderers = ()
    custom_renderer = None

    template_name = ''

    def update(self):
        super().update()
        settings = self.settings
        if settings.reference:
            source = settings.target
        else:
            source = self.context
        registry = self.request.registry
        renderer = self.custom_renderer = registry.queryMultiAdapter(
            (source, self.request, self.view), IParagraphContainerPortletRenderer,
            name=self.request.view_name)
        if renderer is not None:
            self.renderers = [renderer]
        else:
            container = IParagraphContainer(source, None)
            if container is not None:
                paragraphs = container.get_visible_paragraphs(
                    names=settings.paragraphs,
                    anchors_only=settings.anchors_only,
                    exclude_anchors=settings.exclude_anchors,
                    factories=settings.factories,
                    excluded_factories=settings.excluded_factories,
                    limit=settings.limit)
                renderers = [
                    paragraph.get_renderer(self.request)
                    for paragraph in paragraphs
                ]
            else:
                renderers = [
                    adapter
                    for name, adapter in sorted(
                        registry.getAdapters((source, self.request),
                                             ISharedContentRenderer),
                        key=lambda x: x[1].weight)
                ]
            self.renderers = tuple(filter(is_not_none, renderers))
        [renderer.update() for renderer in self.renderers]

    @property
    def use_portlets_cache(self):
        """Portlets cache checker"""
        use_cache = super().use_portlets_cache
        if use_cache and (self.custom_renderer is not None):
            return self.custom_renderer.use_portlets_cache
        return use_cache

    def get_cache_key(self):
        """Cache key getter"""
        key = super().get_cache_key()
        if self.custom_renderer is not None:
            key = f'{key}::{self.request.view_name}'
        return key

    def get_navigation_links(self):
        """Navigation links getter"""

        def test_item(nav_item):
            """Navigation item test"""
            item_sequence = ISequentialIdInfo(nav_item, None)
            if (item_sequence is not None) and (item_sequence.oid == context_sequence.oid):
                return True
            if IInternalReference.providedBy(nav_item) and \
                    (nav_item.reference == context_sequence.hex_oid):
                return True
            return False

        prev_nav, next_nav = None, None
        context_sequence = ISequentialIdInfo(self.context, None)
        if context_sequence is not None:
            display_context = self.request.display_context
            if ISiteContainer.providedBy(display_context):
                registry = self.request.registry
                previous_item = None
                items = display_context.get_visible_items(self.request)
                for item in items:
                    if test_item(item):
                        prev_nav = registry.queryMultiAdapter((previous_item, self.request),
                                                              IContentSummaryInfo)
                        break
                    previous_item = item
                try:
                    next_item = next(items)
                except (StopIteration, RuntimeError):
                    pass
                else:
                    next_nav = registry.queryMultiAdapter((next_item, self.request),
                                                          IContentSummaryInfo)
        return prev_nav, next_nav


@adapter_config(required=(IPortalContext, IPyAMSLayer, Interface,
                          IParagraphNavigationPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/navigation-default.pt', layer=IPyAMSLayer)
class ParagraphsNavigationPortletRenderer(PortletRenderer):
    """Paragraphs navigation portlet renderer

    By default, this renderer is applying the renderer selected on each of its
    context container paragraphs.

    But you can define a custom renderer providing *IParagraphContainerPortletRenderer*,
    which will be registered with a view name; if used, and if this view name is
    matching the current request view name, this renderer will be used instead of the default
    one.

    For an example, look at form shared content submit rendering...
    """

    label = _("Paragraphs navigation (default)")
    weight = 1

    paragraphs = ()

    def update(self):
        super().update()
        container = IParagraphContainer(self.context, None)
        if container is not None:
            settings = self.settings
            self.paragraphs = container.get_visible_paragraphs(
                names=settings.paragraphs,
                anchors_only=settings.anchors_only,
                factories=settings.factories,
                excluded_factories=settings.excluded_factories)
