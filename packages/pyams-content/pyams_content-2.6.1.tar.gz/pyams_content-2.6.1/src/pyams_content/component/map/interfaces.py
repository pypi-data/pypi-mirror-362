# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from zope.interface import Interface

from pyams_content.component.paragraph.interfaces import IBaseParagraph
from pyams_content.component.paragraph.schema import ParagraphRendererChoice
from pyams_gis.schema import GeoPointField

__docformat__ = 'restructuredtext'

from pyams_content import _


MAP_PARAGRAPH_TYPE = 'map'
MAP_PARAGRAPH_NAME = _("Location map")
MAP_PARAGRAPH_RENDERERS = 'PyAMS_content.paragraph.map.renderers'
MAP_PARAGRAPH_ICON_CLASS = 'fas fa-map-marker'


class IMapInfo(Interface):
    """Base map settings interface"""

    position = GeoPointField(title=_("Map position"),
                             description=_("GPS coordinates used to locate map"),
                             required=False)


class IMapParagraph(IMapInfo, IBaseParagraph):
    """Map paragraph interface"""

    renderer = ParagraphRendererChoice(description=_("Presentation template used for this map"),
                                       renderers=MAP_PARAGRAPH_RENDERERS)
