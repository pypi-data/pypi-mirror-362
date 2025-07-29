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

"""PyAMS_content.component.illustration.skin.paragraph module

This module provides illustration paragraph rendering components.
"""

from persistent import Persistent
from zope.container.contained import Contained
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.illustration.interfaces import IIllustrationParagraph
from pyams_content.component.illustration.skin.interfaces import \
    IIllustrationDefaultRendererSettings
from pyams_content.feature.renderer import DefaultContentRenderer, IContentRenderer
from pyams_portal.interfaces import DEFAULT_RENDERER_NAME
from pyams_layer.interfaces import IPyAMSLayer
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_utils.factory import factory_config


__docformat__ = 'restructuredtext'

from pyams_content import _


@factory_config(IIllustrationDefaultRendererSettings)
class IllustrationParagraphDefaultRendererSettings(Persistent, Contained):
    """Illustration paragraph default renderer settings"""

    thumb_selection = FieldProperty(IIllustrationDefaultRendererSettings['thumb_selection'])


@adapter_config(name=DEFAULT_RENDERER_NAME,
                required=(IIllustrationParagraph, IPyAMSLayer),
                provides=IContentRenderer)
@template_config(template='templates/paragraph-default.pt', layer=IPyAMSLayer)
class IllustrationParagraphDefaultRenderer(DefaultContentRenderer):
    """Illustration paragraph default renderer"""

    label = _("Illustration (default)")

    settings_interface = IIllustrationDefaultRendererSettings
