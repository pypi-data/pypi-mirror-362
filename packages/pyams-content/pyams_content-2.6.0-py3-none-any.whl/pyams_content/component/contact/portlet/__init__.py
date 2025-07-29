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

"""PyAMS_content.component.contact.portlet module

This module defines contact portlet and contact portlet settings persistent class.
"""

from zope.interface import alsoProvides
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.contact.portlet.interfaces import IContactPortletSettings
from pyams_file.interfaces import IImageFile, IResponsiveImage
from pyams_file.property import FileProperty
from pyams_portal.portlet import Portlet, PortletSettings, portlet_config
from pyams_utils.factory import factory_config

__docformat__ = 'restructuredtext'

from pyams_content import _


CONTACT_PORTLET_NAME = 'pyams_content.portlet.contact'


@factory_config(IContactPortletSettings)
class ContactPortletSettings(PortletSettings):
    """Contact portlet settings"""

    title = FieldProperty(IContactPortletSettings['title'])
    name = FieldProperty(IContactPortletSettings['name'])
    charge = FieldProperty(IContactPortletSettings['charge'])
    company = FieldProperty(IContactPortletSettings['company'])
    contact_email = FieldProperty(IContactPortletSettings['contact_email'])
    phone_number = FieldProperty(IContactPortletSettings['phone_number'])
    contact_form = FieldProperty(IContactPortletSettings['contact_form'])
    _photo = FileProperty(IContactPortletSettings['photo'])
    address = FieldProperty(IContactPortletSettings['address'])
    position = FieldProperty(IContactPortletSettings['position'])

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


@portlet_config(permission=None)
class ContactPortlet(Portlet):
    """Contact portlet"""

    name = CONTACT_PORTLET_NAME
    label = _("Contact card")

    settings_factory = IContactPortletSettings
    toolbar_css_class = 'far fa-address-card'
