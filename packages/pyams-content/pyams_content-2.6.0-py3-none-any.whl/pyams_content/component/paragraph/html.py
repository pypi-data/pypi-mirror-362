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

"""PyAMS_content.component.paragraph.html module

This module defines raw and rich text HTML paragraphs.
"""

__docformat__ = 'restructuredtext'

from pyramid.events import subscriber
from zope.interface import implementer
from zope.lifecycleevent import IObjectAddedEvent, IObjectModifiedEvent
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.extfile.interfaces import IExtFileContainerTarget
from pyams_content.component.illustration import IIllustrationTarget
from pyams_content.component.links.html import check_content_links
from pyams_content.component.links.interfaces import ILinkContainerTarget
from pyams_content.component.paragraph import BaseParagraph
from pyams_content.component.paragraph.interfaces import IBaseParagraph
from pyams_content.component.paragraph.interfaces.html import HTML_PARAGRAPH_ICON_CLASS, \
    HTML_PARAGRAPH_NAME, HTML_PARAGRAPH_RENDERERS, HTML_PARAGRAPH_TYPE, IHTMLParagraph, \
    IRawParagraph, RAW_PARAGRAPH_ICON_CLASS, RAW_PARAGRAPH_NAME, RAW_PARAGRAPH_RENDERERS, \
    RAW_PARAGRAPH_TYPE
from pyams_content.feature.renderer import RenderersVocabulary
from pyams_utils.factory import factory_config
from pyams_utils.vocabulary import vocabulary_config


#
# Raw HTML code paragraph
#

@factory_config(IRawParagraph)
@factory_config(IBaseParagraph, name=RAW_PARAGRAPH_TYPE)
class RawParagraph(BaseParagraph):
    """Raw paragraph persistent class"""

    factory_name = RAW_PARAGRAPH_TYPE
    factory_label = RAW_PARAGRAPH_NAME
    factory_intf = IRawParagraph

    icon_class = RAW_PARAGRAPH_ICON_CLASS
    secondary = True

    body = FieldProperty(IRawParagraph['body'])
    renderer = FieldProperty(IRawParagraph['renderer'])


@vocabulary_config(name=RAW_PARAGRAPH_RENDERERS)
class RawParagraphRenderersVocabulary(RenderersVocabulary):
    """Raw paragraph renderers vocabulary"""

    content_interface = IRawParagraph


#
# Rich text HTML paragraph
#

@factory_config(IHTMLParagraph)
@factory_config(IBaseParagraph, name=HTML_PARAGRAPH_TYPE)
@implementer(IIllustrationTarget, IExtFileContainerTarget, ILinkContainerTarget)
class HTMLParagraph(BaseParagraph):
    """HTML paragraph persistent class"""

    factory_name = HTML_PARAGRAPH_TYPE
    factory_label = HTML_PARAGRAPH_NAME
    factory_intf = IHTMLParagraph

    icon_class = HTML_PARAGRAPH_ICON_CLASS

    body = FieldProperty(IHTMLParagraph['body'])
    renderer = FieldProperty(IHTMLParagraph['renderer'])


@subscriber(IObjectAddedEvent, context_selector=IHTMLParagraph)
@subscriber(IObjectModifiedEvent, context_selector=IHTMLParagraph)
def handle_html_paragraph_links(event):
    """Handle HTML paragraph links"""
    paragraph = event.object
    for lang, body in (paragraph.body or {}).items():
        check_content_links(paragraph, body, lang, notify=False)


@vocabulary_config(name=HTML_PARAGRAPH_RENDERERS)
class HTMLParagraphRenderersVocabulary(RenderersVocabulary):
    """HTML paragraph renderers vocabulary"""

    content_interface = IHTMLParagraph
