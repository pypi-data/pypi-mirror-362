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

"""PyAMS_content.component.verbatim.skin module

This module defines renderers for verbatim paragraph.
"""
from pyams_content.component.illustration import IIllustration
from pyams_content.component.verbatim.interfaces import IVerbatimParagraph
from pyams_content.feature.renderer import DefaultContentRenderer, IRendererSettings
from pyams_content.feature.renderer.interfaces import IContentRenderer
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import DEFAULT_RENDERER_NAME
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config

__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(name=DEFAULT_RENDERER_NAME,
                required=(IVerbatimParagraph, IPyAMSLayer),
                provides=IContentRenderer)
@template_config(template='templates/verbatim-default.pt',
                 layer=IPyAMSLayer)
class VerbatimParagraphDefaultRenderer(DefaultContentRenderer):
    """Verbatim paragraph default renderer"""

    label = _("Full width verbatim (default)")

    @property
    def illustration_selections(self):
        illustration = IIllustration(self.context, None)
        if (illustration is not None) and illustration.has_data():
            renderer_settings = IRendererSettings(illustration, None)
            selection = getattr(renderer_settings, 'thumb_selection', None)
            if selection:
                selection = selection.copy()
                selection['xs'].cols = 12
                selection['sm'].cols = 3
                selection['md'].cols = 2
                selection['lg'].cols = 2
                selection['xl'].cols = 2
            return selection
        return None
        