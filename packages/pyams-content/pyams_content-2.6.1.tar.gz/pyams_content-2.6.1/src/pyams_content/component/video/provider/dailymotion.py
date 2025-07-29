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

"""PyAMS_content.component.video.provider.dailymotion module

This module defines settings used for Dailymotion videos integration.
"""

import re

from persistent import Persistent
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.video import IExternalVideo, IExternalVideoProvider, IExternalVideoSettings, \
    external_video_settings
from pyams_content.component.video.provider.interfaces import IDailymotionVideoSettings
from pyams_utils.adapter import adapter_config
from pyams_utils.factory import factory_config
from pyams_utils.registry import utility_config

__docformat__ = 'restructuredtext'

from pyams_content import _


DAILYMOTION_BASE_URL = re.compile(r'https?://(?:dai\.ly|www\.dailymotion\.com/video)/([^/]+)')


@factory_config(IDailymotionVideoSettings)
class YoutubeVideoSettings(Persistent):
    """Youtube video settings"""

    _video_id = FieldProperty(IDailymotionVideoSettings['video_id'])
    start_at = FieldProperty(IDailymotionVideoSettings['start_at'])
    autoplay = FieldProperty(IDailymotionVideoSettings['autoplay'])
    show_info = FieldProperty(IDailymotionVideoSettings['show_info'])
    show_commands = FieldProperty(IDailymotionVideoSettings['show_commands'])
    ui_theme = FieldProperty(IDailymotionVideoSettings['ui_theme'])
    show_branding = FieldProperty(IDailymotionVideoSettings['show_branding'])
    show_endscreen = FieldProperty(IDailymotionVideoSettings['show_endscreen'])
    allow_fullscreen = FieldProperty(IDailymotionVideoSettings['allow_fullscreen'])
    allow_sharing = FieldProperty(IDailymotionVideoSettings['allow_sharing'])
    width = FieldProperty(IDailymotionVideoSettings['width'])
    height = FieldProperty(IDailymotionVideoSettings['height'])

    @property
    def video_id(self):
        return self._video_id

    @video_id.setter
    def video_id(self, value):
        if value:
            match = DAILYMOTION_BASE_URL.match(value)
            if match:
                value = match.groups()[0]
        self._video_id = value


@utility_config(name='dailymotion',
                provides=IExternalVideoProvider)
class DailymotionVideoProvider:
    """Dailymotion video provider"""

    label = _("Dailymotion")
    weight = 20

    settings_interface = IDailymotionVideoSettings


@adapter_config(required=IExternalVideo,
                provides=IDailymotionVideoSettings)
def dailymotion_video_settings(context):
    """Dailymotion video settings factory"""
    return external_video_settings(context, provider_name='dailymotion')


@adapter_config(required=DailymotionVideoProvider,
                provides=IExternalVideoSettings)
def dailymotion_video_provider_settings_factory(context):
    """Dailymotion video provider settings factory"""
    return IDailymotionVideoSettings
