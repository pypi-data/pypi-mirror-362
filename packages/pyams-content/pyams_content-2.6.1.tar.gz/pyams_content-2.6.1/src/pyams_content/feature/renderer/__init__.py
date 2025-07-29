#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.features.renderer module

Content renderers are a very common pattern, which allows to separated *what* will be
rendered from *how* it will be rendered, and the *renderer* is used to specify the *how*:
so, for a given component, you can often choose the renderer which will be used to render
this component.
"""

from pyramid.decorator import reify
from zope.interface import implementer
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_content.feature.renderer.interfaces import IContentRenderer, IRenderedContent, IRendererSettings, \
    RENDERER_SETTINGS_KEY
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import DEFAULT_RENDERER_NAME, HIDDEN_RENDERER_NAME
from pyams_utils.adapter import adapter_config, get_annotation_adapter
from pyams_utils.factory import get_object_factory
from pyams_utils.request import check_request
from pyams_viewlet.viewlet import BaseContentProvider

__docformat__ = 'restructuredtext'

from pyams_content import _


@implementer(IRenderedContent)
class RenderedContentMixin:
    """Renderer mixin interface"""

    renderer = None
    """Attribute used to store selected content renderer.
    Subclasses should generally override this attribute to define a "Choice" field property based
    on a given renderers vocabulary.
    """

    renderer_interface = IContentRenderer
    """Content renderer interface"""

    def get_renderer(self, request=None):
        """Get rendering adapter based on selected renderer name"""
        if request is None:
            request = check_request()
        renderer = request.registry.queryMultiAdapter((self, request), self.renderer_interface,
                                                      name=self.renderer or '')
        if (renderer is not None) and ('lang' in request.params):
            renderer.language = request.params['lang']
        return renderer


@adapter_config(required=IRenderedContent,
                provides=IContentRenderer)
def rendered_content_renderer_factory(context):
    """Rendered content renderer factory"""
    return context.get_renderer()


@adapter_config(required=IRenderedContent,
                provides=IRendererSettings)
def rendered_content_renderer_settings_factory(context):
    """Rendered content renderer settings factory"""
    renderer = IContentRenderer(context)
    if (renderer is None) or (renderer.settings_interface is None):
        return None
    return get_annotation_adapter(context,
                                  f'{RENDERER_SETTINGS_KEY}::{context.renderer}',
                                  renderer.settings_interface, name='++renderer++')


class RenderersVocabulary(SimpleVocabulary):
    """Renderers vocabulary base class"""

    renderer_interface = IContentRenderer
    """Renderer interface"""

    content_interface = IRenderedContent
    """Interface used to check current context"""

    content_factory = None
    """Factory used to create a new context if current context doesn't implements required
    interface. If no factory is given, vocabulary is looking for default object factory for
    given interface.
    """

    def __init__(self, context=None):
        request = check_request()
        translate = request.localizer.translate
        registry = request.registry
        if not self.content_interface.providedBy(context):
            factory = self.content_factory
            if factory is None:
                factory = get_object_factory(self.content_interface)
            if factory is not None:
                context = factory()
        terms = [
            SimpleTerm(name, title=translate(adapter.label))
            for name, adapter in sorted(registry.getAdapters((context, request),
                                                             self.renderer_interface),
                                        key=lambda x: x[1].weight)
        ]
        super().__init__(terms)


@implementer(IContentRenderer)
class BaseContentRenderer(BaseContentProvider):
    """Base content renderer"""

    label = None
    weight = 0

    settings_interface = None

    @reify
    def settings(self):
        """Renderer settings getter"""
        if self.settings_interface is None:
            return None
        return IRendererSettings(self.context)


@adapter_config(name=HIDDEN_RENDERER_NAME,
                required=(IRenderedContent, IPyAMSLayer),
                provides=IContentRenderer)
class HiddenContentRenderer(BaseContentRenderer):
    """Hidden content renderer"""

    label = _("Hidden content")
    weight = -999

    def render(self, template_name=''):
        """Renderer output"""
        return ''


@adapter_config(name=DEFAULT_RENDERER_NAME,
                required=(IRenderedContent, IPyAMSLayer),
                provides=IContentRenderer)
class DefaultContentRenderer(BaseContentRenderer):
    """Default content renderer"""

    label = _("Default content renderer")
