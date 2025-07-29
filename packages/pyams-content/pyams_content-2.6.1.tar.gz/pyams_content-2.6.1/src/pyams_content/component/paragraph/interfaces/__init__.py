#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.component.paragraph.interfaces module

"""

from zope.annotation import IAttributeAnnotatable
from zope.container.constraints import containers, contains
from zope.container.interfaces import IOrderedContainer
from zope.interface import Attribute, Interface
from zope.schema import Bool, Choice, List, Set

from pyams_content.feature.renderer import IContentRenderer, IRenderedContent
from pyams_i18n.schema import I18nTextLineField


__docformat__ = 'restructuredtext'

from pyams_content import _


PARAGRAPH_CONTAINER_KEY = 'pyams_content.paragraph'


class IBaseParagraph(IRenderedContent, IAttributeAnnotatable):
    """Base paragraph interface"""

    containers('.IParagraphContainer')

    factory_name = Attribute("Paragraph factory name")
    factory_label = Attribute("Paragraph factory label")

    icon_class = Attribute("Icon class in paragraphs list")
    icon_hint = Attribute("Icon hint in paragraphs list")

    secondary = Attribute("Boolean class attribute used to specify if this factory is secondary "
                          "or not; secondary factories are displayed in a separate sub-menu")

    visible = Bool(title=_("Visible?"),
                   description=_("Is this paragraph visible in front-office?"),
                   required=True,
                   default=True)

    anchor = Bool(title=_("Anchor?"),
                  description=_("Is this paragraph a navigation anchor?"),
                  required=True,
                  default=False)

    locked = Bool(title=_("Locked?"),
                  description=_("A locked paragraph can only be removed by a content manager "
                                "or a webmaster"),
                  required=True,
                  default=False)

    title = I18nTextLineField(title=_("§ Title"),
                              required=False)


PARAGRAPH_HIDDEN_FIELDS = ('__parent__', '__name__', 'visible', 'anchor', 'locked', 'renderer')


class IParagraphTitle(Interface):
    """Paragraph title adapter"""


class IParagraphContainer(IOrderedContainer):
    """Paragraphs container"""

    contains(IBaseParagraph)

    def append(self, value):
        """Add given value to container"""

    def get_paragraphs(self, factories):
        """Get paragraphs matching given factories"""

    def get_visible_paragraphs(self, names=None, anchors_only=False, exclude_anchors=False,
                               factories=None, excluded_factories=None, limit=None):
        """Get visible paragraphs matching given arguments"""


CONTENT_PARAGRAPHS_VOCABULARY = 'pyams_content.paragraphs'


class IParagraphContainerTarget(IAttributeAnnotatable):
    """Paragraphs container marker interface"""


#
# Paragraph factory settings
#

PARAGRAPH_FACTORIES_VOCABULARY = 'pyams_content.paragraph.factories'

PARAGRAPH_FACTORY_SETTINGS_KEY = 'pyams_content.paragraph.settings'


class IParagraphFactorySettings(Interface):
    """Paragraph factory settings interface

    This interface is used to defined default auto-created paragraphs
    for a given shared tool."""

    allowed_paragraphs = Set(title=_("Allowed paragraphs"),
                             description=_("List of paragraphs allowed for this content type; if selection is empty, "
                                           "all paragraphs types will be allowed"),
                             required=False,
                             value_type=Choice(vocabulary=PARAGRAPH_FACTORIES_VOCABULARY))

    auto_created_paragraphs = List(title=_("Default paragraphs types"),
                                   description=_("Empty paragraphs of these types will be added "
                                                 "automatically to new contents of this content "
                                                 "type; if paragraphs are associated to content type, these will "
                                                 "be used instead of these ones"),
                                   required=False,
                                   value_type=Choice(vocabulary=PARAGRAPH_FACTORIES_VOCABULARY))


class IParagraphFactorySettingsTarget(Interface):
    """Paragraph factory settings target interface"""


#
# Paragraphs renderers
#

DEFAULT_PARAGRAPH_RENDERER_NAME = 'default'


class IParagraphRenderer(IContentRenderer):
    """Paragraph renderer interface"""
