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

"""PyAMS_content.component.gallery module

This module defines persistent components and adapters used to handle medias
galleries.
"""

from pyramid.events import subscriber
from zope.interface import implementer
from zope.lifecycleevent import IObjectAddedEvent, IObjectModifiedEvent, IObjectRemovedEvent, \
    ObjectModifiedEvent
from zope.location import locate
from zope.location.interfaces import ISublocations
from zope.schema.fieldproperty import FieldProperty
from zope.traversing.interfaces import ITraversable

from pyams_catalog.utils import index_object
from pyams_content.component.gallery.interfaces import GALLERY_CONTAINER_KEY, GALLERY_RENDERERS, \
    IBaseGallery, IGallery, IGalleryContainer, IGalleryFile, IGalleryItem, IGalleryTarget
from pyams_content.component.illustration import VirtualIllustration
from pyams_content.component.illustration.interfaces import IBaseIllustration
from pyams_content.component.paragraph import IBaseParagraph
from pyams_content.feature.renderer import RenderedContentMixin, RenderersVocabulary
from pyams_content.interfaces import MANAGE_SITE_ROOT_PERMISSION
from pyams_content.shared.common import IWfSharedContent
from pyams_file.interfaces import IBaseImageFile
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_utils.adapter import ContextAdapter, adapter_config, get_annotation_adapter
from pyams_utils.container import BTreeOrderedContainer
from pyams_utils.factory import factory_config
from pyams_utils.list import boolean_iter
from pyams_utils.registry import get_current_registry
from pyams_utils.traversing import get_parent
from pyams_utils.vocabulary import vocabulary_config


__docformat__ = 'restructuredtext'


@implementer(IGalleryContainer)
class GalleryContainer(BTreeOrderedContainer):
    """Gallery medias container"""

    def get_visible_medias(self):
        """Visible medias iterator"""
        yield from filter(lambda x: IGalleryFile(x).visible, self.values())

    def get_visible_images(self):
        """Visible images iterator"""
        yield from filter(lambda x: IBaseImageFile.providedBy(x.data),
                          self.get_visible_medias())


@factory_config(provided=IBaseGallery)
class BaseGallery(RenderedContentMixin, GalleryContainer):
    """Base gallery persistent class"""

    renderer = FieldProperty(IBaseGallery['renderer'])


@factory_config(provided=IGallery)
class Gallery(BaseGallery):
    """Gallery persistent class"""

    title = FieldProperty(IGallery['title'])
    description = FieldProperty(IGallery['description'])


@adapter_config(required=IGalleryTarget,
                provides=IGallery)
def gallery_adapter(target):
    """Gallery container adapter"""
    return get_annotation_adapter(target, GALLERY_CONTAINER_KEY, IGallery,
                                  name='++gallery++')


@adapter_config(name='gallery',
                required=IGalleryTarget,
                provides=ITraversable)
class GalleryContainerNamespace(ContextAdapter):
    """++gallery++ container namespace traverser"""

    def traverse(self, name, furtherPath=None):
        """Gallery traverser"""
        return get_current_registry().queryAdapter(self.context, IGallery, name=name)


@adapter_config(name='gallery',
                required=IGalleryTarget,
                provides=ISublocations)
class GalleryContainerSublocations(ContextAdapter):
    """Galleries container sub-locations"""

    def sublocations(self):
        """Sub-locations getter"""
        yield from IGallery(self.context).values()


@adapter_config(required=IGallery,
                provides=IViewContextPermissionChecker)
class GalleryPermissionChecker(ContextAdapter):
    """Gallery permission checker"""

    @property
    def edit_permission(self):
        """Edit permission getter"""
        content = get_parent(self.context, IWfSharedContent)
        if content is not None:
            return IViewContextPermissionChecker(content).edit_permission
        return MANAGE_SITE_ROOT_PERMISSION


@subscriber(IObjectAddedEvent, context_selector=IGallery)
@subscriber(IObjectModifiedEvent, context_selector=IGallery)
@subscriber(IObjectRemovedEvent, context_selector=IGallery)
def handle_gallery_event(event):
    """Handle event for added, modified or removed gallery"""
    gallery = event.object
    if IBaseParagraph.providedBy(gallery):
        # there is another event subscriber for paragraphs,
        # so don't trigger event twice !
        return
    content = get_parent(gallery, IWfSharedContent)
    if content is not None:
        get_current_registry().notify(ObjectModifiedEvent(content))


@vocabulary_config(name=GALLERY_RENDERERS)
class GalleryRenderersVocabulary(RenderersVocabulary):
    """Gallery renderers vocabulary"""

    content_interface = IBaseGallery


#
# Illustrations adapters
#

@adapter_config(required=IBaseGallery,
                provides=IBaseIllustration)
def gallery_illustration_adapter(gallery):
    """Gallery illustration adapter"""
    has_medias, medias = boolean_iter(gallery.get_visible_medias())
    if has_medias:
        return IBaseIllustration(next(medias).data, None)
    return None


@adapter_config(required=IGalleryFile,
                provides=IBaseIllustration)
def gallery_file_illustration_adapter(file):
    """Gallery file illustration adapter"""
    illustration = VirtualIllustration(file.data)
    illustration.title = (file.title or {}).copy()
    illustration.alt_title = (file.alt_title or {}).copy()
    illustration.author = file.author
    return illustration
