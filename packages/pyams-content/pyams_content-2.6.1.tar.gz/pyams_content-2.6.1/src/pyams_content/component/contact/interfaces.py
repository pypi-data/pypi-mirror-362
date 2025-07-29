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

"""PyAMS_content.component.contact.interfaces module

This module defines base interfaces for contact paragraph or portlet settings.
"""

from zope.interface import Interface
from zope.schema import Text, TextLine

from pyams_content.component.paragraph.interfaces import IBaseParagraph
from pyams_content.component.paragraph.schema import ParagraphRendererChoice
from pyams_content.shared.form import FORM_CONTENT_TYPE
from pyams_file.schema import ImageField
from pyams_gis.schema import GeoPointField
from pyams_i18n.schema import I18nTextLineField
from pyams_sequence.schema import InternalReferenceField
from pyams_utils.schema import MailAddressField

__docformat__ = 'restructuredtext'

from pyams_content import _


CONTACT_PARAGRAPH_TYPE = 'contact'
CONTACT_PARAGRAPH_NAME = _("Contact card")
CONTACT_PARAGRAPH_RENDERERS = 'PyAMS_content.paragraph.contact.renderers'
CONTACT_PARAGRAPH_ICON_CLASS = 'far fa-address-card'


class IContactInfo(Interface):
    """Base contact information interface"""

    name = TextLine(title=_("Contact identity"),
                    description=_("Name of the contact"),
                    required=False)

    charge = I18nTextLineField(title=_("In charge of"),
                               description=_("Label of contact function"),
                               required=False)

    company = TextLine(title=_("Company"),
                       description=_("Business name of the employer"),
                       required=False)

    contact_email = MailAddressField(title=_("Email address"),
                                     description=_("Contact email address"),
                                     required=False)

    phone_number = TextLine(title=_('Phone number'),
                            description=_('Phone number in international format. E.g. +33 ....'),
                            required=False)

    contact_form = InternalReferenceField(title=_("Contact form"),
                                          description=_("Reference of contact form"),
                                          required=False,
                                          content_type=FORM_CONTENT_TYPE)

    photo = ImageField(title=_("Photo"),
                       description=_("Use 'browse' button to select contact picture"),
                       required=False)

    address = Text(title=_("Address"),
                   required=False)

    position = GeoPointField(title=_("Position"),
                             description=_("GPS coordinates used to locate contact"),
                             required=False)


class IContactParagraph(IContactInfo, IBaseParagraph):
    """Contact paragraph interface"""

    renderer = ParagraphRendererChoice(description=_("Presentation template used for this contact card"),
                                       renderers=CONTACT_PARAGRAPH_RENDERERS)
