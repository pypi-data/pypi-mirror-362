#
# Copyright (c) 2015-2024 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.component.contact module

This module defines contact paragraph persistent class.
"""

from zope.interface import alsoProvides
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.contact.interfaces import CONTACT_PARAGRAPH_ICON_CLASS, CONTACT_PARAGRAPH_NAME, \
    CONTACT_PARAGRAPH_RENDERERS, CONTACT_PARAGRAPH_TYPE, IContactParagraph
from pyams_content.component.paragraph import BaseParagraph
from pyams_content.component.paragraph.interfaces import IBaseParagraph
from pyams_content.feature.renderer import RenderersVocabulary
from pyams_file.interfaces import IImageFile, IResponsiveImage
from pyams_file.property import FileProperty
from pyams_gis.schema import GeoPointField
from pyams_utils.factory import factory_config
from pyams_utils.vocabulary import vocabulary_config

__docformat__ = 'restructuredtext'


@factory_config(IContactParagraph)
@factory_config(IBaseParagraph, name=CONTACT_PARAGRAPH_TYPE)
class ContactParagraph(BaseParagraph):
    """Contact paragraph persistent class"""

    factory_name = CONTACT_PARAGRAPH_TYPE
    factory_label = CONTACT_PARAGRAPH_NAME
    factory_intf = IContactParagraph

    icon_class = CONTACT_PARAGRAPH_ICON_CLASS
    secondary = True

    name = FieldProperty(IContactParagraph['name'])
    charge = FieldProperty(IContactParagraph['charge'])
    company = FieldProperty(IContactParagraph['company'])
    contact_email = FieldProperty(IContactParagraph['contact_email'])
    phone_number = FieldProperty(IContactParagraph['phone_number'])
    contact_form = FieldProperty(IContactParagraph['contact_form'])
    _photo = FileProperty(IContactParagraph['photo'])
    address = FieldProperty(IContactParagraph['address'])
    position = FieldProperty(IContactParagraph['position'])

    @property
    def photo(self):
        return self._photo

    @photo.setter
    def photo(self, value):
        self._photo = value
        if IImageFile.providedBy(self._photo):
            alsoProvides(self._photo, IResponsiveImage)

    @photo.deleter
    def photo(self):
        del self._photo


@vocabulary_config(name=CONTACT_PARAGRAPH_RENDERERS)
class ContactParagraphRenderersVocabulary(RenderersVocabulary):
    """Contact paragraph renderers vocabulary"""

    content_interface = IContactParagraph
