#
# Copyright (c) 2015-2022 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.component.association.zmi.paragraph module

"""

from pyams_content.component.association.interfaces import ASSOCIATION_PARAGRAPH_ICON_CLASS, \
    ASSOCIATION_PARAGRAPH_NAME, ASSOCIATION_PARAGRAPH_TYPE, IAssociationParagraph
from pyams_content.component.paragraph import IParagraphContainer, IParagraphContainerTarget
from pyams_content.component.paragraph.zmi import BaseParagraphAddForm, BaseParagraphAddMenu, \
    IParagraphContainerBaseTable
from pyams_form.ajax import ajax_form_config
from pyams_layer.interfaces import IPyAMSLayer
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager


__docformat__ = 'restructuredtext'


@viewlet_config(name='add-association-paragraph.menu',
                context=IParagraphContainerTarget, layer=IAdminLayer,
                view=IParagraphContainerBaseTable,
                manager=IContextAddingsViewletManager, weight=90)
class AssociationParagraphAddMenu(BaseParagraphAddMenu):
    """Association paragraph add menu"""

    label = ASSOCIATION_PARAGRAPH_NAME
    icon_class = ASSOCIATION_PARAGRAPH_ICON_CLASS

    factory_name = ASSOCIATION_PARAGRAPH_TYPE
    href = 'add-association-paragraph.html'


@ajax_form_config(name='add-association-paragraph.html',
                  context=IParagraphContainer, layer=IPyAMSLayer)
class AssociationParagraphAddForm(BaseParagraphAddForm):
    """Association paragraph add form"""

    content_factory = IAssociationParagraph
