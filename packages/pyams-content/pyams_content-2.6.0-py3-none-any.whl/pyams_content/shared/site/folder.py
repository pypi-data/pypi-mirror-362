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

"""PyAMS_content.shared.folder module

This module provides persistent classes to handles sites folders, which are used to group
contents together.
"""

from pyramid.events import subscriber
from zope.container.ordered import OrderedContainer
from zope.interface import alsoProvides, implementer
from zope.intid import IIntIds
from zope.lifecycleevent import IObjectAddedEvent
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_content.component.illustration.interfaces import IIllustrationTarget, \
    ILinkIllustrationTarget
from pyams_content.component.links import InternalLink
from pyams_content.component.thesaurus import IThemesTarget
from pyams_content.feature.navigation.interfaces import IDynamicMenu
from pyams_content.feature.preview.interfaces import IPreviewTarget
from pyams_content.interfaces import MANAGE_SITE_PERMISSION
from pyams_content.shared.common import ISharedContent
from pyams_content.shared.common.manager import BaseSharedTool
from pyams_content.shared.site.container import SiteContainerMixin
from pyams_content.shared.site.interfaces import ISiteFolder, ISiteManager, \
    SITE_FOLDERS_VOCABULARY, SITE_TOPIC_CONTENT_TYPE
from pyams_i18n.interfaces import II18n
from pyams_portal.interfaces import IPortalContext, IPortalFooterContext, IPortalHeaderContext
from pyams_security.interfaces import IDefaultProtectionPolicy, IViewContextPermissionChecker
from pyams_sequence.interfaces import ISequentialIdInfo
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.factory import factory_config, get_object_factory
from pyams_utils.finder import find_objects_providing
from pyams_utils.registry import get_utility
from pyams_utils.request import query_request
from pyams_utils.traversing import get_parent
from pyams_utils.vocabulary import vocabulary_config

__docformat__ = 'restructuredtext'

from pyams_content import _


@factory_config(ISiteFolder)
@implementer(IDefaultProtectionPolicy,
             IIllustrationTarget, ILinkIllustrationTarget,
             IPortalContext, IPortalHeaderContext, IPortalFooterContext, IPreviewTarget)
class SiteFolder(SiteContainerMixin, OrderedContainer, BaseSharedTool):
    """Site folder persistent class"""

    header = FieldProperty(ISiteFolder['header'])
    description = FieldProperty(ISiteFolder['description'])
    notepad = FieldProperty(ISiteFolder['notepad'])

    visible_in_list = FieldProperty(ISiteFolder['visible_in_list'])
    navigation_title = FieldProperty(ISiteFolder['navigation_title'])
    navigation_mode = FieldProperty(ISiteFolder['navigation_mode'])

    content_name = _("Site folder")

    sequence_name = ''  # use default sequence generator
    sequence_prefix = ''

    shared_content_type = SITE_TOPIC_CONTENT_TYPE

    @property
    def shared_content_factory(self):
        return get_object_factory(ISharedContent, name=self.shared_content_type)

    def is_deletable(self):
        """Check if item can be deleted"""
        for element in self.values():
            if not element.is_deletable():
                return False
        return True


@subscriber(IObjectAddedEvent, context_selector=ISiteFolder, parent_selector=IThemesTarget)
def handle_added_site_folder(event):
    """Handle site folder when added to a themes target"""
    alsoProvides(event.object, IThemesTarget)


@adapter_config(required=ISiteFolder,
                provides=IViewContextPermissionChecker)
class SiteFolderPermissionChecker(ContextAdapter):
    """Site folder edit permission checker"""

    edit_permission = MANAGE_SITE_PERMISSION


@adapter_config(required=ISiteFolder,
                provides=IDynamicMenu)
def site_folder_dynamic_menu(context):
    """Site folder dynamic menu factory"""
    result = InternalLink()
    result.title = context.navigation_title.copy() if context.navigation_title else {}
    result.reference = ISequentialIdInfo(context).hex_oid
    return result


@vocabulary_config(name=SITE_FOLDERS_VOCABULARY)
class SiteManagerFoldersVocabulary(SimpleVocabulary):
    """Site manager folders vocabulary"""

    def __init__(self, context):
        terms = []
        site = get_parent(context, ISiteManager)
        if site is not None:
            request = query_request()
            intids = get_utility(IIntIds)
            for folder in find_objects_providing(site, ISiteFolder):
                terms.append(SimpleTerm(value=intids.queryId(folder),
                                        title=II18n(folder).query_attribute('title',
                                                                            request=request)))
        super().__init__(terms)
