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

"""PyAMS_content.component.video.skin.provider.dailymotion module

This module defines Dailymotion video renderer.
"""

from pyams_content.component.video.provider.interfaces import IDailymotionVideoSettings
from pyams_content.component.video.skin import IExternalVideoRenderer
from pyams_content.component.video.skin.provider import BaseExternalVideoRenderer, time_to_seconds
from pyams_layer.interfaces import IPyAMSLayer
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config

__docformat__ = 'restructuredtext'


DAILYMOTION_PARAMS = (
    ('start_at', 'start', time_to_seconds),
    ('autoplay', 'autoplay', int),
    ('show_info', 'ui-start-screen-info', int),
    ('show_commands', 'controls', int),
    ('ui_theme', 'ui-theme', str),
    ('show_branding', 'ui-logo', int),
    ('show_endscreen', 'endscreen-enable', int),
    ('allow_sharing', 'sharing-enable', int)
)


@adapter_config(required=(IDailymotionVideoSettings, IPyAMSLayer),
                provides=IExternalVideoRenderer)
@template_config(template='templates/dailymotion-render.pt', layer=IPyAMSLayer)
class DailymotionVideoRenderer(BaseExternalVideoRenderer):
    """Dailymotion video renderer"""

    params = DAILYMOTION_PARAMS
