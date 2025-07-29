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

"""PyAMS_content.component.cards.skin module

This module defines renderers of Bootstrap cards paragraphs.
"""

from pyams_content.component.cards import ICardsParagraph
from pyams_content.component.cards.skin.interfaces import ICardsParagraphDefaultRendererSettings, \
    ICardsParagraphMasonryRendererSettings
from pyams_content.feature.renderer import BaseContentRenderer, IContentRenderer
from pyams_portal.interfaces import DEFAULT_RENDERER_NAME
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.portlets.cards.skin import CardsPortletMasonryRendererSettings, CardsPortletRendererSettings
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_utils.factory import factory_config


__docformat__ = 'restructuredtext'

from pyams_content import _


@factory_config(ICardsParagraphDefaultRendererSettings)
class CardsParagraphDefaultRendererSettings(CardsPortletRendererSettings):
    """Cards paragraph default renderer settings"""


@adapter_config(name=DEFAULT_RENDERER_NAME,
                required=(ICardsParagraph, IPyAMSLayer),
                provides=IContentRenderer)
@template_config(template='templates/cards.pt',
                 layer=IPyAMSLayer)
class CardsParagraphDefaultRenderer(BaseContentRenderer):
    """Cards paragraph default renderer"""

    label = _("Bootstrap cards renderer (default)")

    settings_interface = ICardsParagraphDefaultRendererSettings
    weight = 10


@factory_config(ICardsParagraphMasonryRendererSettings)
class CardsParagraphMasonryRendererSettings(CardsPortletMasonryRendererSettings):
    """Cards paragraph Masonry renderer settings"""


@adapter_config(name='cards::masonry',
                required=(ICardsParagraph, IPyAMSLayer),
                provides=IContentRenderer)
@template_config(template='templates/cards-masonry.pt',
                 layer=IPyAMSLayer)
class CardsParagraphMasonryRenderer(BaseContentRenderer):
    """Cards paragraph masonry renderer"""

    label = _("Bootstrap cards Masonry renderer")

    settings_interface = ICardsParagraphMasonryRendererSettings
    weight = 20
