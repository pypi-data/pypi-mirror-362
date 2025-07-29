# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

__docformat__ = 'restructuredtext'

from pyams_content.component.map.interfaces import IMapParagraph, MAP_PARAGRAPH_ICON_CLASS, MAP_PARAGRAPH_NAME, \
    MAP_PARAGRAPH_TYPE
from pyams_content.component.paragraph.interfaces import IParagraphContainer, IParagraphContainerTarget
from pyams_content.component.paragraph.zmi import BaseParagraphAddForm, BaseParagraphAddMenu
from pyams_content.component.paragraph.zmi.interfaces import IParagraphContainerBaseTable
from pyams_form.ajax import ajax_form_config
from pyams_layer.interfaces import IPyAMSLayer
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager


@viewlet_config(name='add-map-paragraph.menu',
                context=IParagraphContainerTarget, layer=IAdminLayer,
                view=IParagraphContainerBaseTable,
                manager=IContextAddingsViewletManager, weight=600)
class MapParagraphAddMenu(BaseParagraphAddMenu):
    """Map paragraph add menu"""

    label = MAP_PARAGRAPH_NAME
    icon_class = MAP_PARAGRAPH_ICON_CLASS

    factory_name = MAP_PARAGRAPH_TYPE
    href = 'add-map-paragraph.html'


@ajax_form_config(name='add-map-paragraph.html',
                  context=IParagraphContainer, layer=IPyAMSLayer)
class MapParagraphAddForm(BaseParagraphAddForm):
    """Map paragraph add form"""

    content_factory = IMapParagraph
