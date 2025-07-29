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

"""PyAMS_content.component.gallery.portlet.skin module

This module defines gallery portlet renderers.
"""

from persistent import Persistent
from zope.container.contained import Contained
from zope.interface import Interface
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.gallery import IGallery
from pyams_content.component.gallery.portlet import IGalleryPortletSettings
from pyams_content.component.gallery.portlet.skin.interfaces import \
    IGalleryPortletCarouselRendererSettings, IGalleryPortletDefaultRendererSettings
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import IPortalContext, IPortletRenderer
from pyams_portal.skin import PortletRenderer
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_utils.factory import factory_config
from pyams_utils.list import random_iter

__docformat__ = 'restructuredtext'

from pyams_content import _


class BaseGalleryPortletRenderer(PortletRenderer):
    """Base gallery portlet renderer"""

    def get_visible_medias(self):
        """Visible medias getter"""
        settings = self.settings
        gallery = IGallery(self.context, None)
        if gallery is not None:
            yield from gallery.get_visible_medias()
        yield from settings.get_visible_medias()


#
# Default gallery portlet renderer
#

@factory_config(provided=IGalleryPortletDefaultRendererSettings)
class GalleryPortletDefaultRendererSettings(Persistent, Contained):
    """Gallery portlet default renderer settings"""

    thumb_selection = FieldProperty(IGalleryPortletDefaultRendererSettings['thumb_selection'])

    def get_css_cols(self):
        """Get CSS cols matching current selections"""
        return ' '.join([
            f"col-{'{}-'.format(device) if device != 'xs' else ''}{selection.cols}"
            for device, selection in self.thumb_selection.items()
        ])


@adapter_config(required=(IPortalContext, IPyAMSLayer, Interface, IGalleryPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/gallery-default.pt', layer=IPyAMSLayer)
class GalleryPortletDefaultRenderer(BaseGalleryPortletRenderer):
    """Gallery portlet default renderer"""

    label = _("Grid gallery renderer (default)")

    settings_interface = IGalleryPortletDefaultRendererSettings
    weight = 10


#
# Carousel gallery portlet renderer
#

@factory_config(provided=IGalleryPortletCarouselRendererSettings)
class GalleryPortletCarouselRendererSettings(Persistent, Contained):
    """Gallery portlet carousel renderer settings"""

    thumb_selection = FieldProperty(IGalleryPortletCarouselRendererSettings['thumb_selection'])


@adapter_config(name='carousel',
                required=(IPortalContext, IPyAMSLayer, Interface, IGalleryPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/gallery-carousel.pt', layer=IPyAMSLayer)
class GalleryPortletCarouselRenderer(BaseGalleryPortletRenderer):
    """Gallery carousel default renderer"""

    label = _("Carousel gallery renderer")

    settings_interface = IGalleryPortletCarouselRendererSettings
    weight = 20


#
# Random image gallery portlet renderer
#

@factory_config(provided=IGalleryPortletCarouselRendererSettings)
class GalleryPortletRandomImageRendererSettings(Persistent, Contained):
    """Gallery portlet random image renderer settings"""

    thumb_selection = FieldProperty(IGalleryPortletCarouselRendererSettings['thumb_selection'])


@adapter_config(name='random',
                required=(IPortalContext, IPyAMSLayer, Interface, IGalleryPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/gallery-random.pt', layer=IPyAMSLayer)
class GalleryPortletRandomImageRenderer(BaseGalleryPortletRenderer):
    """Gallery carousel random image renderer"""

    label = _("Random image renderer")

    settings_interface = IGalleryPortletCarouselRendererSettings
    weight = 30

    def get_media(self):
        """Visible media getter"""
        return next(random_iter(self.settings.get_visible_medias()))
