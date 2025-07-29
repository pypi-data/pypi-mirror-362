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

"""PyAMS_content.component.video.skin.provider module

This module defines base external videos renderers class.
"""

__docformat__ = 'restructuredtext'

from urllib.parse import urlencode

from pyams_content.component.video.provider import ICustomVideoSettings
from pyams_content.component.video.skin import IExternalVideoRenderer
from pyams_layer.interfaces import IPyAMSLayer
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_viewlet.viewlet import BaseContentProvider


def time_to_seconds(value):
    """Convert minutes:seconds value to seconds"""
    if value and (':' in value):
        minutes, seconds = value.split(':', 1)
        return str(int(minutes) * 60 + int(seconds))
    return value or ''


def get_playlist_id(settings):
    """Include playlist ID if loop is required"""
    if settings.loop:
        return settings.video_id
    return None


class BaseExternalVideoRenderer(BaseContentProvider):
    """Base external video renderer"""

    params = ()

    def get_url_params(self):
        settings = self.context
        params = {}
        for attr, param, handler in self.params:
            if attr is None:
                result = handler(settings)
            else:
                result = handler(getattr(settings, attr))
            if result is not None:
                params[param] = result
        return urlencode(params)


@adapter_config(required=(ICustomVideoSettings, IPyAMSLayer),
                provides=IExternalVideoRenderer)
@template_config(template='templates/custom-render.pt', layer=IPyAMSLayer)
class CustomVideoRenderer(BaseExternalVideoRenderer):
    """Custom video renderer"""
