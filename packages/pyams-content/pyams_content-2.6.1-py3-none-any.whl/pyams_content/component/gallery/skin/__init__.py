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

"""PyAMS_content.component.gallery.skin module

"""

from persistent import Persistent
from zope.container.contained import Contained
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.gallery.interfaces import IGalleryParagraph
from pyams_content.component.gallery.skin.interfaces import IGalleryCarouselRendererSettings, \
    IGalleryDefaultRendererSettings, IGalleryRandomImageRendererSettings
from pyams_content.feature.renderer import BaseContentRenderer, IContentRenderer
from pyams_portal.interfaces import DEFAULT_RENDERER_NAME
from pyams_layer.interfaces import IPyAMSLayer
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_utils.factory import factory_config
from pyams_utils.list import random_iter


__docformat__ = 'restructuredtext'

from pyams_content import _


class BaseGalleryRenderer(BaseContentRenderer):
    """Base gallery renderer"""


#
# Default gallery renderer
#

@factory_config(IGalleryDefaultRendererSettings)
class GalleryDefaultRendererSettings(Persistent, Contained):
    """Gallery default renderer settings"""

    thumb_selection = FieldProperty(
        IGalleryDefaultRendererSettings['thumb_selection'])

    def get_css_cols(self):
        """Get CSS cols matching current selections"""
        return ' '.join([
            f"col-{'{}-'.format(device) if device != 'xs' else ''}{selection.cols}"
            for device, selection in self.thumb_selection.items()
        ])


@adapter_config(name=DEFAULT_RENDERER_NAME,
                required=(IGalleryParagraph, IPyAMSLayer),
                provides=IContentRenderer)
@template_config(template='templates/gallery-default.pt', layer=IPyAMSLayer)
class GalleryParagraphDefaultRenderer(BaseGalleryRenderer):
    """Gallery paragraph default renderer"""

    label = _("Grid gallery renderer (default)")

    settings_interface = IGalleryDefaultRendererSettings
    weight = 10


#
# Carousel gallery renderer
#

@factory_config(IGalleryCarouselRendererSettings)
class GalleryCarouselRendererSettings(Persistent, Contained):
    """Gallery carousel renderer settings"""

    thumb_selection = FieldProperty(
        IGalleryCarouselRendererSettings['thumb_selection'])


@adapter_config(name='carousel',
                required=(IGalleryParagraph, IPyAMSLayer),
                provides=IContentRenderer)
@template_config(template='templates/gallery-carousel.pt', layer=IPyAMSLayer)
class GalleryParagraphCarouselRenderer(BaseGalleryRenderer):
    """Gallery paragraph carousel renderer"""

    label = _("Carousel gallery renderer")

    settings_interface = IGalleryCarouselRendererSettings
    weight = 20


#
# Random image gallery renderer
#

@factory_config(IGalleryRandomImageRendererSettings)
class GalleryRandomImageRendererSettings(Persistent, Contained):
    """Gallery random image renderer settings"""

    thumb_selection = FieldProperty(
        IGalleryRandomImageRendererSettings['thumb_selection'])


@adapter_config(name='random',
                required=(IGalleryParagraph, IPyAMSLayer),
                provides=IContentRenderer)
@template_config(template='templates/gallery-random.pt', layer=IPyAMSLayer)
class GalleryRandomImageRenderer(BaseGalleryRenderer):
    """Gallery paragraph random image renderer"""

    label = _("Random image renderer")

    settings_interface = IGalleryRandomImageRendererSettings
    weight = 30

    def get_media(self):
        """Visible media getter"""
        return next(random_iter(self.context.get_visible_medias()))
