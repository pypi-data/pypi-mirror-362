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

"""PyAMS_content.component.video.provider.youtube module

This is the YouTube external videos provider module.
"""

import re

from persistent import Persistent
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.video import IExternalVideo, IExternalVideoSettings, external_video_settings
from pyams_content.component.video.interfaces import IExternalVideoProvider
from pyams_content.component.video.provider.interfaces import IYoutubeVideoSettings
from pyams_utils.adapter import adapter_config
from pyams_utils.factory import factory_config
from pyams_utils.registry import utility_config


__docformat__ = 'restructuredtext'

from pyams_content import _


YOUTUBE_BASE_URL = re.compile(r'https://youtu.be/(.*)')
YOUTUBE_EXTENDED_URL = re.compile(r'https://(?:www\.)?youtube.com/watch\?v=(.*)')


@factory_config(IYoutubeVideoSettings)
class YoutubeVideoSettings(Persistent):
    """Youtube video settings"""

    _video_id = FieldProperty(IYoutubeVideoSettings['video_id'])
    start_at = FieldProperty(IYoutubeVideoSettings['start_at'])
    stop_at = FieldProperty(IYoutubeVideoSettings['stop_at'])
    autoplay = FieldProperty(IYoutubeVideoSettings['autoplay'])
    loop = FieldProperty(IYoutubeVideoSettings['loop'])
    show_commands = FieldProperty(IYoutubeVideoSettings['show_commands'])
    hide_branding = FieldProperty(IYoutubeVideoSettings['hide_branding'])
    show_related = FieldProperty(IYoutubeVideoSettings['show_related'])
    allow_fullscreen = FieldProperty(IYoutubeVideoSettings['allow_fullscreen'])
    disable_keyboard = FieldProperty(IYoutubeVideoSettings['disable_keyboard'])
    width = FieldProperty(IYoutubeVideoSettings['width'])
    height = FieldProperty(IYoutubeVideoSettings['height'])

    @property
    def video_id(self):
        return self._video_id

    @video_id.setter
    def video_id(self, value):
        if value:
            match = YOUTUBE_BASE_URL.match(value) or YOUTUBE_EXTENDED_URL.match(value)
            if match:
                value = match.groups()[0]
        self._video_id = value


@utility_config(name='youtube',
                provides=IExternalVideoProvider)
class YoutubeVideoProvider:
    """YouTube video provider"""

    label = _("YouTube")
    weight = 10

    settings_interface = IYoutubeVideoSettings


@adapter_config(required=IExternalVideo,
                provides=IYoutubeVideoSettings)
def youtube_video_settings(context):
    """YouTube video settings factory"""
    return external_video_settings(context, provider_name='youtube')


@adapter_config(required=YoutubeVideoProvider,
                provides=IExternalVideoSettings)
def youtube_video_provider_settings_factory(context):
    """YouTube video provider settings factory"""
    return IYoutubeVideoSettings
