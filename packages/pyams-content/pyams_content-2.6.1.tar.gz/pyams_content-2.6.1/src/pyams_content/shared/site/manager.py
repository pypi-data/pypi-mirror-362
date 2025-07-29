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

"""PyAMS_content.shared.site.manager module

"""

from pyramid.events import subscriber
from zope.container.ordered import OrderedContainer
from zope.interface import implementer
from zope.lifecycleevent.interfaces import IObjectAddedEvent, IObjectMovedEvent, IObjectRemovedEvent
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_content.component.illustration.interfaces import IIllustrationTarget, ILinkIllustrationTarget
from pyams_content.component.thesaurus.interfaces import IThemesManagerTarget
from pyams_content.feature.preview.interfaces import IPreviewTarget
from pyams_content.interfaces import MANAGE_SITE_PERMISSION
from pyams_content.reference.pictogram.interfaces import IPictogramManagerTarget
from pyams_content.shared.common.interfaces import ISharedContent
from pyams_content.shared.common.manager import BaseSharedTool
from pyams_content.shared.common.types import TypedSharedToolMixin
from pyams_content.shared.site.container import SiteContainerMixin
from pyams_content.shared.site.interfaces import ISiteManager, PYAMS_SITES_VOCABULARY, SITE_TOPIC_CONTENT_TYPE
from pyams_i18n.interfaces import II18n
from pyams_layer.skin import UserSkinnableContentMixin
from pyams_portal.interfaces import IPortalContext, IPortalFooterContext, IPortalHeaderContext
from pyams_security.interfaces import IDefaultProtectionPolicy, IViewContextPermissionChecker
from pyams_site.interfaces import ISiteRoot
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.factory import factory_config, get_object_factory
from pyams_utils.registry import get_utilities_for
from pyams_utils.request import query_request, check_request
from pyams_utils.traversing import get_parent
from pyams_utils.vocabulary import vocabulary_config

__docformat__ = 'restructuredtext'

from pyams_content import _


@factory_config(ISiteManager)
@implementer(IDefaultProtectionPolicy, IPictogramManagerTarget, IThemesManagerTarget,
             IIllustrationTarget, ILinkIllustrationTarget,
             IPortalContext, IPortalHeaderContext, IPortalFooterContext, IPreviewTarget)
class SiteManager(SiteContainerMixin, OrderedContainer, TypedSharedToolMixin, BaseSharedTool,
                  UserSkinnableContentMixin):
    """Site manager persistent class"""

    header = FieldProperty(ISiteManager['header'])
    description = FieldProperty(ISiteManager['description'])
    notepad = FieldProperty(ISiteManager['notepad'])
    navigation_mode = FieldProperty(ISiteManager['navigation_mode'])
    indexation_mode = FieldProperty(ISiteManager['indexation_mode'])

    sequence_name = ''  # use default sequence generator
    sequence_prefix = ''

    content_name = _("Site manager")

    shared_content_type = SITE_TOPIC_CONTENT_TYPE

    @property
    def shared_content_factory(self):
        return get_object_factory(ISharedContent, name=self.shared_content_type)

    def is_deletable(self):
        for element in self.values():
            if not element.is_deletable():
                return False
        return True


@subscriber(IObjectAddedEvent, context_selector=ISiteManager)
def handle_added_site_manager(event: IObjectAddedEvent):
    """Register site manager when added"""
    site = get_parent(event.newParent, ISiteRoot)
    registry = site.getSiteManager()
    if registry is not None:
        registry.registerUtility(event.object, ISiteManager, name=event.newName)


@subscriber(IObjectMovedEvent, context_selector=ISiteManager)
def handle_moved_site_manager(event: IObjectMovedEvent):
    """Update site manager registration when renamed"""
    if IObjectRemovedEvent.providedBy(event):
        return
    request = check_request()
    registry = request.root.getSiteManager()
    if registry is not None:
        old_name = event.oldName
        new_name = event.newName
        if old_name == new_name:
            return
        registry.unregisterUtility(event.object, ISiteManager, name=old_name)
        if new_name:
            registry.registerUtility(event.object, ISiteManager, name=new_name)


@subscriber(IObjectRemovedEvent, context_selector=ISiteManager)
def handle_deleted_site_manager(event: IObjectRemovedEvent):
    """Un-register site manager when deleted"""
    site = get_parent(event.oldParent, ISiteRoot)
    registry = site.getSiteManager()
    if registry is not None:
        registry.unregisterUtility(event.object, ISiteManager, name=event.oldName)


@adapter_config(required=ISiteManager,
                provides=IViewContextPermissionChecker)
class SiteManagerPermissionChecker(ContextAdapter):
    """Site manager edit permission checker"""

    edit_permission = MANAGE_SITE_PERMISSION


@vocabulary_config(name=PYAMS_SITES_VOCABULARY)
class SiteManagerVocabulary(SimpleVocabulary):
    """Site manager vocabulary"""

    interface = ISiteManager

    def __init__(self, context=None):
        request = query_request()
        super().__init__([
            SimpleTerm(v, title=II18n(t).query_attribute('title', request=request))
            for v, t in get_utilities_for(self.interface)
        ])
