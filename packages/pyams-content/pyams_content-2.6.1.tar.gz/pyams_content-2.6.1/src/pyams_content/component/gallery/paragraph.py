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

"""PyAMS_content.component.gallery.paragraph module

"""

from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.gallery import BaseGallery
from pyams_content.component.gallery.interfaces import GALLERY_PARAGRAPH_ICON_CLASS, \
    GALLERY_PARAGRAPH_NAME, GALLERY_PARAGRAPH_RENDERERS, GALLERY_PARAGRAPH_TYPE, IGalleryParagraph
from pyams_content.component.paragraph import BaseParagraph, IBaseParagraph
from pyams_content.feature.renderer import RenderersVocabulary
from pyams_utils.factory import factory_config
from pyams_utils.vocabulary import vocabulary_config


__docformat__ = 'restructuredtext'


@factory_config(IGalleryParagraph)
@factory_config(IBaseParagraph, name=GALLERY_PARAGRAPH_TYPE)
class GalleryParagraph(BaseGallery, BaseParagraph):
    """Gallery class"""

    factory_name = GALLERY_PARAGRAPH_TYPE
    factory_label = GALLERY_PARAGRAPH_NAME
    factory_intf = IGalleryParagraph

    icon_class = GALLERY_PARAGRAPH_ICON_CLASS

    renderer = FieldProperty(IGalleryParagraph['renderer'])


@vocabulary_config(name=GALLERY_PARAGRAPH_RENDERERS)
class GalleryParagraphRenderersVocabulary(RenderersVocabulary):
    """Gallery paragraph renderers vocabulary"""

    content_interface = IGalleryParagraph
