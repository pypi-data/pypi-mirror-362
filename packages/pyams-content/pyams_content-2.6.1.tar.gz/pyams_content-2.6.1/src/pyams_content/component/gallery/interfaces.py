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

"""PyAMS_content.component.gallery.interfaces module

"""

from zope.annotation import IAttributeAnnotatable
from zope.container.constraints import containers, contains
from zope.container.interfaces import IOrderedContainer
from zope.interface import Interface
from zope.schema import Bool, Choice, TextLine

from pyams_content.component.paragraph import IBaseParagraph
from pyams_content.component.paragraph.schema import ParagraphRendererChoice
from pyams_content.feature.renderer import IRenderedContent
from pyams_file.schema import AudioField, MediaField
from pyams_i18n.schema import I18nTextField, I18nTextLineField


__docformat__ = 'restructuredtext'

from pyams_content import _  # pylint: disable=ungrouped-imports


GALLERY_CONTAINER_KEY = 'pyams_content.gallery'
GALLERY_RENDERERS = 'pyams.gallery.renderers'


class IGalleryItem(Interface):
    """Gallery item interface"""

    containers('.IGallery')


class IGalleryFile(IGalleryItem):
    """Gallery file interface"""

    data = MediaField(title=_("Image or video data"),
                      description=_("Image or video content"),
                      required=True)

    title = I18nTextLineField(title=_("Legend"),
                              required=False)

    alt_title = I18nTextLineField(title=_("Accessibility title"),
                                  description=_("Alternate title used to describe media content"),
                                  required=False)

    description = I18nTextField(title=_("Associated text"),
                                description=_("Media description can be displayed in "
                                              "front-office templates"),
                                required=False)

    author = TextLine(title=_("Author"),
                      description=_("Name of media's author"),
                      required=False)

    sound = AudioField(title=_("Audio data"),
                       description=_("Sound file associated with the current media"),
                       required=False)

    sound_title = I18nTextLineField(title=_("Sound title"),
                                    description=_("Title of associated sound file"),
                                    required=False)

    sound_description = I18nTextField(title=_("Sound description"),
                                      description=_("Short description of associated sound file"),
                                      required=False)

    visible = Bool(title=_("Visible media?"),
                   description=_("If 'no', this media won't be displayed in front office"),
                   required=True,
                   default=True)


class IGalleryContainer(IOrderedContainer):
    """Base gallery container interface"""

    contains(IGalleryItem)

    def append(self, item, notify=True):
        """Append new file to gallery

        @param item: the media object to append
        @param boolean notify: if 'False', the item value object is pre-located so that adding
            events are not notified
        """

    def get_visible_medias(self):
        """Get iterator over visible medias"""

    def get_visible_images(self):
        """Get iterator over visible images"""


class IBaseGallery(IGalleryContainer, IRenderedContent):
    """Base gallery interface"""

    renderer = Choice(title=_("Gallery renderer"),
                      description=_("Presentation template used for this gallery"),
                      vocabulary=GALLERY_RENDERERS,
                      default='default')


class IGallery(IBaseGallery):
    """Gallery interface"""

    title = I18nTextLineField(title=_("Title"),
                              description=_("Gallery title, as shown in front-office"),
                              required=False)

    description = I18nTextField(title=_("Description"),
                                description=_("Gallery description displayed by front-office "
                                              "template"),
                                required=False)


class IGalleryTarget(IAttributeAnnotatable):
    """Gallery container target marker interface"""


GALLERY_PARAGRAPH_TYPE = 'gallery'
GALLERY_PARAGRAPH_NAME = _("Medias gallery")
GALLERY_PARAGRAPH_RENDERERS = 'PyAMS_content.paragraph.gallery.renderers'
GALLERY_PARAGRAPH_ICON_CLASS = 'fas fa-images'


class IGalleryParagraph(IBaseGallery, IBaseParagraph):
    """Gallery paragraph"""

    renderer = ParagraphRendererChoice(description=_("Presentation template used for gallery"),
                                       renderers=GALLERY_PARAGRAPH_RENDERERS)
