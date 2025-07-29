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

"""PyAMS_content.component.video.provider module

This module defines base components which are used to handle external videos
provides by platforms like YouTube, Dailymotion, Vimeo or anything else.
"""

from persistent import Persistent
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_content.component.video import IExternalVideo, IExternalVideoProvider, IExternalVideoSettings, \
    external_video_settings
from pyams_content.component.video.interfaces import PYAMS_VIDEOS_PROVIDERS
from pyams_content.component.video.provider.interfaces import ICustomVideoSettings
from pyams_utils.adapter import adapter_config, get_adapter_weight
from pyams_utils.factory import factory_config
from pyams_utils.registry import get_utilities_for, utility_config
from pyams_utils.vocabulary import vocabulary_config

__docformat__ = 'restructuredtext'

from pyams_content import _


@vocabulary_config(name=PYAMS_VIDEOS_PROVIDERS)
class VideoProvidersVocabulary(SimpleVocabulary):
    """Video providers vocabulary"""

    interface = IExternalVideoProvider

    def __init__(self, context):
        utils = sorted(get_utilities_for(self.interface),
                       key=get_adapter_weight)
        terms = [
            SimpleTerm(name, title=getattr(util, 'label', name))
            for name, util in utils
        ]
        super().__init__(terms)


#
# Custom video provider settings
#

@factory_config(ICustomVideoSettings)
class CustomVideoSettings(Persistent):
    """Custom video provider settings"""

    integration_code = FieldProperty(ICustomVideoSettings['integration_code'])


@utility_config(name='custom',
                provides=IExternalVideoProvider)
class CustomVideoProvider:
    """Custom video provider"""

    label = _("Other provider")
    weight = 99

    settings_interface = ICustomVideoSettings


@adapter_config(required=IExternalVideo,
                provides=ICustomVideoSettings)
def custom_video_settings(context):
    """Custom video settings factory"""
    return external_video_settings(context, provider_name='custom')


@adapter_config(required=CustomVideoProvider,
                provides=IExternalVideoSettings)
def custom_video_provider_settings_factory(context):
    """Custom video provider settings factory"""
    return ICustomVideoSettings
