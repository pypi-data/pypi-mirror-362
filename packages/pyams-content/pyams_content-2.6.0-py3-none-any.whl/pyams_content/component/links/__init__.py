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

"""PyAMS_content.component.links module

"""

from html import escape

from pyramid.encode import url_quote, urlencode
from pyramid.events import subscriber
from zope.interface import alsoProvides, directlyProvidedBy, implementer, noLongerProvides
from zope.lifecycleevent import IObjectAddedEvent, IObjectModifiedEvent
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_content.component.association import AssociationItem
from pyams_content.component.association.interfaces import IAssociationContainer, \
    IAssociationContainerTarget, IAssociationInfo
from pyams_content.component.links.interfaces import CONTENT_LINKS_VOCABULARY, \
    EXTERNAL_LINK_ICON_CLASS, EXTERNAL_LINK_ICON_HINT, IBaseLink, \
    IExternalLink, IInternalLink, IInternalLinkCustomInfo, IInternalLinkCustomInfoTarget, \
    IMailtoLink, INTERNAL_LINK_ICON_CLASS, INTERNAL_LINK_ICON_HINT, MAILTO_LINK_ICON_CLASS, \
    MAILTO_LINK_ICON_HINT
from pyams_content.reference.pictogram.interfaces import IPictogramTable
from pyams_i18n.interfaces import II18n
from pyams_sequence.interfaces import IInternalReference, ISequentialIdInfo
from pyams_sequence.reference import InternalReferenceMixin
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.factory import factory_config
from pyams_utils.interfaces import MISSING_INFO
from pyams_utils.registry import query_utility
from pyams_utils.request import check_request
from pyams_utils.traversing import get_parent
from pyams_utils.url import canonical_url, relative_url
from pyams_utils.vocabulary import vocabulary_config
from pyams_utils.zodb import volatile_property
from pyams_workflow.interfaces import IWorkflowPublicationInfo


__docformat__ = 'restructuredtext'


#
# Links vocabulary
#

@vocabulary_config(name=CONTENT_LINKS_VOCABULARY)
class ContentLinksVocabulary(SimpleVocabulary):
    """Content links vocabulary"""

    def __init__(self, context=None):
        terms = []
        target = get_parent(context, IAssociationContainerTarget)
        if target is not None:
            terms = [
                SimpleTerm(link.__name__, title=IAssociationInfo(link).inner_title)
                for link in IAssociationContainer(target).values()
                if IBaseLink.providedBy(link)
            ]
        super(ContentLinksVocabulary, self).__init__(terms)


#
# Base link persistent class
#

@implementer(IBaseLink)
class BaseLink(AssociationItem):
    """Base link persistent class"""

    title = FieldProperty(IBaseLink['title'])
    description = FieldProperty(IBaseLink['description'])
    _pictogram_name = FieldProperty(IBaseLink['pictogram_name'])

    @property
    def pictogram_name(self):
        """Pictogram name getter"""
        return self._pictogram_name

    @pictogram_name.setter
    def pictogram_name(self, value):
        """Pictogram name setter"""
        if value != self._pictogram_name:
            self._pictogram_name = value
            del self.pictogram

    @volatile_property
    def pictogram(self):
        """Pictogram getter"""
        if not self.pictogram_name:
            return None
        table = query_utility(IPictogramTable)
        if table is not None:
            return table.get(self._pictogram_name)


class BaseLinkInfoAdapter(ContextAdapter):
    """Base link association info adapter"""

    @property
    def pictogram(self):
        """Pictogram getter"""
        return self.context.icon_class

    user_icon = None


#
# Internal links
#

@factory_config(IInternalLink)
class InternalLink(InternalReferenceMixin, BaseLink):
    """Internal link persistent class"""

    icon_class = INTERNAL_LINK_ICON_CLASS
    icon_hint = INTERNAL_LINK_ICON_HINT

    _reference = FieldProperty(IInternalLink['reference'])
    force_canonical_url = FieldProperty(IInternalLink['force_canonical_url'])

    def is_visible(self, request=None):
        """Link visibility getter"""
        target = self.get_target()
        if target is not None:
            publication_info = IWorkflowPublicationInfo(target, None)
            if publication_info is not None:
                return publication_info.is_visible(request)
        return False

    def get_editor_url(self):
        """Editor URL getter"""
        return 'oid://{0}'.format(self.reference)

    def get_url(self, request=None, view_name=None):
        """URL getter"""
        target = self.get_target()
        if target is not None:
            if request is None:
                request = check_request()
            params = None
            if IInternalLinkCustomInfoTarget.providedBy(target):
                custom_info = IInternalLinkCustomInfo(self, None)
                if custom_info is not None:
                    params = custom_info.get_url_params()
                    if params:
                        params = urlencode(params)
            if self.force_canonical_url:
                return canonical_url(target, request, view_name, query=params)
            return relative_url(target, request, view_name=view_name, query=params)
        return ''


