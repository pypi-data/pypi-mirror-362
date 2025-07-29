# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.component.contact.skin.interfaces module

This module defines base interfaces of contact renderer settings.
"""

from zope.interface import Attribute
from zope.schema import Bool, Choice
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_content.feature.renderer.interfaces import IRendererSettings
from pyams_gis.interfaces.configuration import IMapConfiguration
from pyams_i18n.schema import I18nTextLineField

__docformat__ = 'restructuredtext'

from pyams_content import _


CONTENT_POSITIONS = (
    {'id': 'left', 'title': _("Left")},
    {'id': 'right', 'title': _("Right")}
)

CONTENT_POSITIONS_VOCABULARY = SimpleVocabulary([
    SimpleTerm(item['id'], title=item['title'])
    for item in CONTENT_POSITIONS
])


class IBaseContactRendererSettings(IMapConfiguration):
    """Contact base renderer settings interface"""

    link_label = I18nTextLineField(title=_("Button label"),
                                   description=_("Label of the button used to get access to contact form"),
                                   required=False)

    can_display_link = Attribute("Check if link to contact form can be displayed")

    display_photo = Bool(title=_("Show photo?"),
                         description=_("Display contact photo"),
                         required=True,
                         default=True)

    photo_position = Choice(title=_("Photo position"),
                            required=False,
                            vocabulary=CONTENT_POSITIONS_VOCABULARY,
                            default='left')

    can_display_photo = Attribute("Check if photo can be displayed")

    display_map = Bool(title=_("Show location map?"),
                       description=_("If 'no', location map will not be displayed"),
                       required=True,
                       default=True)

    map_position = Choice(title=_("Map position"),
                          required=False,
                          vocabulary=CONTENT_POSITIONS_VOCABULARY,
                          default='right')

    display_marker = Bool(title=_("Display location mark?"),
                          description=_("If 'yes', a location marker will be displayed on map"),
                          required=True,
                          default=True)

    display_coordinates = Bool(title=_("Display coordinates?"),
                               description=_("If 'yes', GPS coordinates (if GPS position "
                                             "is defined) will be displayed below the map"),
                               required=True,
                               default=False)

    no_use_default_map_configuration = Bool(title=_("Don't use default configuration?"),
                                            required=True,
                                            default=False)

    use_default_map_configuration = Bool(title=_("Use default configuration?"),
                                         required=True,
                                         default=True)

    configuration = Attribute("Map configuration")

    can_display_map = Attribute("Check if location map can be displayed")


class IContactDefaultRendererSettings(IRendererSettings, IBaseContactRendererSettings):
    """Contact default renderer settings"""
