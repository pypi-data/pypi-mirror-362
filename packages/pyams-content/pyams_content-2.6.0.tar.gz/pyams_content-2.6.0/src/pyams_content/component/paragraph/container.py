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

"""PyAMS_content.component.paragraph.container module

This module provides paragraphs containers classes and adapters.
"""

from ZODB.interfaces import IBroken
from pyramid.events import subscriber
from zope.copy import copy
from zope.lifecycleevent import IObjectAddedEvent
from zope.location.interfaces import ISublocations
from zope.traversing.interfaces import ITraversable

from pyams_content.component.paragraph import IParagraphContainerTarget
from pyams_content.component.paragraph.interfaces import IBaseParagraph, IParagraphContainer, \
    IParagraphFactorySettings, IParagraphFactorySettingsTarget, PARAGRAPH_CONTAINER_KEY
from pyams_content.shared.common import IWfSharedContent
from pyams_content.shared.common.interfaces.types import IWfTypedSharedContent
from pyams_utils.adapter import ContextAdapter, adapter_config, get_annotation_adapter
from pyams_utils.container import BTreeOrderedContainer
from pyams_utils.factory import factory_config, get_object_factory
from pyams_utils.traversing import get_parent
from pyams_workflow.interfaces import IWorkflowState

__docformat__ = 'restructuredtext'


@factory_config(IParagraphContainer)
class ParagraphContainer(BTreeOrderedContainer):
    """Paragraph container persistent class"""

    def get_paragraphs(self, factories):
        """Get paragraphs matching given factories"""
        if not isinstance(factories, (list, tuple, set)):
            factories = {factories}
        yield from (
            paragraph
            for paragraph in self.values()
            if paragraph.factory_name in (factories or ())
        )

    def get_visible_paragraphs(self, names=None, anchors_only=False, exclude_anchors=False,
                               factories=None, excluded_factories=None, limit=None):
        """Visible paragraphs getter"""
        count = 0
        if names:
            for name in names:
                paragraph = self.get(name)
                if (paragraph is not None) and \
                        (not IBroken.providedBy(paragraph)) and \
                        paragraph.visible:
                    yield paragraph
                    count += 1
                    if limit and (count == limit):
                        return
        else:
            for paragraph in self.values():
                if IBroken.providedBy(paragraph) or not paragraph.visible:
                    continue
                if anchors_only and not paragraph.anchor:
                    continue
                if exclude_anchors and paragraph.anchor:
                    continue
                if factories and (paragraph.factory_name not in factories):
                    continue
                if excluded_factories and (paragraph.factory_name in excluded_factories):
                    continue
                yield paragraph
                count += 1
                if limit and (count == limit):
                    return


@adapter_config(required=IParagraphContainerTarget,
                provides=IParagraphContainer)
def paragraph_container_factory(target):
    """Paragraphs container factory"""
    return get_annotation_adapter(target, PARAGRAPH_CONTAINER_KEY, IParagraphContainer,
                                  name='++paras++')


@adapter_config(name='paras',
                required=IParagraphContainerTarget,
                provides=ITraversable)
class ParagraphContainerNamespace(ContextAdapter):
    """++paras++ namespace adapter"""

    def traverse(self, name, furtherpath=None):
        """Paragraphs container traverser"""
        target = IParagraphContainer(self.context)
        if name:
            target = target.get(name)
        return target


@adapter_config(name='paras',
                required=IParagraphContainerTarget,
                provides=ISublocations)
class ParagraphContainerSublocations(ContextAdapter):
    """Paragraphs container sub-locations"""

    def sublocations(self):
        """Paragraphs container sub-locations getter"""
        yield from IParagraphContainer(self.context).values()


@subscriber(IObjectAddedEvent, context_selector=IParagraphContainerTarget)
def handle_added_paragraph_container(event):
    """Handle added new paragraphs container

    This subscriber to IObjectAddedEvent is used to automatically
    create new paragraphs based on selected data type or on shared
    content manager settings.
    """
    # don't create new paragraphs if container is not empty
    container = IParagraphContainer(event.object)
    if len(container) > 0:
        return
    content = get_parent(container, IWfSharedContent)
    # only apply manager settings to first version
    state = IWorkflowState(content, None) if content is not None else None
    if (state is not None) and (state.version_id > 1):
        return
    # check for typed shared content settings
    if IWfTypedSharedContent.providedBy(content):
        datatype = content.get_data_type()
        if datatype is not None:
            source = IParagraphContainer(datatype, None)
            if source is not None:
                for paragraph in source.values():
                    container.append(copy(paragraph))
    if len(container) > 0:
        return
    # check for shared content manager auto-created paragraphs
    manager = get_parent(container, IParagraphFactorySettingsTarget)
    if manager is not None:
        settings = IParagraphFactorySettings(manager)
        for name in settings.auto_created_paragraphs or ():
            factory = get_object_factory(IBaseParagraph, name=name)
            if factory is not None:
                container.append(factory())
