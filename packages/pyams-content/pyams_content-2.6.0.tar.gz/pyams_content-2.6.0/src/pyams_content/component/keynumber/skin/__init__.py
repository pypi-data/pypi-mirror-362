# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from pyams_content.component.keynumber import IKeyNumbersParagraph
from pyams_content.feature.renderer import BaseContentRenderer, IContentRenderer
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import DEFAULT_RENDERER_NAME
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config

__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(name=DEFAULT_RENDERER_NAME,
                required=(IKeyNumbersParagraph, IPyAMSLayer),
                provides=IContentRenderer)
@template_config(template='templates/key-numbers-default.pt',
                 layer=IPyAMSLayer)
class KeyNumbersParagraphDefaultRenderer(BaseContentRenderer):
    """Key numbers paragraph default renderer"""
    
    label = _("Horizontal cards list (default)")
    weight = 10
    
    
@adapter_config(name='vertical',
                required=(IKeyNumbersParagraph, IPyAMSLayer),
                provides=IContentRenderer)
@template_config(template='templates/key-numbers-vertical.pt',
                 layer=IPyAMSLayer)
class KeyNumbersParagraphVerticalRenderer(BaseContentRenderer):
    """Key numbers paragraph vertical renderer"""
    
    label = _("Vertical cards list")
    weight = 20
