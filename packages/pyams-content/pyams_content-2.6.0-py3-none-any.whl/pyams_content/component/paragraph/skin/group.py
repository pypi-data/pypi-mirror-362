# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from pyams_content.component.paragraph import IParagraphContainer
from pyams_content.component.paragraph.interfaces.group import IParagraphsGroup
from pyams_content.feature.renderer import BaseContentRenderer, IContentRenderer
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import DEFAULT_RENDERER_NAME
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_utils.list import is_not_none

__docformat__ = 'restructuredtext'

from pyams_content import _


class BaseParagraphsGroupRenderer(BaseContentRenderer):
    """Base paragraphs group renderer"""
    
    renderers = ()
    
    def get_paragraphs(self):
        container = IParagraphContainer(self.context, None)
        if container is not None:
            yield from container.get_visible_paragraphs()

    def update(self):
        super().update()
        renderers = [
            paragraph.get_renderer(self.request)
            for paragraph in self.get_paragraphs()
        ]
        self.renderers = tuple(filter(is_not_none, renderers))
        [renderer.update() for renderer in self.renderers]
    
    
@adapter_config(name=DEFAULT_RENDERER_NAME,
                required=(IParagraphsGroup, IPyAMSLayer),
                provides=IContentRenderer)
@template_config(template="templates/group-default.pt", layer=IPyAMSLayer)
@template_config(name='group:tab',
                 template='templates/group-default-tab.pt', layer=IPyAMSLayer)
class ParagraphsGroupDefaultRenderer(BaseParagraphsGroupRenderer):
    """Paragraphs group default renderer"""
    
    label = _("Simple paragraphs list (default)")
    weight = 10
    
    
@adapter_config(name='tabs-horizontal',
                required=(IParagraphsGroup, IPyAMSLayer),
                provides=IContentRenderer)
@template_config(template='templates/group-tabs-horizontal.pt', layer=IPyAMSLayer)
@template_config(name='group:tab',
                 template='templates/group-tabs-horizontal-tab.pt', layer=IPyAMSLayer)
class ParagraphsGroupsHorizontalTabsRenderer(BaseParagraphsGroupRenderer):
    """Paragraphs group horizontal tabs renderer"""
    
    label = _("Horizontal tabs")
    weight = 20

    
@adapter_config(name='tabs-vertical',
                required=(IParagraphsGroup, IPyAMSLayer),
                provides=IContentRenderer)
@template_config(template='templates/group-tabs-vertical.pt', layer=IPyAMSLayer)
@template_config(name='group:tab',
                 template='templates/group-tabs-vertical-tab.pt', layer=IPyAMSLayer)
class ParagraphsGroupsVerticalTabsRenderer(BaseParagraphsGroupRenderer):
    """Paragraphs group vertical tabs renderer"""
    
    label = _("Vertical tabs")
    weight = 30
