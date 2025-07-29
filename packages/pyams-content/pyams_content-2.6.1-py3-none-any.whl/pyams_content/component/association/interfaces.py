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

"""PyAMS_content.component.association.interfaces module

"""

from zope.annotation import IAttributeAnnotatable
from zope.container.constraints import containers, contains
from zope.container.interfaces import IOrderedContainer
from zope.interface import Attribute, Interface
from zope.schema import Bool, Choice
from pyams_content.component.paragraph.interfaces import IBaseParagraph
from pyams_content.component.paragraph.schema import ParagraphRendererChoice

__docformat__ = 'restructuredtext'

from pyams_content import _


ASSOCIATION_CONTAINER_KEY = 'pyams_content.associations'
ASSOCIATION_VOCABULARY = 'pyams_content.associations'


class IAssociationItem(IAttributeAnnotatable):
    """Base association item interface"""

    containers('.IAssociationContainer')

    icon_class = Attribute("Icon class in associations list")
    icon_hint = Attribute("Icon hint in associations list")

    visible = Bool(title=_("Visible?"),
                   description=_("Is this item visible in front-office?"),
                   required=True,
                   default=True)

    def is_visible(self, request=None):
        """Is association item published?"""

    def get_url(self, request=None, view_name=None):
        """Get link URL"""


class IAssociationInfo(Interface):
    """Association information interface"""

    pictogram = Attribute("Association pictogram")

    user_title = Attribute("Association title proposed on public site")
    user_header = Attribute("Association header proposed on public site")
    user_icon = Attribute("Icon associated with user title")

    inner_title = Attribute("Inner content, if available")
    human_size = Attribute("Content size, if available")


class IAssociationContainer(IOrderedContainer):
    """Associations container interface"""

    contains(IAssociationItem)

    def append(self, value, notify=True):
        """Append given value to container"""

    def get_visible_items(self, request=None):
        """Get list of visible items"""


class IAssociationContainerTarget(IAttributeAnnotatable):
    """Associations container target interface"""


class IAssociationRenderer(Interface):
    """Association renderer adapter interface"""


#
# Associations paragraph
#

ASSOCIATION_PARAGRAPH_TYPE = 'associations'
ASSOCIATION_PARAGRAPH_NAME = _("Associations")
ASSOCIATION_PARAGRAPH_RENDERERS = 'PyAMS_content.paragraph.associations.renderers'
ASSOCIATION_PARAGRAPH_ICON_CLASS = 'fas fa-link'


class IAssociationParagraph(IBaseParagraph):
    """Associations paragraph interface"""

    renderer = ParagraphRendererChoice(description=_("Presentation template used for "
                                                     "associations"),
                                       renderers=ASSOCIATION_PARAGRAPH_RENDERERS)
