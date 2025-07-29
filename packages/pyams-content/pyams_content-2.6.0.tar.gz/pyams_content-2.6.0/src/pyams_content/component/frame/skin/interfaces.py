#
# Copyright (c) 2015-2024 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.component.frame.skin.interfaces module

This module defines framed text pararaph renderers settings interfaces.
"""

from collections import OrderedDict
from enum import Enum

from zope.interface import Attribute, Interface
from zope.schema import Choice
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_content.feature.renderer import IRendererSettings
from pyams_content.reference.pictogram.interfaces import SELECTED_PICTOGRAM_VOCABULARY
from pyams_skin.interfaces import BOOTSTRAP_STATUS_VOCABULARY
from pyams_skin.schema import BootstrapThumbnailsSelectionField

__docformat__ = 'restructuredtext'

from pyams_content import _


class FRAME_POSITION(Enum):
    """Frame positions"""
    LEFT = 'left'
    RIGHT = 'right'


FRAME_POSITION_LABELS = OrderedDict((
    (FRAME_POSITION.LEFT.value, _("Left")),
    (FRAME_POSITION.RIGHT.value, _("Right"))
))

FRAME_POSITION_VOCABULARY = SimpleVocabulary([
    SimpleTerm(v, title=t)
    for v, t in FRAME_POSITION_LABELS.items()
])


class IFrameBaseRendererSettings(Interface):
    """Frame base renderer settings interface"""

    status = Choice(title=_("Frame alert status"),
                    description=_("Bootstrap alert status defines rendering color"),
                    vocabulary=BOOTSTRAP_STATUS_VOCABULARY,
                    required=False)

    pictogram_name = Choice(title=_("Pictogram"),
                            description=_("Name of the pictogram associated with this frame paragraph"),
                            required=False,
                            vocabulary=SELECTED_PICTOGRAM_VOCABULARY)

    pictogram = Attribute("Selected pictogram instance")


class IFrameBaseLateralRendererSettings(IFrameBaseRendererSettings):
    """Frame paragraph lateral renderer settings interface"""

    position = Choice(title=_("Frame position"),
                      description=_("Frame position relatively to it's parent paragraph"),
                      required=True,
                      vocabulary=FRAME_POSITION_VOCABULARY,
                      default=FRAME_POSITION.RIGHT.value)

    width = BootstrapThumbnailsSelectionField(title=_("Devices width"),
                                              description=_("Select frame size for all available devices"),
                                              required=True,
                                              change_selection=False,
                                              default_width={
                                                  'xs': 12,
                                                  'sm': 12,
                                                  'md': 6,
                                                  'lg': 5,
                                                  'xl': 4
                                              })

    def get_css_class(self):
        """CSS class getter"""


class IFrameDefaultRendererSettings(IRendererSettings, IFrameBaseRendererSettings):
    """Frame default renderer settings interface"""


class IFrameLateralRendererSettings(IRendererSettings, IFrameBaseLateralRendererSettings):
    """Frame lateral renderer settings interface"""
