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

"""PyAMS_content.component.video.skin.provider.vimeo module

This module defines Vimeo external video renderer.
"""

from pyams_content.component.video.provider.interfaces import IVimeoVideoSettings
from pyams_content.component.video.skin import IExternalVideoRenderer
from pyams_content.component.video.skin.provider import BaseExternalVideoRenderer
from pyams_layer.interfaces import IPyAMSLayer
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config

__docformat__ = 'restructuredtext'


VIMEO_PARAMS = (
    ('show_title', 'title', int),
    ('show_signature', 'byline', int),
    ('color', 'color', str),
    ('autoplay', 'autoplay', int),
    ('loop', 'loop', int)
)


@adapter_config(required=(IVimeoVideoSettings, IPyAMSLayer),
                provides=IExternalVideoRenderer)
@template_config(template='templates/vimeo-render.pt', layer=IPyAMSLayer)
class VimeoVideoRenderer(BaseExternalVideoRenderer):
    """Vimeo video renderer"""

    params = VIMEO_PARAMS
