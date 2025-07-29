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

"""PyAMS_content.component.keynumber module

This module provides persistent classes used to handle key numbers.
"""

from persistent import Persistent
from pyramid.events import subscriber
from zope.container.contained import Contained
from zope.interface import Interface, implementer
from zope.lifecycleevent import ObjectModifiedEvent
from zope.lifecycleevent.interfaces import IObjectAddedEvent, IObjectModifiedEvent, IObjectRemovedEvent
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.keynumber.interfaces import IKeyNumberInfo, IKeyNumbersContainer, IKeyNumbersParagraph, \
    KEYNUMBERS_PARAGRAPH_ICON_CLASS, KEYNUMBERS_PARAGRAPH_NAME, KEYNUMBERS_PARAGRAPH_RENDERERS, \
    KEYNUMBERS_PARAGRAPH_TYPE
from pyams_content.component.paragraph import BaseParagraph, IBaseParagraph, ParagraphPermissionChecker
from pyams_content.feature.renderer import RenderersVocabulary
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import MANAGE_TEMPLATE_PERMISSION
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.container import BTreeOrderedContainer
from pyams_utils.factory import factory_config
from pyams_utils.registry import get_pyramid_registry
from pyams_utils.traversing import get_parent
from pyams_utils.vocabulary import vocabulary_config
from pyams_zmi.interfaces import IObjectLabel

__docformat__ = 'restructuredtext'


@factory_config(provided=IKeyNumberInfo)
class KeyNumber(Persistent, Contained):
    """Key number persistent class"""

    visible = FieldProperty(IKeyNumberInfo['visible'])
    label = FieldProperty(IKeyNumberInfo['label'])
    number = FieldProperty(IKeyNumberInfo['number'])
    unit = FieldProperty(IKeyNumberInfo['unit'])
    text = FieldProperty(IKeyNumberInfo['text'])


@subscriber(IObjectAddedEvent, context_selector=IKeyNumberInfo)
@subscriber(IObjectModifiedEvent, context_selector=IKeyNumberInfo)
@subscriber(IObjectRemovedEvent, context_selector=IKeyNumberInfo)
def handle_modified_key_number(event):
    """Notify container on added, modified or removed key number"""
    container = get_parent(event.object, IKeyNumbersContainer)
    if container is not None:
        registry = get_pyramid_registry()
        registry.notify(ObjectModifiedEvent(container))


@adapter_config(required=IKeyNumberInfo,
                provides=IViewContextPermissionChecker)
class KeyNumberPermissionChecker(ContextAdapter):
    """Key-number permission checker"""
    
    @property
    def edit_permission(self):
        container = get_parent(self.context, IKeyNumbersContainer)
        if container is not None:
            return IViewContextPermissionChecker(container).edit_permission
        return None
    

@adapter_config(required=(IKeyNumberInfo, IPyAMSLayer, Interface),
                provides=IObjectLabel)
def key_number_label(context, request, view):  # pylint: disable=unused-argument
    """Key number label getter"""
    return II18n(context).get_attribute('label', request=request)


@implementer(IKeyNumbersContainer)
class KeyNumbersContainer(BTreeOrderedContainer):
    """Key numbers container"""

    def get_visible_items(self):
        """Get iterator over visible items"""
        yield from filter(lambda x: x.visible, self.values())


@adapter_config(required=IKeyNumbersContainer,
                provides=IViewContextPermissionChecker)
class KeyNumbersContainerPermissionChecker(ContextAdapter):
    """Key-number container permission checker"""
    
    edit_permission = MANAGE_TEMPLATE_PERMISSION


@factory_config(IKeyNumbersParagraph)
@factory_config(IBaseParagraph, name=KEYNUMBERS_PARAGRAPH_TYPE)
class KeyNumbersParagraph(KeyNumbersContainer, BaseParagraph):
    """Key numbers paragraph"""

    factory_name = KEYNUMBERS_PARAGRAPH_TYPE
    factory_label = KEYNUMBERS_PARAGRAPH_NAME
    factory_intf = IKeyNumbersParagraph

    icon_class = KEYNUMBERS_PARAGRAPH_ICON_CLASS
    secondary = True

    renderer = FieldProperty(IKeyNumbersParagraph['renderer'])


@adapter_config(required=IKeyNumbersParagraph,
                provides=IViewContextPermissionChecker)
class KeyNumbersParagraphPermissionChecker(ParagraphPermissionChecker):
    """Key-number paragraph permission checker"""


@vocabulary_config(name=KEYNUMBERS_PARAGRAPH_RENDERERS)
class KeyNumbersParagraphRenderersVocabulary(RenderersVocabulary):
    """Key numbers paragraph renderers vocabulary"""

    content_interface = IKeyNumbersParagraph
