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

"""PyAMS_content.component.illustration module

"""

from persistent import Persistent
from pyramid.events import subscriber
from zope.container.contained import Contained
from zope.interface import alsoProvides, classImplements
from zope.lifecycleevent import IObjectAddedEvent, IObjectModifiedEvent, ObjectAddedEvent
from zope.location.interfaces import ISublocations
from zope.schema.fieldproperty import FieldProperty
from zope.traversing.interfaces import ITraversable

from pyams_content.component.illustration.interfaces import BASIC_ILLUSTRATION_KEY, \
    IBaseIllustration, IBaseIllustrationTarget, IIllustration, IIllustrationTarget, \
    IIllustrationTargetBase, ILLUSTRATION_KEY, ILLUSTRATION_RENDERERS, ILinkIllustration, \
    ILinkIllustrationTarget, IParagraphIllustration, LINK_ILLUSTRATION_KEY
from pyams_content.component.paragraph import IBaseParagraph
from pyams_content.feature.renderer import RenderedContentMixin, RenderersVocabulary
from pyams_file.interfaces import IFileInfo, IImageFile, IResponsiveImage
from pyams_file.property import I18nFileProperty
from pyams_i18n.interfaces import II18n, INegotiator
from pyams_site.site import BaseSiteRoot
from pyams_utils.adapter import ContextAdapter, adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.registry import get_pyramid_registry, query_utility
from pyams_utils.request import check_request
from pyams_utils.vocabulary import vocabulary_config

__docformat__ = 'restructuredtext'


classImplements(BaseSiteRoot, IIllustrationTarget)


@factory_config(IBaseIllustration)
class BasicIllustration(Persistent, Contained):
    """Illustration persistent class"""

    _data = I18nFileProperty(IBaseIllustration['data'])
    title = FieldProperty(IBaseIllustration['title'])
    alt_title = FieldProperty(IBaseIllustration['alt_title'])
    author = FieldProperty(IBaseIllustration['author'])

    @property
    def data(self):
        """Data property getter"""
        return self._data

    @data.setter
    def data(self, value):
        """Data property setter"""
        self._data = value
        for data in (self._data or {}).values():
            if IImageFile.providedBy(data):
                alsoProvides(data, IResponsiveImage)

    @data.deleter
    def data(self):
        """Data property deleter"""
        del self._data

    def has_data(self):
        if not self._data:
            return False
        for data in self._data.values():
            if bool(data):
                return True
        return False


@factory_config(provided=IIllustration)
class Illustration(RenderedContentMixin, BasicIllustration):
    """Illustration persistent class"""

    description = FieldProperty(IIllustration['description'])
    renderer = FieldProperty(IIllustration['renderer'])


@adapter_config(required=IBaseIllustrationTarget,
                provides=IIllustration)
def basic_illustration_factory(context):
    """Basic illustration factory"""

    def illustration_callback(illustration):
        get_pyramid_registry().notify(ObjectAddedEvent(illustration, context,
                                                       illustration.__name__))

    return get_annotation_adapter(context, BASIC_ILLUSTRATION_KEY, IBaseIllustration,
                                  name='++illustration++',
                                  callback=illustration_callback)


@adapter_config(required=IIllustrationTarget,
                provides=IIllustration)
def illustration_factory(context):
    """Illustration factory"""

    def illustration_callback(illustration):
        if IBaseParagraph.providedBy(context):
            alsoProvides(illustration, IParagraphIllustration)
        get_pyramid_registry().notify(ObjectAddedEvent(illustration, context,
                                                       illustration.__name__))

    return get_annotation_adapter(context, ILLUSTRATION_KEY, IIllustration,
                                  name='++illustration++',
                                  callback=illustration_callback)


@adapter_config(required=ILinkIllustrationTarget,
                provides=ILinkIllustration)
@adapter_config(name='link',
                required=ILinkIllustrationTarget,
                provides=IIllustration)
def link_illustration_factory(context):
    """Link illustration factory"""

    def illustration_callback(illustration):
        get_pyramid_registry().notify(ObjectAddedEvent(illustration, context,
                                                       illustration.__name__))

    return get_annotation_adapter(context, LINK_ILLUSTRATION_KEY, IBaseIllustration,
                                  markers=ILinkIllustration,
                                  name='++illustration++link',
                                  callback=illustration_callback)


def update_illustration_properties(illustration):
    """Update missing file properties"""
    request = check_request()
    i18n = query_utility(INegotiator)
    if i18n is not None:
        lang = i18n.server_language
        data = II18n(illustration).get_attribute('data', lang, request)
        if data:
            info = IFileInfo(data)
            info.title = II18n(illustration).get_attribute('title', lang, request)
            info.description = II18n(illustration).get_attribute('alt_title', lang, request)


@subscriber(IObjectAddedEvent, context_selector=IBaseIllustration)
def handle_added_illustration(event):
    """Handle added illustration"""
    illustration = event.object
    update_illustration_properties(illustration)


@subscriber(IObjectModifiedEvent, context_selector=IBaseIllustration)
def handle_modified_illustration(event):
    """Handle modified illustration"""
    illustration = event.object
    update_illustration_properties(illustration)


@adapter_config(name='illustration',
                required=IIllustrationTargetBase,
                provides=ITraversable)
class IllustrationNamespace(ContextAdapter):
    """++illustration++ namespace adapter"""

    def traverse(self, name, furtherpath=None):
        registry = get_pyramid_registry()
        return registry.queryAdapter(self.context, IIllustration, name=name)


@adapter_config(name='illustration',
                required=IIllustrationTargetBase,
                provides=ISublocations)
class IllustrationSublocations(ContextAdapter):
    """Illustration sub-locations adapter"""

    def sublocations(self):
        """Sub-locations iterator"""
        registry = get_pyramid_registry()
        for _name, adapter in registry.getAdapters((self.context,), IBaseIllustration):
            yield adapter


@vocabulary_config(name=ILLUSTRATION_RENDERERS)
class IllustrationRenderersVocabulary(RenderersVocabulary):
    """Illustration renderers vocabulary"""

    content_interface = IIllustration


#
# Custom image file to illustration adapter
#

@adapter_config(required=IImageFile,
                provides=IBaseIllustration)
class VirtualIllustration:
    """Virtual illustration based on image file"""

    title = None
    alt_title = None
    author = None

    def __init__(self, source):
        self.source = source

    @property
    def data(self):
        return self.source

    def has_data(self):
        return bool(self.source)
