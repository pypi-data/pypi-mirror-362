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

"""PyAMS_content.component.illustration.portlet.skin module

This module defines illustration portlet renderers.
"""

from persistent import Persistent
from zope.container.contained import Contained
from zope.interface import Interface
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.illustration import IIllustration
from pyams_content.component.illustration.portlet.interfaces import IIllustrationPortletContent, \
    IIllustrationPortletSettings
from pyams_content.component.illustration.portlet.skin.interfaces import \
    IIllustrationPortletBaseRendererSettings, IIllustrationPortletDefaultRendererSettings, \
    IIllustrationPortletSideRendererSettings
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import HIDDEN_RENDERER_NAME, IPortalContext, IPortletCSSClass, IPortletRenderer
from pyams_portal.skin import PortletRenderer
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_utils.factory import factory_config

__docformat__ = 'restructuredtext'

from pyams_content import _


@factory_config(IIllustrationPortletBaseRendererSettings)
class IllustrationPortletBaseRendererSettings(Persistent, Contained):
    """Illustration portlet base renderer settings"""

    thumb_selection = FieldProperty(
        IIllustrationPortletBaseRendererSettings['thumb_selection'])


class BaseIllustrationPortletRenderer(PortletRenderer):
    """Base illustration portlet renderer"""

    @property
    def illustration(self):
        """Illustration getter"""
        registry = self.request.registry
        context = self.request.context
        for illustration in (
                registry.queryMultiAdapter((context, self.request, self.view), IIllustrationPortletContent),
                IIllustration(context, None),
                registry.queryMultiAdapter((self.context, self.request, self.view), IIllustrationPortletContent),
                IIllustration(self.context, None)):
            if (illustration is not None) and \
                    (illustration.renderer != HIDDEN_RENDERER_NAME) and \
                    illustration.has_data():
                return illustration
        return None


#
# Illustration portlet default renderer
#

@factory_config(IIllustrationPortletDefaultRendererSettings)
class IllustrationPortletDefaultRendererSettings(IllustrationPortletBaseRendererSettings):
    """Illustration portlet default renderer settings"""

    display_title = FieldProperty(IIllustrationPortletDefaultRendererSettings['display_title'])
    display_author = FieldProperty(IIllustrationPortletDefaultRendererSettings['display_author'])
    display_description = FieldProperty(
        IIllustrationPortletDefaultRendererSettings['display_description'])


@adapter_config(required=(IPortalContext, IPyAMSLayer, Interface, IIllustrationPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/illustration-default.pt', layer=IPyAMSLayer)
class IllustrationPortletDefaultRenderer(BaseIllustrationPortletRenderer):
    """Illustration portlet default renderer"""

    label = _("Full width illustration (default)")

    settings_interface = IIllustrationPortletDefaultRendererSettings
    weight = 10


#
# Illustration portlet side renderers
#

@factory_config(IIllustrationPortletSideRendererSettings)
class IllustrationPortletSideRendererSettings(IllustrationPortletBaseRendererSettings):
    """Illustration portlet base renderer settings"""

    thumb_selection = FieldProperty(
        IIllustrationPortletSideRendererSettings['thumb_selection'])
    zoom_on_click = FieldProperty(
        IIllustrationPortletSideRendererSettings['zoom_on_click'])

    def get_css_cols(self, side):
        """Get CSS cols matching current selections"""
        return ' '.join([
            f"float-{'{}-'.format(device) if device != 'xs' else ''}"
            f"{'none' if selection.cols==12 else side} "
            f"col-{'{}-'.format(device) if device != 'xs' else ''}{selection.cols} "
            f"mx-{'{}-'.format(device) if device != 'xs' else ''}"
            f"{'0' if selection.cols==12 else '3'}"
            for device, selection in self.thumb_selection.items()
        ])


@template_config(template='templates/illustration-side.pt', layer=IPyAMSLayer)
class IllustrationPortletSideRenderer(BaseIllustrationPortletRenderer):
    """Illustration portlet side renderer"""

    settings_interface = IIllustrationPortletSideRendererSettings


@adapter_config(name='float-left',
                required=(IPortalContext, IPyAMSLayer, Interface, IIllustrationPortletSettings),
                provides=IPortletRenderer)
class IllustrationPortletLeftFloatRenderer(IllustrationPortletSideRenderer):
    """Left floating illustration portlet renderer"""

    label = _("Floating illustration to the left")
    css_class = 'float-right'

    weight = 20


@adapter_config(name='float-left',
                required=(IPortalContext, IPyAMSLayer, Interface,
                          IIllustrationPortletSideRendererSettings),
                provides=IPortletCSSClass)
def illustration_portlet_left_float_css_class(context, request, view, renderer_settings):
    """Left floating illustration portlet renderer CSS class"""
    return f"{renderer_settings.get_css_cols('left')} mb-3 px-0"


@adapter_config(name='float-right',
                required=(IPortalContext, IPyAMSLayer, Interface, IIllustrationPortletSettings),
                provides=IPortletRenderer)
class IllustrationPortletRightFloatRenderer(IllustrationPortletSideRenderer):
    """Right floating illustration portlet renderer"""

    label = _("Floating illustration to the right")
    css_class = 'float-right'

    weight = 30


@adapter_config(name='float-right',
                required=(IPortalContext, IPyAMSLayer, Interface,
                          IIllustrationPortletSideRendererSettings),
                provides=IPortletCSSClass)
def illustration_portlet_right_float_css_class(context, request, view, renderer_settings):
    """Right floating illustration portlet renderer CSS class"""
    return f"{renderer_settings.get_css_cols('right')} mb-3 px-0"
