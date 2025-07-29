#
# Copyright (c) 2015-2022 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.component.paragraph.html.skin.interfaces module

This module defines interfaces of HTML paragraph default renderer.
"""

from zope.schema import Bool, Choice

from pyams_content.feature.renderer import IRendererSettings
from pyams_skin.interfaces import BOOTSTRAP_STATUS_VOCABULARY

__docformat__ = 'restructuredtext'

from pyams_content import _


class IHTMLParagraphRendererSettings(IRendererSettings):
    """HTML paragraph renderer settings interface"""

    xs_horizontal_padding = Choice(title=_("XS horizontal padding"),
                                   description=_("Define horizontal padding for smartphones"),
                                   required=False,
                                   values=list(range(5)))

    sm_horizontal_padding = Choice(title=_("SM horizontal padding"),
                                   description=_("Define horizontal padding for tablets"),
                                   required=False,
                                   values=list(range(5)))

    md_horizontal_padding = Choice(title=_("MD horizontal padding"),
                                   description=_("Define horizontal padding for medium screens"),
                                   required=False,
                                   values=list(range(5)))

    lg_horizontal_padding = Choice(title=_("LG horizontal padding"),
                                   description=_("Define horizontal padding for large screens"),
                                   required=False,
                                   values=list(range(5)))

    xl_horizontal_padding = Choice(title=_("XL horizontal padding"),
                                   description=_("Define horizontal padding for extra large "
                                                 "screens"),
                                   required=False,
                                   values=list(range(5)))

    def has_padding(self):
        """Check if any padding is defined"""

    def get_padding(self):
        """Get settings padding"""


class IHTMLParagraphAlertRendererSettings(IHTMLParagraphRendererSettings):
    """HTML paragraph alert renderer settings interface"""

    status = Choice(title=_("Alert status"),
                    description=_("Bootstrap alert status defines alert rendering color"),
                    required=True,
                    vocabulary=BOOTSTRAP_STATUS_VOCABULARY,
                    default='info')

    display_dismiss_button = Bool(title=_("Display dismiss button"),
                                  description=_("Select this option to display a dismiss button"),
                                  required=True,
                                  default=False)
