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

"""PyAMS_content.shared.common module

"""

from hypatia.interfaces import ICatalog
from persistent import Persistent
from pyramid.events import subscriber
from pyramid.settings import asbool
from zope.container.contained import Contained
from zope.dublincore.interfaces import IZopeDublinCore
from zope.interface import implementer
from zope.intid import IIntIds
from zope.lifecycleevent import IObjectModifiedEvent
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_content.feature.filter.interfaces import IFilterValues
from pyams_content.interfaces import IBaseContentInfo, IObjectType
from pyams_content.shared.common.interfaces import CONTENT_TYPES_VOCABULARY, IBaseSharedTool, \
    ISharedContent, IWfSharedContent, IWfSharedContentRoles, SHARED_CONTENT_TYPES_VOCABULARY, \
    VIEWS_SHARED_CONTENT_TYPES_VOCABULARY
from pyams_i18n.content import I18nManagerMixin
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces import IDefaultProtectionPolicy
from pyams_security.interfaces.base import VIEW_PERMISSION
from pyams_security.security import ProtectedObjectMixin
from pyams_security.utility import get_principal
from pyams_sequence.interfaces import ISequentialIdInfo, ISequentialIdTarget
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.date import format_datetime
from pyams_utils.factory import get_all_factories, get_interface_base_name, get_object_factory
from pyams_utils.interfaces.text import IHTMLRenderer
from pyams_utils.property import ClassPropertyType, classproperty
from pyams_utils.registry import query_utility
from pyams_utils.request import check_request, query_request
from pyams_utils.timezone import tztime
from pyams_utils.traversing import get_parent
from pyams_utils.vocabulary import vocabulary_config
from pyams_utils.zodb import volatile_property
from pyams_workflow.interfaces import IObjectClonedEvent, IWorkflow, IWorkflowPublicationSupport, \
    IWorkflowTransitionEvent, IWorkflowVersions
from pyams_zmi.interfaces import IObjectLabel

__docformat__ = 'restructuredtext'

from pyams_content import _


@vocabulary_config(name=SHARED_CONTENT_TYPES_VOCABULARY)
class ContentTypesVocabulary(SimpleVocabulary):
    """Content types vocabulary"""

    def __init__(self, context):
        request = check_request()
        settings = request.registry.settings
        translate = request.localizer.translate
        terms = sorted([
            SimpleTerm(factory.content_type, title=translate(factory.content_name))
            for _name, factory in get_all_factories(ISharedContent)
            if asbool(settings.get(f'pyams_content.register.{factory.content_type}', True))
        ], key=lambda x: x.title)
        super().__init__(terms)


@vocabulary_config(name=VIEWS_SHARED_CONTENT_TYPES_VOCABULARY)
class ViewsContentTypesVocabulary(SimpleVocabulary):
    """Views and search folders content types vocabulary"""

    def __init__(self, context):
        request = check_request()
        settings = request.registry.settings
        translate = request.localizer.translate
        terms = sorted([
            SimpleTerm(factory.content_type, title=translate(factory.content_name))
            for _name, factory in get_all_factories(ISharedContent)
            if factory.content_view and
               asbool(settings.get(f'pyams_content.register.{factory.content_type}', True))
        ], key=lambda x: x.title)
        super().__init__(terms)


#
# Workflow shared content class and adapters
#

@implementer(IDefaultProtectionPolicy, IWfSharedContent, IWorkflowPublicationSupport)
class WfSharedContent(ProtectedObjectMixin, I18nManagerMixin, Persistent, Contained):
    """Shared data content class"""

    content_type = None
    content_name = None
    content_intf = None
    content_view = True

    handle_short_name = False
    handle_content_url = True
    handle_header = True
    handle_description = True

    title = FieldProperty(IWfSharedContent['title'])
    short_name = FieldProperty(IWfSharedContent['short_name'])
    content_url = FieldProperty(IWfSharedContent['content_url'])
    creator = FieldProperty(IWfSharedContent['creator'])
    modifiers = FieldProperty(IWfSharedContent['modifiers'])
    last_modifier = FieldProperty(IWfSharedContent['last_modifier'])
    header = FieldProperty(IWfSharedContent['header'])
    description = FieldProperty(IWfSharedContent['description'])
    keywords = FieldProperty(IWfSharedContent['keywords'])
    notepad = FieldProperty(IWfSharedContent['notepad'])

    @property
    def first_owner(self):
        """First owner getter"""
        versions = IWorkflowVersions(self, None)
        if versions is not None:
            return versions.get_version(1).creator

    @property
    def creation_label(self):
        """Creation label getter"""
        request = check_request()
        translate = request.localizer.translate
        return translate(_('{date} by {principal}')).format(
            date=format_datetime(tztime(IBaseContentInfo(self).created_date)),
            principal=get_principal(request, self.creator).title)

    @property
    def last_update_label(self):
        """Last update label getter"""
        request = check_request()
        translate = request.localizer.translate
        return translate(_('{date} by {principal}')).format(
            date=format_datetime(tztime(IBaseContentInfo(self).modified_date)),
            principal=get_principal(request, self.last_modifier).title)


