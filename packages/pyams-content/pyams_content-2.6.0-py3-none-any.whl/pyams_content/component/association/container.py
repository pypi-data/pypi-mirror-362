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

"""PyAMS_content.component.association.container module

This module provides associations container component.
"""

__docformat__ = 'restructuredtext'

from zope.container.ordered import OrderedContainer
from zope.location import locate
from zope.location.interfaces import ISublocations
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.traversing.interfaces import ITraversable

from pyams_catalog.utils import index_object
from pyams_content.component.association import IAssociationContainer, \
    IAssociationContainerTarget, IAssociationItem
from pyams_content.component.association.interfaces import ASSOCIATION_CONTAINER_KEY, \
    ASSOCIATION_VOCABULARY, IAssociationInfo
from pyams_utils.adapter import ContextAdapter, adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.registry import get_pyramid_registry
from pyams_utils.traversing import get_parent
from pyams_utils.vocabulary import vocabulary_config
from pyams_zmi.interfaces import IAdminLayer


@factory_config(IAssociationContainer)
class AssociationContainer(OrderedContainer):
    """Association container"""

    last_id = 1

    def append(self, value, notify=True):
        """Append item to container"""
        key = str(self.last_id)
        if not notify:
            # pre-locate association item to avoid multiple notifications
            locate(value, self, key)
        self[key] = value
        self.last_id += 1
        if not notify:
            # make sure that association item is correctly indexed
            index_object(value)

    def get_visible_items(self, request=None):
        """Visible items iterator"""
        for item in filter(lambda x: IAssociationItem(x).visible, self.values()):
            if IAdminLayer.providedBy(request) or item.is_visible(request):
                yield item


@adapter_config(required=IAssociationContainerTarget,
                provides=IAssociationContainer)
def association_container_factory(target):
    """Associations container factory"""
    return get_annotation_adapter(target, ASSOCIATION_CONTAINER_KEY, IAssociationContainer,
                                  name='++ass++')


@adapter_config(name='ass',
                required=IAssociationContainerTarget,
                provides=ITraversable)
class AssociationContainerNamespace(ContextAdapter):
    """Associations container ++ass++ namespace"""

    def traverse(self, name, furtherpath=None):  # pylint: disable=unused-argument
        """Associations container traverser"""
        registry = get_pyramid_registry()
        return registry.queryAdapter(self.context, IAssociationContainer, name=name or '')


@adapter_config(name='associations',
                required=IAssociationContainerTarget,
                provides=ISublocations)
class AssociationContainerSublocations(ContextAdapter):
    """Associations container sub-locations adapter"""

    def sublocations(self):
        """Sub-locations iterator"""
        yield from IAssociationContainer(self.context).values()


@vocabulary_config(name=ASSOCIATION_VOCABULARY)
class ContentAssociationsVocabulary(SimpleVocabulary):
    """Content associations vocabulary"""

    def __init__(self, context=None):
        terms = []
        target = get_parent(context, IAssociationContainerTarget)
        if target is not None:
            terms = [
                SimpleTerm(link.__name__, title=IAssociationInfo(link).inner_title)
                for link in IAssociationContainer(target).values()
            ]
        super().__init__(terms)
