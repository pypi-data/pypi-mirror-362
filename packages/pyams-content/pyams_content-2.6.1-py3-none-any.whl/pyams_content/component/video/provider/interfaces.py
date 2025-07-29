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

"""PyAMS_content.component.video.provider.interfaces module

This module defines settings interfaces of external videos providers.
"""

from zope.schema import Bool, Choice, Int, Text, TextLine

from pyams_content.component.video.interfaces import IExternalVideoSettings
from pyams_utils.schema import ColorField

__docformat__ = 'restructuredtext'

from pyams_content import _


class ICustomVideoSettings(IExternalVideoSettings):
    """Custom external video provider settings"""

    integration_code = Text(title=_("Integration code"),
                            description=_("Please select integration code provided by your video provider, "
                                          "and paste it here"),
                            required=True)


class IYoutubeVideoSettings(IExternalVideoSettings):
    """Youtube video provider settings"""

    video_id = TextLine(title=_("Video ID"),
                        description=_("To get video ID, just use the 'Share' button in Youtube platform and "
                                      "copy/paste the given URL here"),
                        required=True)

    start_at = TextLine(title=_("Start at"),
                        description=_("Position at which to start video, in 'seconds' or 'minutes:seconds' format"),
                        required=False,
                        default='0:00')

    stop_at = TextLine(title=_("Stop at"),
                       description=_("Position at which to stop video, in 'seconds' or 'minutes:seconds' format"),
                       required=False)

    autoplay = Bool(title=_("Auto play?"),
                    description=_("If 'yes', video is started automatically on page load"),
                    required=True,
                    default=False)

    loop = Bool(title=_("Loop playback?"),
                description=_("If 'yes', video is played indefinitely"),
                required=True,
                default=False)

    show_commands = Bool(title=_("Show commands?"),
                         description=_("Show video player commands"),
                         required=True,
                         default=True)

    hide_branding = Bool(title=_("Hide branding?"),
                         description=_("If 'no', Youtube branding will be displayed"),
                         required=True,
                         default=True)

    show_related = Bool(title=_("Show related videos?"),
                        description=_("Show related videos when video end"),
                        required=True,
                        default=False)

    allow_fullscreen = Bool(title=_("Allow full screen?"),
                            description=_("If 'yes', video can be displayed in full screen"),
                            required=True,
                            default=True)

    disable_keyboard = Bool(title=_("Disable keyboard?"),
                            description=_("If 'yes', video player can't be controlled via keyboard shortcuts"),
                            required=True,
                            default=False)

    width = Int(title=_("Video width"),
                description=_("Initial video frame width; mandatory for old browsers but may be overridden by "
                              "presentation skin"),
                required=True,
                min=200,
                default=720)

    height = Int(title=_("Video height"),
                 description=_("Initial video frame height; mandatory for old browsers but may be overridden by "
                               "presentation skin"),
                 required=True,
                 min=200,
                 default=405)


class IDailymotionVideoSettings(IExternalVideoSettings):
    """Dailymotion video provider settings"""

    video_id = TextLine(title=_("Video ID"),
                        description=_("To get video ID, just use the 'Share' button in Dailymotion platform, "
                                      "click on \"Copy link\" and paste the given URL here"),
                        required=True)

    start_at = TextLine(title=_("Start at"),
                        description=_("Position at which to start video, in 'seconds' or 'minutes:seconds' format"),
                        required=False,
                        default='0:00')

    autoplay = Bool(title=_("Auto play?"),
                    description=_("If 'yes', video is started automatically on page load"),
                    required=True,
                    default=False)

    show_info = Bool(title=_("Show video info?"),
                     description=_("If 'no', video title and information won't be displayed"),
                     required=True,
                     default=True)

    show_commands = Bool(title=_("Show commands?"),
                         description=_("Show video player commands"),
                         required=True,
                         default=True)

    ui_theme = Choice(title=_("UI theme"),
                      description=_("Default base color theme"),
                      values=('dark', 'light'),
                      default='dark')

    show_branding = Bool(title=_("Show branding?"),
                         description=_("If 'yes', Dailymotion branding will be displayed"),
                         required=True,
                         default=False)

    show_endscreen = Bool(title=_("Show end screen?"),
                          description=_("Show end screen when video end"),
                          required=True,
                          default=False)

    allow_fullscreen = Bool(title=_("Allow full screen?"),
                            description=_("If 'yes', video can be displayed in full screen"),
                            required=True,
                            default=True)

    allow_sharing = Bool(title=_("Allow sharing?"),
                         description=_("If 'no', video sharing will be disabled"),
                         required=True,
                         default=True)

    width = Int(title=_("Video width"),
                description=_("Initial video frame width; mandatory for old browsers but may be overridden by "
                              "presentation skin"),
                required=True,
                min=200,
                default=720)

    height = Int(title=_("Video height"),
                 description=_("Initial video frame height; mandatory for old browsers but may be overridden by "
                               "presentation skin"),
                 required=True,
                 min=200,
                 default=405)


class IVimeoVideoSettings(IExternalVideoSettings):
    """Vimeo video provider settings"""

    video_id = TextLine(title=_("Video ID"),
                        description=_("To get video ID, just use the 'Share' button in Vimeo platform, "
                                      "click on \"Link\" entry and copy/paste the given URL here"),
                        required=True)

    show_title = Bool(title=_("Show title?"),
                      description=_("If 'no', video title won't be displayed"),
                      required=True,
                      default=True)

    show_signature = Bool(title=_("Show signature?"),
                          description=_("If 'no', video's author signature won't be displayed"),
                          required=True,
                          default=True)

    color = ColorField(title=_("Infos color"),
                       description=_("Color used for title and signature"),
                       required=True,
                       default='ffffff')

    autoplay = Bool(title=_("Auto play?"),
                    description=_("If 'yes', video is started automatically on page load"),
                    required=True,
                    default=False)

    loop = Bool(title=_("Loop playback?"),
                description=_("If 'yes', video is played indefinitely"),
                required=True,
                default=False)

    allow_fullscreen = Bool(title=_("Allow full screen?"),
                            description=_("If 'yes', video can be displayed in full screen"),
                            required=True,
                            default=True)

    width = Int(title=_("Video width"),
                description=_("Initial video frame width; mandatory for old browsers but may be overridden by "
                              "presentation skin"),
                required=True,
                min=200,
                default=720)

    height = Int(title=_("Video height"),
                 description=_("Initial video frame height; mandatory for old browsers but may be overridden by "
                               "presentation skin"),
                 required=True,
                 min=200,
                 default=405)
