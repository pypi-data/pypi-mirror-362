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

"""PyAMS_content.component.extfile.interfaces module

This module defines interfaces which are used to handle external files.
"""

from zope.interface import Interface
from zope.schema import Choice, TextLine

from pyams_content.component.association import IAssociationContainerTarget, IAssociationItem
from pyams_file.schema import I18nAudioField, I18nFileField, I18nThumbnailImageField, \
    I18nVideoField
from pyams_i18n.interfaces import BASE_LANGUAGES_VOCABULARY_NAME
from pyams_i18n.schema import I18nTextField, I18nTextLineField


__docformat__ = 'restructuredtext'

from pyams_content import _


EXTFILE_CONTAINER_KEY = 'pyams_content.extfile'
EXTFILE_LINKS_CONTAINER_KEY = 'pyams_content.extfile.links'

EXTFILE_FACTORIES_VOCABULARY = 'pyams_content.extfile.factories'


class IBaseExtFile(IAssociationItem):
    """Base external file interface"""

    title = I18nTextLineField(title=_("Download link label"),
                              description=_("Label of download link, as shown in front-office"),
                              required=False)

    description = I18nTextField(title=_("Description"),
                                description=_("File description displayed by front-office "
                                              "template"),
                                required=False)

    author = TextLine(title=_("Author"),
                      description=_("Name of document's author"),
                      required=False)

    language = Choice(title=_("Language"),
                      description=_("File's content language"),
                      vocabulary=BASE_LANGUAGES_VOCABULARY_NAME,
                      required=False)

    filename = TextLine(title=_("Save file as..."),
                        description=_("Name under which the file will be saved"),
                        required=False)


EXTFILE_ICON_CLASS = 'far fa-file-alt'
EXTFILE_ICON_HINT = _("Standard file")


class IExtFile(IBaseExtFile):
    """Generic external file interface"""

    data = I18nFileField(title=_("File data"),
                         description=_("File content"),
                         required=True)


class IExtMedia(IExtFile):
    """External media file interface"""


EXTIMAGE_ICON_CLASS = 'far fa-image'
EXTIMAGE_ICON_HINT = _("External image")


class IExtImage(IExtMedia):
    """External image file interface"""

    data = I18nThumbnailImageField(title=_("Image data"),
                                   description=_("Image content"),
                                   required=True)


EXTVIDEO_ICON_CLASS = 'fas fa-film'
EXTVIDEO_ICON_HINT = _("Video")


class IExtVideo(IExtMedia):
    """External video file interface"""

    data = I18nVideoField(title=_("Video data"),
                          description=_("Video content"),
                          required=True)


EXTAUDIO_ICON_CLASS = 'fas fa-headphones'
EXTAUDIO_ICON_HINT = _("Audio file")


class IExtAudio(IExtMedia):
    """External audio file interface"""

    data = I18nAudioField(title=_("Audio data"),
                          description=_("Audio file content"),
                          required=True)


class IExtFileContainerTarget(IAssociationContainerTarget):
    """External files container marker interface"""


#
# External files management
#

EXTFILE_MANAGER_INFO_KEY = 'pyams_content.extfile.manager'


class IExtFileManagerInfo(Interface):
    """External file manager interface"""

    default_title_prefix = I18nTextLineField(title=_("Default title prefix"),
                                             description=_("If used, this prefix will be "
                                                           "automatically added to download "
                                                           "link's label of all files"),
                                             required=False)


class IExtFileManagerTarget(Interface):
    """External files manager target interface"""
