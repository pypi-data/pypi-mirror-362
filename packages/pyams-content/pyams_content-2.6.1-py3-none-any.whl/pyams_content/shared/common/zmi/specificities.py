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
from pyams_content.shared.common.interfaces import ISpecificitiesParagraph, SPECIFICITIES_PARAGRAPH_ICON_CLASS, \
    SPECIFICITIES_PARAGRAPH_NAME, SPECIFICITIES_PARAGRAPH_TYPE
from pyams_form.ajax import ajax_form_config
from pyams_layer.interfaces import IPyAMSLayer
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager

__docformat__ = 'restructuredtext'


@viewlet_config(name='add-specificities-paragraph.menu',
                context=IParagraphContainerTarget, layer=IAdminLayer,
                view=IParagraphContainerBaseTable,
                manager=IContextAddingsViewletManager, weight=600)
class SpecificitiesParagraphAddMenu(BaseParagraphAddMenu):
    """Specificities paragraph add menu"""

    label = SPECIFICITIES_PARAGRAPH_NAME
    icon_class = SPECIFICITIES_PARAGRAPH_ICON_CLASS

    factory_name = SPECIFICITIES_PARAGRAPH_TYPE
    href = 'add-specificities-paragraph.html'


@ajax_form_config(name='add-specificities-paragraph.html',
                  context=IParagraphContainer, layer=IPyAMSLayer)
class SpecificitiesParagraphAddForm(BaseParagraphAddForm):
    """Specificities paragraph add form"""

    content_factory = ISpecificitiesParagraph
