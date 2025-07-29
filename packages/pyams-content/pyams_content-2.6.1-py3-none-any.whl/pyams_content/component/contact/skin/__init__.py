# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.component.contact.skin module

This module defines contact paragraph renderer and renderer settings.
"""

import json
from urllib.parse import quote
from zope.interface import implementer
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.contact.interfaces import IContactInfo, IContactParagraph
from pyams_content.component.contact.skin.interfaces import IBaseContactRendererSettings, \
    IContactDefaultRendererSettings
from pyams_content.feature.renderer import DefaultContentRenderer, IContentRenderer
from pyams_gis.configuration import MapConfiguration
from pyams_gis.interfaces.configuration import IMapConfiguration
from pyams_gis.interfaces.utility import IMapManager
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import DEFAULT_RENDERER_NAME
from pyams_sequence.reference import get_reference_target
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_utils.dict import update_dict
from pyams_utils.factory import factory_config
from pyams_utils.registry import get_utility
from pyams_utils.request import check_request

__docformat__ = 'restructuredtext'

from pyams_content import _


@implementer(IBaseContactRendererSettings)
class BaseContactRendererSettings(MapConfiguration):
    """Contact default renderer settings"""

    display_photo = FieldProperty(IBaseContactRendererSettings['display_photo'])
    photo_position = FieldProperty(IBaseContactRendererSettings['photo_position'])
    display_map = FieldProperty(IBaseContactRendererSettings['display_map'])
    map_position = FieldProperty(IBaseContactRendererSettings['map_position'])
    display_marker = FieldProperty(IBaseContactRendererSettings['display_marker'])
    display_coordinates = FieldProperty(IBaseContactRendererSettings['display_coordinates'])
    use_default_map_configuration = FieldProperty(IBaseContactRendererSettings['use_default_map_configuration'])
    link_label = FieldProperty(IBaseContactRendererSettings['link_label'])

    @property
    def no_use_default_map_configuration(self):
        return not bool(self.use_default_map_configuration)
    
    @no_use_default_map_configuration.setter
    def no_use_default_map_configuration(self, value):
        self.use_default_map_configuration = not bool(value)
        
    @property
    def configuration(self):
        if self.use_default_map_configuration:
            manager = get_utility(IMapManager)
            return IMapConfiguration(manager)
        return self

    def get_marker(self, context):
        """Marker position getter"""
        if self.display_marker and context.position:
            coordinates = context.position.wgs_coordinates
            return {
                'lon': float(coordinates['longitude']),
                'lat': float(coordinates['latitude'])
            }

    def get_map_configuration(self, context):
        configuration = self.configuration.get_configuration()
        update_dict(configuration, 'marker', self.get_marker(context))
        return json.dumps(configuration)


@factory_config(IContactDefaultRendererSettings)
class ContactDefaultRendererSettings(BaseContactRendererSettings):
    """Contact default renderer settings"""

    @property
    def can_display_link(self):
        contact = IContactInfo(self.__parent__, None)
        return (contact is not None) and contact.contact_form

    @property
    def email_url(self):
        name = self.__parent__.name
        if name:
            return 'mailto:{}'.format(quote('{} <{}>'.format(name, self.__parent__.contact_email)))
        return 'mailto:{}'.format(self.__parent__.contact_email)

    @property
    def contact_form_target(self):
        return get_reference_target(self.__parent__.contact_form)

    @property
    def contact_link_label(self):
        request = check_request()
        label = II18n(self).query_attribute('link_label', request=request)
        if not label:
            label = request.localizer.translate(_("contact-button-label", default="Contact"))
        return label

    @property
    def can_display_photo(self):
        if not self.display_photo:
            return None
        contact = IContactInfo(self.__parent__, None)
        return (contact is not None) and contact.photo

    @property
    def can_display_map(self):
        if not self.display_map:
            return None
        contact = IContactInfo(self.__parent__, None)
        return (contact is not None) and contact.position

    
@adapter_config(name=DEFAULT_RENDERER_NAME,
                required=(IContactParagraph, IPyAMSLayer),
                provides=IContentRenderer)
@template_config(template='templates/contact-default.pt',
                 layer=IPyAMSLayer)
class ContactParagraphDefaultRenderer(DefaultContentRenderer):
    """Contact paragraph default renderer"""
    
    label = _("Simple contact renderer (default)")
    
    settings_interface = IContactDefaultRendererSettings