@subscriber(IObjectModifiedEvent, context_selector=IWfSharedContent)
def handle_modified_shared_content(event):
    """Define content's modifiers when content is modified"""
    request = query_request()
    if request is not None:
        content = event.object
        try:
            principal_id = request.principal.id
        except AttributeError:
            pass
        else:
            modifiers = content.modifiers or set()
            if principal_id not in modifiers:
                modifiers.add(principal_id)
                content.modifiers = modifiers
                catalog = query_utility(ICatalog)
                intids = query_utility(IIntIds)
                catalog['modifiers'].reindex_doc(intids.register(content), content)
            content.last_modifier = principal_id


@subscriber(IObjectClonedEvent, context_selector=IWfSharedContent)
def handle_cloned_shared_content(event):
    """Handle cloned object when a new version is created

    Current principal is set as version creator, and is added to version
    contributors if he is not the original content's owner
    """
    request = query_request()
    principal_id = request.principal.id
    content = event.object
    content.creator = principal_id
    roles = IWfSharedContentRoles(content)
    if principal_id not in roles.owner:
        # creation of new versions doesn't change owner
        # but new creators are added to contributors list
        contributors = roles.contributors or set()
        contributors.add(principal_id)
        roles.contributors = contributors
    # reset modifiers
    content.modifiers = set()


@adapter_config(required=IWfSharedContent,
                provides=ISequentialIdInfo)
def wf_shared_content_sequence_adapter(context):
    """Shared content sequence adapter"""
    parent = get_parent(context, ISharedContent)
    if parent is not None:
        return ISequentialIdInfo(parent)


@adapter_config(required=IWfSharedContent,
                provides=IObjectType)
def wf_shared_content_object_type(context):
    """Shared content object type adapter"""
    return get_interface_base_name(context.content_intf)


@adapter_config(required=(IWfSharedContent, IPyAMSLayer),
                provides=IObjectLabel)
def wf_shared_content_label(context, request):
    """Shared content label adapter"""
    return II18n(context).query_attribute('title', request=request)


@adapter_config(required=IWfSharedContent,
                provides=IBaseContentInfo)
class WfSharedContentInfoAdapter(ContextAdapter):
    """Shared content base info adapter"""

    @property
    def created_date(self):
        """Creation date getter"""
        return IZopeDublinCore(self.context).created

    @property
    def modified_date(self):
        """Last modification date getter"""
        return IZopeDublinCore(self.context).modified


@adapter_config(required=IWfSharedContent,
                provides=IWorkflow)
def wf_shared_content_workflow_adapter(context):
    """Shared content workflow adapter"""
    parent = get_parent(context, IBaseSharedTool)
    return query_utility(IWorkflow, name=parent.shared_content_workflow)


@adapter_config(name='content_type',
                required=IWfSharedContent,
                provides=IFilterValues)
def shared_content_filter_values(context):
    """Shared content filter values"""
    yield f"content_type:{context.content_type}"


#
# Main shared content class and adapters
#

@implementer(ISharedContent, ISequentialIdTarget)
class SharedContent(Persistent, Contained, metaclass=ClassPropertyType):
    """Workflow managed shared data"""

    view_permission = VIEW_PERMISSION

    sequence_name = ''  # use default sequence generator
    sequence_prefix = ''

    content_type = None
    content_name = None
    content_view = True

    @classproperty
    def content_factory(cls):
        """Content class getter"""
        return get_object_factory(IWfSharedContent, name=cls.content_type)

    @property
    def workflow_name(self):
        """Workflow getter"""
        return get_parent(self, IBaseSharedTool).shared_content_workflow

    @volatile_property
    def visible_version(self):
        workflow = IWorkflow(self)
        versions = IWorkflowVersions(self).get_versions(workflow.visible_states, sort=True)
        if versions:
            return versions[-1]
        return None


@adapter_config(required=ISharedContent,
                provides=IBaseContentInfo)
class SharedContentInfoAdapter(ContextAdapter):
    """Shared content base info adapter"""

    @property
    def created_date(self):
        """Creation date getter"""
        return IZopeDublinCore(self.context).created

    @property
    def modified_date(self):
        """Modification date getter"""
        return IZopeDublinCore(self.context).modified


@adapter_config(required=ISharedContent,
                provides=IWorkflow)
def shared_content_workflow_adapter(context):
    """Shared content workflow adapter"""
    parent = get_parent(context, IBaseSharedTool)
    return query_utility(IWorkflow, name=parent.shared_content_workflow)


@subscriber(IWorkflowTransitionEvent)
def handle_workflow_event(event):
    """Reset target on workflow transition"""
    content = get_parent(event.object, ISharedContent)
    if content is not None:
        del content.visible_version


@adapter_config(name='text_with_oid',
                required=(ISharedContent, str),
                provides=IHTMLRenderer)
@adapter_config(name='text_with_oid',
                required=(IWfSharedContent, str),
                provides=IHTMLRenderer)
class SharedContentTextWithOIDRenderer:
    """Shared content text with OID renderer"""

    def __init__(self, context, value):
        self.context = context
        self.value = value

    def render(self, **kwargs):
        sequence = ISequentialIdInfo(self.context, None)
        if sequence is None:
            return self.value
        return f'{self.value} ({sequence.public_oid})'
