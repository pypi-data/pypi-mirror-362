#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.component.gallery module

This module defines persistent components and adapters used to handle medias
galleries.
"""

from persistent import Persistent
from zope.container.contained import Contained
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.video.interfaces import IExternalVideo, IExternalVideoSettings, IExternalVideoProvider
from pyams_utils.adapter import adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.registry import get_utility, query_utility


@factory_config(IExternalVideo)
class ExternalVideo(Persistent, Contained):
    """External video persistent class"""

    author = FieldProperty(IExternalVideo['author'])
    description = FieldProperty(IExternalVideo['description'])
    provider_name = FieldProperty(IExternalVideo['provider_name'])

    def get_provider(self):
        return query_utility(IExternalVideoProvider, name=self.provider_name or '')

    @property
    def settings(self):
        provider = self.get_provider()
        if provider is None:
            return None
        return provider.settings_interface(self)


EXTERNAL_VIDEO_SETTINGS_KEY = 'pyams_content.video::{}'


@adapter_config(required=IExternalVideo,
                provides=IExternalVideoSettings)
def external_video_settings(context, provider_name=None):
    """External video settings factory"""
    if not provider_name:
        provider_name = context.provider_name
        if not provider_name:
            return None
    provider = get_utility(IExternalVideoProvider, name=provider_name)
    settings_key = EXTERNAL_VIDEO_SETTINGS_KEY.format(provider_name.lower())
    return get_annotation_adapter(context, settings_key,
                                  factory=IExternalVideoSettings(provider))
