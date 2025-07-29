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

from pyams_content import _
from pyams_content.component.paragraph import IParagraphContainer, IParagraphContainerTarget
from pyams_content.component.paragraph.interfaces.group import GROUP_PARAGRAPH_ICON_CLASS, GROUP_PARAGRAPH_NAME, \
    GROUP_PARAGRAPH_TYPE, IParagraphsGroup
from pyams_content.component.paragraph.zmi import BaseParagraphAddForm, BaseParagraphAddMenu, \
    IParagraphContainerBaseTable
from pyams_form.ajax import ajax_form_config
from pyams_layer.interfaces import IPyAMSLayer
from pyams_skin.interfaces.viewlet import IContentSuffixViewletManager
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.form import IPropertiesEditForm
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager
from pyams_zmi.table import InnerTableAdminView


@viewlet_config(name='add-group-paragraph.menu',
                context=IParagraphContainerTarget, layer=IAdminLayer,
                view=IParagraphContainerBaseTable,
                manager=IContextAddingsViewletManager, weight=600)
class ParagraphsGroupAddMenu(BaseParagraphAddMenu):
    """Paragraphs group add menu"""

    label = GROUP_PARAGRAPH_NAME
    icon_class = GROUP_PARAGRAPH_ICON_CLASS

    factory_name = GROUP_PARAGRAPH_TYPE
    href = 'add-group-paragraph.html'


@ajax_form_config(name='add-group-paragraph.html',
                  context=IParagraphContainer, layer=IPyAMSLayer)
class ParagraphsGroupAddForm(BaseParagraphAddForm):
    """Paragraphs group add form"""

    content_factory = IParagraphsGroup


@viewlet_config(name='paragraphs-group-table',
                context=IParagraphsGroup, layer=IAdminLayer,
                view=IPropertiesEditForm,
                manager=IContentSuffixViewletManager, weight=10)
class ParagraphsGroupTable(InnerTableAdminView):
    """Paragraphs group table"""
    
    table_class = IParagraphContainerBaseTable
    table_label = _("Group paragraphs list")
    
    container_intf = IParagraphContainer
