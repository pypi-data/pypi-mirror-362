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

"""PyAMS_content.component.video.interfaces module

This module defines interfaces which are required for support of external videos.
"""

from zope.annotation.interfaces import IAttributeAnnotatable
from zope.interface import Attribute, Interface
from zope.schema import TextLine, Choice

from pyams_content.component.paragraph import IBaseParagraph
from pyams_content.component.paragraph.schema import ParagraphRendererChoice
from pyams_i18n.schema import I18nTextField, I18nTextLineField

__docformat__ = 'restructuredtext'

from pyams_content import _


PYAMS_VIDEOS_PROVIDERS = 'pyams_content.video.providers'


class IExternalVideoSettings(Interface):
    """External video settings"""

    video_id = Attribute("Video ID")


class IExternalVideoProvider(Interface):
    """External video provider"""

    label = Attribute("Video provider label")
    weight = Attribute("Video provider weight (used for ordering)")
    settings_interface = Attribute("Video provider settings interface")


class IExternalVideo(IAttributeAnnotatable):
    """Base interface for external video integration"""

    author = TextLine(title=_("Author"),
                      description=_("Name of video's author"),
                      required=False)

    description = I18nTextField(title=_("Associated text"),
                                description=_("Video description displayed by front-office template"),
                                required=False)

    provider_name = Choice(title=_("Video provider"),
                           description=_("Name of external platform providing selected video"),
                           required=False,
                           vocabulary=PYAMS_VIDEOS_PROVIDERS)

    def get_provider(self):
        """Get external video provider utility"""

    settings = Attribute("Video settings")


EXTERNAL_VIDEO_PARAGRAPH_TYPE = 'video.external'
EXTERNAL_VIDEO_PARAGRAPH_NAME = _("External video")
EXTERNAL_VIDEO_PARAGRAPH_RENDERERS = 'PyAMS_content.paragraph.video.renderers'
EXTERNAL_VIDEO_PARAGRAPH_ICON_CLASS = 'fab fa-youtube'


class IExternalVideoParagraph(IExternalVideo, IBaseParagraph):
    """External video paragraph"""

    title = I18nTextLineField(title=_("Legend"),
                              required=False)

    renderer = ParagraphRendererChoice(description=_("Presentation template used for video"),
                                       renderers=EXTERNAL_VIDEO_PARAGRAPH_RENDERERS)
