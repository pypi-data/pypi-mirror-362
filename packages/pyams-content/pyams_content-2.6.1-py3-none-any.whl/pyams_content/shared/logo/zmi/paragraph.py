# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from pyams_content.component.paragraph import IParagraphContainer, IParagraphContainerTarget
from pyams_content.component.paragraph.zmi import BaseParagraphAddForm, BaseParagraphAddMenu, \
    IParagraphContainerBaseTable
from pyams_content.shared.logo.interfaces import ILogosParagraph, LOGOS_PARAGRAPH_ICON_CLASS, LOGOS_PARAGRAPH_NAME, \
    LOGOS_PARAGRAPH_TYPE
from pyams_form.ajax import ajax_form_config
from pyams_layer.interfaces import IPyAMSLayer
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager

__docformat__ = 'restructuredtext'


@viewlet_config(name='add-logos-paragraph.menu',
                context=IParagraphContainerTarget, layer=IAdminLayer,
                view=IParagraphContainerBaseTable,
                manager=IContextAddingsViewletManager, weight=600)
class LogosParagraphAddMenu(BaseParagraphAddMenu):
    """Logos paragraph add menu"""

    label = LOGOS_PARAGRAPH_NAME
    icon_class = LOGOS_PARAGRAPH_ICON_CLASS

    factory_name = LOGOS_PARAGRAPH_TYPE
    href = 'add-logos-paragraph.html'


@ajax_form_config(name='add-logos-paragraph.html',
                  context=IParagraphContainer, layer=IPyAMSLayer)
class LogosParagraphAddForm(BaseParagraphAddForm):
    """Logos paragraph add form"""

    content_factory = ILogosParagraph
