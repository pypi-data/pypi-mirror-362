#
# Copyright (c) 2015-2023 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.feature.navigation.portlet.interfaces module

This module defines navigation menus portlet interfaces.
"""

from zope.container.constraints import containers, contains
from zope.interface import Attribute, Interface
from zope.schema import Bool, Choice

from pyams_content.component.association import IAssociationContainer, IAssociationContainerTarget
from pyams_content.component.links.interfaces import ILinkContainerTarget
from pyams_content.reference.pictogram.interfaces import SELECTED_PICTOGRAM_VOCABULARY
from pyams_i18n.schema import I18nTextLineField
from pyams_sequence.interfaces import IInternalReference
from pyams_sequence.schema import InternalReferenceField


__docformat__ = 'restructuredtext'

from pyams_content import _


MENU_LINKS_CONTAINER_KEY = 'pyams_content.navigation'


class IMenuLink(Interface):
    """Menu link marker interface"""


class IMenuInternalLink(IMenuLink):
    """Menu internal link marker interface"""


class IMenuExternalLink(IMenuLink):
    """Menu external link marker interface"""


class IMenuMailtoLink(IMenuLink):
    """Menu mailto link marker interface"""


class IDynamicMenu(Interface):
    """Dynamic menu interface

    This interface is used to handle menus whose content is not static, but created
    dynamically based on its target contents.
    """


MENUS_CONTAINER_KEY = 'pyams_content.navigation'


class IMenuLinksContainer(IAssociationContainer):
    """Menu links container interface"""

    contains(IMenuLink)


class IMenuLinksContainerTarget(ILinkContainerTarget):
    """Menu links container target marker interface"""


MENU_ICON_CLASS = 'fas fa-table-list'
MENU_ICON_HINT = _("Navigation menu")


class IMenu(IMenuLinksContainerTarget, IInternalReference):
    """Menu container interface"""

    containers('.IMenusContainer')

    visible = Bool(title=_("Visible?"),
                   description=_("Is this item visible in front-office?"),
                   required=True,
                   default=True)

    def is_visible(self, request=None):
        """Is menu visible?"""

    title = I18nTextLineField(title=_("Menu title"),
                              description=_("Displayed menu label"),
                              required=True)

    reference = InternalReferenceField(title=_("Internal reference"),
                                       description=_("Direct reference to menu target"),
                                       required=False)

    dynamic_menu = Bool(title=_("Dynamic menu?"),
                        description=_("If 'yes', menu items will be built from internal "
                                      "reference navigation items; other static items will be "
                                      "placed after dynamic items"),
                        required=False,
                        default=False)

    force_canonical_url = Bool(title=_("Force canonical URL?"),
                               description=_("If 'yes', link to internal references will "
                                             "use their canonical instead of relative URL"),
                               required=True,
                               default=False)

    pictogram_name = Choice(title=_("Pictogram"),
                            description=_("Name of the pictogram associated with this menu; "
                                          "pictogram display may depend on selected renderer "
                                          "and skin"),
                            required=False,
                            vocabulary=SELECTED_PICTOGRAM_VOCABULARY)

    pictogram = Attribute("Pictogram object reference")

    def get_url(self, request=None, view_name=None):
        """Menu menu target URL"""


class IMenusContainer(IAssociationContainer):
    """Menus container interface"""

    contains(IMenu)


class IMenusContainerTarget(IAssociationContainerTarget):
    """Menus container target marker interface"""
