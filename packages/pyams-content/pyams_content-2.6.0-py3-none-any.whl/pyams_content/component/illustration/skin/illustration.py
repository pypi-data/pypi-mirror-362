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

"""PyAMS_content.component.illustration.skin.illustration module

This module provides base illustrations renderers.
"""

from persistent import Persistent
from zope.container.contained import Contained
from zope.interface import implementer
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.illustration import IParagraphIllustration
from pyams_content.component.illustration.skin.interfaces import \
    IIllustrationDefaultRendererSettings, IIllustrationRenderer, ILLUSTRATION_AFTER_BODY, \
    ILLUSTRATION_BEFORE_BODY, IParagraphIllustrationSideRendererSettings
from pyams_content.feature.renderer import BaseContentRenderer, IContentRenderer
from pyams_portal.interfaces import DEFAULT_RENDERER_NAME
from pyams_layer.interfaces import IPyAMSLayer
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_utils.factory import factory_config


__docformat__ = 'restructuredtext'

from pyams_content import _


#
# Illustrations renderer settings
#

@factory_config(IIllustrationDefaultRendererSettings)
class IllustrationDefaultRendererSettings(Persistent, Contained):
    """Illustration paragraph default renderer settings"""

    thumb_selection = FieldProperty(
        IIllustrationDefaultRendererSettings['thumb_selection'])


@factory_config(IParagraphIllustrationSideRendererSettings)
class ParagraphIllustrationSideRendererSettings(IllustrationDefaultRendererSettings):
    """Illustration paragraph side renderer settings"""

    thumb_selection = FieldProperty(
        IParagraphIllustrationSideRendererSettings['thumb_selection'])
    zoom_on_click = FieldProperty(
        IParagraphIllustrationSideRendererSettings['zoom_on_click'])


#
# Illustrations renderers
#

@implementer(IIllustrationRenderer)
class BaseIllustrationRenderer(BaseContentRenderer):
    """Base illustration renderer"""

    settings_interface = IIllustrationDefaultRendererSettings
    position = None


@adapter_config(name='centered-before',
                required=(IParagraphIllustration, IPyAMSLayer),
                provides=IContentRenderer)
@template_config(template='templates/illustration-default.pt', layer=IPyAMSLayer)
class ParagraphIllustrationBeforeTextRenderer(BaseIllustrationRenderer):
    """Illustration centered before text renderer"""

    label = _("Centered image before text")

    position = ILLUSTRATION_BEFORE_BODY
    weight = 10


@template_config(template='templates/illustration-side.pt', layer=IPyAMSLayer)
class BaseParagraphIllustrationSideRenderer(BaseIllustrationRenderer):
    """Base illustration side renderer"""

    settings_interface = IParagraphIllustrationSideRendererSettings
    position = ILLUSTRATION_BEFORE_BODY

    css_class = None

    def get_css_class(self):
        """CSS class getter"""
        selection = self.settings.thumb_selection
        cols = ' '.join((
            f'col-{selection.cols}' if device == 'xs' else f'col-{device}-{selection.cols}'
            for device, selection in selection.items()
        ))
        return f'{self.css_class} {cols}'


@adapter_config(name='float-left',
                required=(IParagraphIllustration, IPyAMSLayer),
                provides=IContentRenderer)
class ParagraphIllustrationLeftFloatRenderer(BaseParagraphIllustrationSideRenderer):
    """Left floating illustration renderer"""

    label = _("Floating illustration to the left")
    css_class = 'float-left mr-3'

    weight = 20


@adapter_config(name='float-right',
                required=(IParagraphIllustration, IPyAMSLayer),
                provides=IContentRenderer)
class ParagraphIllustrationRightFloatRenderer(BaseParagraphIllustrationSideRenderer):
    """Right floating illustration renderer"""

    label = _("Floating illustration to the right")
    css_class = 'float-right ml-3'

    weight = 30


@adapter_config(name=DEFAULT_RENDERER_NAME,
                required=(IParagraphIllustration, IPyAMSLayer),
                provides=IContentRenderer)
@template_config(template='templates/illustration-default.pt', layer=IPyAMSLayer)
class ParagraphIllustrationAfterTextRenderer(BaseIllustrationRenderer):
    """Illustration centered after text renderer"""

    label = _("Centered image after text (default)")

    position = ILLUSTRATION_AFTER_BODY
    weight = 40
