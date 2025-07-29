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

"""PyAMS_content.component.frame module

This module defines framed text paragraph.
"""

from pyramid.events import subscriber
from zope.interface import implementer
from zope.lifecycleevent.interfaces import IObjectAddedEvent, IObjectModifiedEvent
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.extfile.interfaces import IExtFileContainerTarget
from pyams_content.component.frame.interfaces import FRAME_PARAGRAPH_ICON_CLASS, FRAME_PARAGRAPH_NAME, \
    FRAME_PARAGRAPH_RENDERERS, FRAME_PARAGRAPH_TYPE, IFrameParagraph
from pyams_content.component.illustration import IIllustrationTarget
from pyams_content.component.links.html import check_content_links
from pyams_content.component.links.interfaces import ILinkContainerTarget
from pyams_content.component.paragraph import BaseParagraph, IBaseParagraph
from pyams_content.feature.renderer import RenderersVocabulary
from pyams_utils.factory import factory_config
from pyams_utils.vocabulary import vocabulary_config

__docformat__ = 'restructuredtext'


@factory_config(IFrameParagraph)
@factory_config(IBaseParagraph, name=FRAME_PARAGRAPH_TYPE)
@implementer(IIllustrationTarget, IExtFileContainerTarget, ILinkContainerTarget)
class FrameParagraph(BaseParagraph):
    """Frame paragraph persistent class"""

    factory_name = FRAME_PARAGRAPH_TYPE
    factory_label = FRAME_PARAGRAPH_NAME
    factory_intf = IFrameParagraph

    icon_class = FRAME_PARAGRAPH_ICON_CLASS
    secondary = True

    body = FieldProperty(IFrameParagraph['body'])
    renderer = FieldProperty(IFrameParagraph['renderer'])


@subscriber(IObjectAddedEvent, context_selector=IFrameParagraph)
@subscriber(IObjectModifiedEvent, context_selector=IFrameParagraph)
def handle_html_paragraph_links(event):
    """Handle HTML paragraph links"""
    paragraph = event.object
    for lang, body in (paragraph.body or {}).items():
        check_content_links(paragraph, body, lang, notify=False)


@vocabulary_config(name=FRAME_PARAGRAPH_RENDERERS)
class FrameParagraphRenderersVocabulary(RenderersVocabulary):
    """Frame paragraph renderers vocabulary"""

    content_interface = IFrameParagraph