@subscriber(IObjectAddedEvent, context_selector=IInternalLink)
def handle_new_internal_link(event):
    """Check if link target is providing custom info"""
    link = event.object
    target = link.target
    if target is not None:
        info = IInternalLinkCustomInfoTarget(target, None)
        if info is not None:
            alsoProvides(link, info.internal_link_marker_interface)


@subscriber(IObjectModifiedEvent, context_selector=IInternalLink)
def handle_updated_internal_link(event):
    """Check when modified if new link target is providing custom info"""
    link = event.object
    # remove previous provided interfaces
    ifaces = tuple([
        iface for iface in directlyProvidedBy(link)
        if issubclass(iface, IInternalLinkCustomInfo)
    ])
    for iface in ifaces:
        noLongerProvides(link, iface)
    target = link.target
    if target is not None:
        info = IInternalLinkCustomInfoTarget(target, None)
        if info is not None:
            alsoProvides(link, info.internal_link_marker_interface)


@adapter_config(required=IInternalReference,
                provides=IAssociationInfo)
class InternalLinkAssociationInfoAdapter(BaseLinkInfoAdapter):
    """Internal link association info adapter"""

    @property
    def user_title(self):
        """User title getter"""
        title = II18n(self.context).query_attribute('title')
        if not title:
            target = self.context.get_target()
            if target is not None:
                title = II18n(target).query_attribute('title')
        return title or MISSING_INFO

    @property
    def user_header(self):
        """User header getter"""
        description = II18n(self.context).query_attribute('description')
        if not description:
            target = self.context.get_target()
            if (target is not None) and hasattr(target, 'header'):
                description = II18n(target).query_attribute('header')
        return description

    @property
    def inner_title(self):
        """Inner title getter"""
        target = self.context.get_target()
        if target is not None:
            sequence = ISequentialIdInfo(target)
            return '{0} ({1})'.format(II18n(target).query_attribute('title'),
                                      sequence.get_short_oid())
        return MISSING_INFO

    @property
    def human_size(self):
        """Human size getter"""
        return MISSING_INFO


#
# External links
#

@factory_config(IExternalLink)
class ExternalLink(BaseLink):
    """External link persistent class"""

    icon_class = EXTERNAL_LINK_ICON_CLASS
    icon_hint = EXTERNAL_LINK_ICON_HINT

    url = FieldProperty(IExternalLink['url'])
    language = FieldProperty(IExternalLink['language'])

    def get_editor_url(self):
        """Editor URL getter"""
        return self.url

    def get_url(self, request=None, view_name=None):
        """URL getter"""
        return self.url


@adapter_config(required=IExternalLink,
                provides=IAssociationInfo)
class ExternalLinkAssociationInfoAdapter(BaseLinkInfoAdapter):
    """External link association info adapter"""

    @property
    def user_title(self):
        """User title getter"""
        title = II18n(self.context).query_attribute('title')
        if not title:
            title = self.context.url
        return title or MISSING_INFO

    @property
    def user_header(self):
        """User header getter"""
        return II18n(self.context).query_attribute('description')

    @property
    def inner_title(self):
        """Inner title getter"""
        return self.context.url

    @property
    def human_size(self):
        """Human size getter"""
        return MISSING_INFO


#
# Mailto links
#

@factory_config(IMailtoLink)
class MailtoLink(BaseLink):
    """Mailto link persistent class"""

    icon_class = MAILTO_LINK_ICON_CLASS
    icon_hint = MAILTO_LINK_ICON_HINT

    address = FieldProperty(IMailtoLink['address'])
    address_name = FieldProperty(IMailtoLink['address_name'])

    def get_editor_url(self):
        """Editor URL getter"""
        return 'mailto:{0} <{1}>'.format(self.address_name, self.address)

    def get_url(self, request=None, view_name=None):
        """URL getter"""
        return 'mailto:{}'.format(url_quote('{} <{}>'.format(self.address_name, self.address))
                                  if self.address_name else self.address)


@adapter_config(required=IMailtoLink,
                provides=IAssociationInfo)
class MailtoLinkAssociationInfoAdapter(BaseLinkInfoAdapter):
    """Mailto link association info adapter"""

    @property
    def user_title(self):
        """User title getter"""
        title = II18n(self.context).query_attribute('title')
        if not title:
            title = self.context.address_name
        return title or MISSING_INFO

    @property
    def user_header(self):
        """User header getter"""
        return II18n(self.context).query_attribute('description')

    @property
    def inner_title(self):
        """Inner title getter"""
        if self.context.address_name:
            return escape('{} <{}>'.format(self.context.address_name, self.context.address))
        return self.context.address

    @property
    def human_size(self):
        """Human size getter"""
        return MISSING_INFO
