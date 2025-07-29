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

"""PyAMS_content.component.video.paragraph module

This module provides components which are used to handle integration of external
videos as content paragraphs.
"""

from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.paragraph import BaseParagraph, IBaseParagraph
from pyams_content.component.video import ExternalVideo
from pyams_content.component.video.interfaces import EXTERNAL_VIDEO_PARAGRAPH_ICON_CLASS, \
    EXTERNAL_VIDEO_PARAGRAPH_NAME, EXTERNAL_VIDEO_PARAGRAPH_RENDERERS, EXTERNAL_VIDEO_PARAGRAPH_TYPE, \
    IExternalVideoParagraph
from pyams_content.feature.renderer import RenderersVocabulary
from pyams_utils.factory import factory_config
from pyams_utils.vocabulary import vocabulary_config

__docformat__ = 'restructuredtext'


@factory_config(IExternalVideoParagraph)
@factory_config(IBaseParagraph, name=EXTERNAL_VIDEO_PARAGRAPH_TYPE)
class ExternalVideoParagraph(ExternalVideo, BaseParagraph):
    """External video paragraph"""

    factory_name = EXTERNAL_VIDEO_PARAGRAPH_TYPE
    factory_label = EXTERNAL_VIDEO_PARAGRAPH_NAME
    factory_intf = IExternalVideoParagraph

    icon_class = EXTERNAL_VIDEO_PARAGRAPH_ICON_CLASS

    renderer = FieldProperty(IExternalVideoParagraph['renderer'])


@vocabulary_config(name=EXTERNAL_VIDEO_PARAGRAPH_RENDERERS)
class ExternalVideoParagraphRenderersVocabulary(RenderersVocabulary):
    """External video paragraph renderers vocabulary"""

    content_interface = IExternalVideoParagraph
