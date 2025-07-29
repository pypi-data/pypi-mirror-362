#
# Copyright (c) 2015-2023 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.component.gallery.portlet module

This module provides a portlet which can be used to display a medias gallery.
"""

from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.gallery import GalleryContainer
from pyams_content.component.gallery.portlet.interfaces import IGalleryPortletSettings
from pyams_portal.portlet import Portlet, PortletSettings, portlet_config
from pyams_utils.factory import factory_config


__docformat__ = 'restructuredtext'

from pyams_content import _


GALLERY_PORTLET_NAME = 'pyams_content.portlet.gallery'
GALLERY_ICON_CLASS = 'fas fa-images'


@factory_config(provided=IGalleryPortletSettings)
class GalleryPortletSettings(GalleryContainer, PortletSettings):
    """Gallery portlet settings"""

    title = FieldProperty(IGalleryPortletSettings['title'])
    use_context_gallery = FieldProperty(IGalleryPortletSettings['use_context_gallery'])


@portlet_config(permission=None)
class GalleryPortlet(Portlet):
    """Medias gallery portlet"""

    name = GALLERY_PORTLET_NAME
    label = _("Medias gallery")

    settings_factory = IGalleryPortletSettings
    toolbar_css_class = GALLERY_ICON_CLASS
