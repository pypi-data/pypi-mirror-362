#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.component.paragraph module

Paragraphs are components which are used to build the *content* of a given web page;
these components can be very simple elements like rich HTML text, but can also include
specialized components like verbatims, contact cards, framed text, illustrations, images
galleries, videos or any other kind of content that you can imagine...
"""

__docformat__ = 'restructuredtext'

from persistent import Persistent
from pyramid.events import subscriber
from zope.container.contained import Contained
from zope.interface import implementer
from zope.lifecycleevent import IObjectAddedEvent, IObjectModifiedEvent, IObjectRemovedEvent, \
    ObjectModifiedEvent
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_content.component.paragraph.interfaces import CONTENT_PARAGRAPHS_VOCABULARY, \
    IBaseParagraph, IParagraphContainer, IParagraphContainerTarget, IParagraphTitle, \
    PARAGRAPH_FACTORIES_VOCABULARY
from pyams_content.feature.preview.interfaces import IPreviewTarget
from pyams_content.feature.renderer import RenderedContentMixin
from pyams_content.interfaces import MANAGE_CONTENT_PERMISSION, PUBLISH_CONTENT_PERMISSION
from pyams_i18n.interfaces import II18n
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.factory import get_all_factories
from pyams_utils.html import html_to_text
from pyams_utils.registry import get_pyramid_registry
from pyams_utils.request import check_request
from pyams_utils.traversing import get_parent
from pyams_utils.vocabulary import vocabulary_config
from pyams_zmi.interfaces import IObjectHint, IObjectIcon, IObjectLabel


@vocabulary_config(name=PARAGRAPH_FACTORIES_VOCABULARY)
class ParagraphFactoriesVocabulary(SimpleVocabulary):
    """Paragraph factories vocabulary"""

    def __init__(self, context=None):  # pylint: disable=unused-argument
        request = check_request()
        translate = request.localizer.translate
        terms = sorted([
            SimpleTerm(name, title=translate(factory.factory_label))
            for name, factory in get_all_factories(IBaseParagraph)
        ], key=lambda x: x.title)
        super().__init__(terms)


@vocabulary_config(name=CONTENT_PARAGRAPHS_VOCABULARY)
class ContentParagraphsVocabulary(SimpleVocabulary):
    """Content paragraphs vocabulary"""

    def __init__(self, context):

        def get_title(paragraph):
            """Paragraph title getter"""
            adapter = request.registry.queryMultiAdapter((paragraph, request),
                                                         IParagraphTitle)
            if adapter is not None:
                return html_to_text(adapter)
            return II18n(paragraph).query_attribute('title', request=request) or \
                BaseParagraph.empty_title

        request = check_request()
        if not IParagraphContainerTarget.providedBy(context):
            context = get_parent(context, IParagraphContainerTarget)
        if context is not None:
            terms = [
                SimpleTerm(para.__name__,
                           title=f'{index+1}: {get_title(para)}')
                for index, para in enumerate(IParagraphContainer(context).values())
            ]
        else:
            terms = []
        super().__init__(terms)


@implementer(IBaseParagraph, IPreviewTarget)
class BaseParagraph(RenderedContentMixin, Persistent, Contained):
    """Base paragraph persistent class"""

    factory_name = None
    factory_label = None
    factory_intf = None
    secondary = False

    icon_class = None

    @property
    def icon_hint(self):
        """Icon hint getter"""
        request = check_request()
        return request.localizer.translate(self.factory_label)

    visible = FieldProperty(IBaseParagraph['visible'])
    anchor = FieldProperty(IBaseParagraph['anchor'])
    locked = FieldProperty(IBaseParagraph['locked'])
    title = FieldProperty(IBaseParagraph['title'])

    empty_title = ' -' * 8


@adapter_config(required=IBaseParagraph,
                provides=IObjectHint)
def paragraph_hint(context):
    """Paragraph hint getter"""
    return context.icon_hint


@adapter_config(required=IBaseParagraph,
                provides=IObjectIcon)
def paragraph_icon(context):
    """Paragraph icon getter"""
    return context.icon_class


@adapter_config(required=IBaseParagraph,
                provides=IObjectLabel)
def paragraph_label(context):
    """Paragraph label getter"""
    request = check_request()
    title = II18n(context).query_attribute('title', request=request)
    return title or BaseParagraph.empty_title


@adapter_config(required=IBaseParagraph,
                provides=IViewContextPermissionChecker)
@adapter_config(required=IParagraphContainer,
                provides=IViewContextPermissionChecker)
class ParagraphPermissionChecker(ContextAdapter):
    """Paragraph permission checker"""

    @property
    def edit_permission(self):
        """Edit permission checker"""
        parent = get_parent(self.context, IParagraphContainerTarget,
                            condition=lambda x: not IBaseParagraph.providedBy(x))
        if parent is not None:
            return IViewContextPermissionChecker(parent).edit_permission
        return None


@adapter_config(name='delete',
                required=IBaseParagraph,
                provides=IViewContextPermissionChecker)
class ParagraphDeletePermissionChecker(ParagraphPermissionChecker):
    """Paragraph delete permission checker"""

    @property
    def edit_permission(self):
        """Edit permission checker"""
        permission = super().edit_permission
        if self.context.locked and (permission == MANAGE_CONTENT_PERMISSION):
            return PUBLISH_CONTENT_PERMISSION
        return permission


@subscriber(IObjectAddedEvent, context_selector=IBaseParagraph)
@subscriber(IObjectModifiedEvent, context_selector=IBaseParagraph)
@subscriber(IObjectRemovedEvent, context_selector=IBaseParagraph)
def handle_paragraph_event(event):
    """Handle paragraph event"""
    content = get_parent(event.object, IParagraphContainerTarget,
                         condition=lambda x: not IBaseParagraph.providedBy(x))
    if content is not None:
        get_pyramid_registry().notify(ObjectModifiedEvent(content))
