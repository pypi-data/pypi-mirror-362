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

"""PyAMS_content.component.verbatim module

This module defines verbatim paragraph.
"""

from persistent import Persistent
from pyramid.events import subscriber
from zope.container.contained import Contained
from zope.interface import implementer
from zope.lifecycleevent.interfaces import IObjectAddedEvent, IObjectModifiedEvent
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.extfile.interfaces import IExtFileContainerTarget
from pyams_content.component.illustration.interfaces import IBaseIllustrationTarget, IIllustrationTarget
from pyams_content.component.links.html import check_content_links
from pyams_content.component.links.interfaces import ILinkContainerTarget
from pyams_content.component.paragraph import BaseParagraph
from pyams_content.component.paragraph.interfaces import IBaseParagraph
from pyams_content.component.verbatim.interfaces import IVerbatimBase, IVerbatimContainer, IVerbatimInfo, \
    IVerbatimParagraph, VERBATIM_PARAGRAPH_ICON_CLASS, VERBATIM_PARAGRAPH_NAME, VERBATIM_PARAGRAPH_RENDERERS, \
    VERBATIM_PARAGRAPH_TYPE
from pyams_content.feature.renderer import RenderersVocabulary
from pyams_portal.interfaces import MANAGE_TEMPLATE_PERMISSION
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.container import BTreeOrderedContainer
from pyams_utils.factory import factory_config
from pyams_utils.vocabulary import vocabulary_config

__docformat__ = 'restructuredtext'


@implementer(IVerbatimContainer)
class VerbatimContainer(BTreeOrderedContainer):
    """Verbatim container persistent class"""

    def get_visible_items(self):
        """Get iterator over visible verbatim"""
        yield from filter(lambda x: x.visible, self.values())


class VerbatimBaseMixin:
    """Base verbatim info persistent class"""

    quote = FieldProperty(IVerbatimBase['quote'])
    author = FieldProperty(IVerbatimBase['author'])
    charge = FieldProperty(IVerbatimBase['charge'])


@factory_config(IVerbatimInfo)
@implementer(IBaseIllustrationTarget)
class VerbatimInfo(VerbatimBaseMixin, Persistent, Contained):
    """Verbatim info persistent class"""

    title = FieldProperty(IVerbatimInfo['title'])
    visible = FieldProperty(IVerbatimInfo['visible'])


@adapter_config(required=IVerbatimInfo,
                provides=IViewContextPermissionChecker)
class VerbatimPermissionChecker(ContextAdapter):
    """Verbatim permission checker"""

    edit_permission = MANAGE_TEMPLATE_PERMISSION


@factory_config(IVerbatimParagraph)
@factory_config(IBaseParagraph, name=VERBATIM_PARAGRAPH_TYPE)
@implementer(IIllustrationTarget, IExtFileContainerTarget, ILinkContainerTarget)
class VerbatimParagraph(VerbatimBaseMixin, BaseParagraph):
    """Verbatim paragraph persistent class"""

    factory_name = VERBATIM_PARAGRAPH_TYPE
    factory_label = VERBATIM_PARAGRAPH_NAME
    factory_intf = IVerbatimParagraph

    icon_class = VERBATIM_PARAGRAPH_ICON_CLASS
    secondary = True


@subscriber(IObjectAddedEvent, context_selector=IVerbatimParagraph)
@subscriber(IObjectModifiedEvent, context_selector=IVerbatimParagraph)
def handle_verbatim_paragraph_links(event):
    """Handle verbatim paragraph links"""
    paragraph = event.object
    for lang, quote in (paragraph.quote or {}).items():
        check_content_links(paragraph, quote, lang, notify=False)


@vocabulary_config(name=VERBATIM_PARAGRAPH_RENDERERS)
class VerbatimParagraphRenderersVocabulary(RenderersVocabulary):
    """Verbatim paragraph renderers vocabulary"""

    content_interface = IVerbatimParagraph
