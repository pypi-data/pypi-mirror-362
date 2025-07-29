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

"""PyAMS_content.component.video.skin module

This module defines default external video paragraph renderer.
"""

from pyams_content.component.video.interfaces import IExternalVideoParagraph
from pyams_content.component.video.skin.interfaces import IExternalVideoRenderer
from pyams_content.feature.renderer import DefaultContentRenderer, IContentRenderer
from pyams_portal.interfaces import DEFAULT_RENDERER_NAME
from pyams_layer.interfaces import IPyAMSLayer
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config

__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(name=DEFAULT_RENDERER_NAME,
                required=(IExternalVideoParagraph, IPyAMSLayer),
                provides=IContentRenderer)
@template_config(template='templates/video-default.pt', layer=IPyAMSLayer)
class ExternalVideoParagraphDefaultRenderer(DefaultContentRenderer):
    """External video paragraph default renderer"""

    label = _("External video renderer (default)")

    video_renderer = None

    def update(self):
        super().update()
        provider = self.context.get_provider()
        if provider is None:
            return ''
        registry = self.request.registry
        renderer = registry.queryMultiAdapter((self.context.settings, self.request),
                                              IExternalVideoRenderer)
        if renderer is not None:
            renderer.update()
        self.video_renderer = renderer

    def render_video(self):
        """Video renderer"""
        if self.video_renderer is None:
            return ''
        return self.video_renderer.render()
