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

"""PyAMS_content.component.video.provider.vimeo module

This module defines components which are used for Vimeo videos integration.
"""

import re

from persistent import Persistent
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.video import IExternalVideo, IExternalVideoSettings, external_video_settings
from pyams_content.component.video.interfaces import IExternalVideoProvider
from pyams_content.component.video.provider.interfaces import IVimeoVideoSettings
from pyams_utils.adapter import adapter_config
from pyams_utils.factory import factory_config
from pyams_utils.registry import utility_config

__docformat__ = 'restructuredtext'

from pyams_content import _


VIMEO_BASE_URL = re.compile('https://vimeo.com/(\d+)')


@factory_config(IVimeoVideoSettings)
class VimeoVideoSettings(Persistent):
    """Vimeo video settings"""

    _video_id = FieldProperty(IVimeoVideoSettings['video_id'])
    show_title = FieldProperty(IVimeoVideoSettings['show_title'])
    show_signature = FieldProperty(IVimeoVideoSettings['show_signature'])
    color = FieldProperty(IVimeoVideoSettings['color'])
    autoplay = FieldProperty(IVimeoVideoSettings['autoplay'])
    loop = FieldProperty(IVimeoVideoSettings['loop'])
    allow_fullscreen = FieldProperty(IVimeoVideoSettings['allow_fullscreen'])
    width = FieldProperty(IVimeoVideoSettings['width'])
    height = FieldProperty(IVimeoVideoSettings['height'])

    @property
    def video_id(self):
        return self._video_id

    @video_id.setter
    def video_id(self, value):
        if value:
            match = VIMEO_BASE_URL.match(value)
            if match:
                value = match.groups()[0]
        self._video_id = value


@utility_config(name='vimeo',
                provides=IExternalVideoProvider)
class VimeoVideoProvider:
    """Vimeo video provider"""

    label = _("Vimeo")
    weight = 30

    settings_interface = IVimeoVideoSettings


@adapter_config(required=IExternalVideo,
                provides=IVimeoVideoSettings)
def vimeo_video_settings(context):
    """Vimeo video settings factory"""
    return external_video_settings(context, provider_name='vimeo')


@adapter_config(required=VimeoVideoProvider,
                provides=IExternalVideoSettings)
def vimeo_video_provider_settings_factory(context):
    """Vimeo video provider settings factory"""
    return IVimeoVideoSettings
