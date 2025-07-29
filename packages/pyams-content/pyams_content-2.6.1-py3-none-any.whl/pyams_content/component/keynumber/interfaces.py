# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from zope.container.constraints import contains
from zope.container.interfaces import IOrderedContainer
from zope.location.interfaces import IContained
from zope.schema import Bool, TextLine

from pyams_content.component.paragraph import IBaseParagraph
from pyams_content.component.paragraph.schema import ParagraphRendererChoice
from pyams_i18n.schema import I18nTextLineField

__docformat__ = 'restructuredtext'

from pyams_content import _


class IKeyNumberInfo(IContained):
    """Key number info interface"""
    
    visible = Bool(title=_("Visible?"),
                   description=_("Is this key-number visible in front-office?"),
                   required=True,
                   default=True)

    label = I18nTextLineField(title=_('key-number-label', default="Header"),
                              description=_("Small text to be displayed above number (according to selected "
                                            "renderer)"),
                              required=False)

    number = TextLine(title=_("Number"),
                      description=_("Key-number value"),
                      required=False)

    unit = I18nTextLineField(title=_('key-number-unit', default="Unit"),
                             description=_("Displayed unit"),
                             required=False)

    text = I18nTextLineField(title=_("Associated text"),
                             description=_("The way this text will be rendered depends on presentation template"),
                             required=False)


class IKeyNumbersContainer(IOrderedContainer):
    """Key numbers container interface"""
    
    contains(IKeyNumberInfo)
    
    def get_visible_items(self):
        """Get iterator over visible key numbers"""


KEYNUMBERS_PARAGRAPH_TYPE = 'key-numbers'
KEYNUMBERS_PARAGRAPH_NAME = _("Key-numbers")
KEYNUMBERS_PARAGRAPH_RENDERERS = 'PyAMS_content.paragraph.key-numbers.renderers'
KEYNUMBERS_PARAGRAPH_ICON_CLASS = 'fas fa-dashboard'


class IKeyNumbersParagraph(IKeyNumbersContainer, IBaseParagraph):
    """Key number paragraph interface"""
    
    renderer = ParagraphRendererChoice(description=_("Presentation template used for key-numbers"),
                                       renderers=KEYNUMBERS_PARAGRAPH_RENDERERS)
