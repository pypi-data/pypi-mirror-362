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

"""PyAMS_content.component.video.skin.provider.youtube module

This module defines YouTube external video renderer.
"""

from pyams_content.component.video.provider.interfaces import IYoutubeVideoSettings
from pyams_content.component.video.skin import IExternalVideoRenderer
from pyams_content.component.video.skin.provider import BaseExternalVideoRenderer, get_playlist_id, time_to_seconds
from pyams_layer.interfaces import IPyAMSLayer
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config

__docformat__ = 'restructuredtext'


YOUTUBE_PARAMS = (
    ('start_at', 'start', time_to_seconds),
    ('stop_at', 'end', time_to_seconds),
    ('autoplay', 'autoplay', int),
    ('loop', 'loop', int),
    (None, 'playlist', get_playlist_id),
    ('show_commands', 'controls', int),
    ('hide_branding', 'modestbranding', int),
    ('show_related', 'rel', int),
    ('allow_fullscreen', 'fs', int),
    ('disable_keyboard', 'disablekb', int)
)


@adapter_config(required=(IYoutubeVideoSettings, IPyAMSLayer),
                provides=IExternalVideoRenderer)
@template_config(template='templates/youtube-render.pt', layer=IPyAMSLayer)
class YoutubeVideoRenderer(BaseExternalVideoRenderer):
    """Youtube video renderer"""

    params = YOUTUBE_PARAMS
