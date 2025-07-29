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

"""PyAMS_content.component.frame.skin module

This module defines framed text paragraph and portlet renderers settings.
"""

from persistent import Persistent
from zope.container.contained import Contained
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.frame import IFrameParagraph
from pyams_content.component.frame.skin.interfaces import IFrameDefaultRendererSettings, \
    IFrameLateralRendererSettings
from pyams_content.component.illustration import IIllustration
from pyams_content.feature.renderer import DefaultContentRenderer, IContentRenderer
from pyams_content.reference.pictogram import IPictogramTable
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import DEFAULT_RENDERER_NAME
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_utils.factory import factory_config
from pyams_utils.registry import query_utility
from pyams_utils.zodb import volatile_property

__docformat__ = 'restructuredtext'

from pyams_content import _


#
# Default frame paragraph renderer
#

@factory_config(IFrameDefaultRendererSettings)
class FrameDefaultRendererSettings(Persistent, Contained):
    """Frame paragraph renderer settings"""

    status = FieldProperty(IFrameDefaultRendererSettings['status'])
    _pictogram_name = FieldProperty(IFrameDefaultRendererSettings['pictogram_name'])

    @property
    def pictogram_name(self):
        return self._pictogram_name

    @pictogram_name.setter
    def pictogram_name(self, value):
        if value != self._pictogram_name:
            self._pictogram_name = value
            del self.pictogram

    @volatile_property
    def pictogram(self):
        table = query_utility(IPictogramTable)
        if table is not None:
            return table.get(self._pictogram_name)


@adapter_config(name=DEFAULT_RENDERER_NAME,
                required=(IFrameParagraph, IPyAMSLayer),
                provides=IContentRenderer)
@template_config(template='templates/frame-default.pt',
                 layer=IPyAMSLayer)
class FrameParagraphDefaultRenderer(DefaultContentRenderer):
    """Frame paragraph default renderer"""

    label = _("Full width frame (default)")

    settings_interface = IFrameDefaultRendererSettings

    illustration = None
    illustration_renderer = None

    def update(self):
        super().update()
        illustration = IIllustration(self.context)
        if illustration.has_data():
            self.illustration = illustration
            self.illustration_renderer = illustration.get_renderer(self.request)
            self.illustration_renderer.update()


#
# Lateral frame paragraph renderers
#

@factory_config(IFrameLateralRendererSettings)
class FrameLateralRendererSettings(FrameDefaultRendererSettings):
    """Frame paragraph lateral renderer settings"""

    position = FieldProperty(IFrameLateralRendererSettings['position'])
    width = FieldProperty(IFrameLateralRendererSettings['width'])

    def get_css_class(self):
        selection = self.width
        return ' '.join((
            f'col-{selection.cols}' if device == 'xs' else f'col-{device}-{selection.cols}'
            for device, selection in selection.items()
        ))


@adapter_config(name='lateral',
                required=(IFrameParagraph, IPyAMSLayer),
                provides=IContentRenderer)
@template_config(template='templates/frame-lateral.pt',
                 layer=IPyAMSLayer)
class FrameParagraphLateralRenderer(FrameParagraphDefaultRenderer):
    """Frame paragraph lateral renderer"""

    label = _("Floating lateral frame")

    settings_interface = IFrameLateralRendererSettings
