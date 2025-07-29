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

"""PyAMS_*** module

"""

from pyams_content.component.association import IAssociationContainer, IAssociationContainerTarget
from pyams_content.component.links import EXTERNAL_LINK_ICON_CLASS, IExternalLink, IInternalLink, \
    IMailtoLink, INTERNAL_LINK_ICON_CLASS, MAILTO_LINK_ICON_CLASS
from pyams_content.component.paragraph.zmi import IParagraphContainerFullTable
from pyams_content.component.paragraph.zmi.container import ParagraphTitleToolbarItemMixin
from pyams_content.component.paragraph.zmi.interfaces import IParagraphTitleToolbar
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer


__docformat__ = 'restructuredtext'

from pyams_content import _


@viewlet_config(name='internal-links',
                context=IAssociationContainerTarget, layer=IAdminLayer,
                view=IParagraphContainerFullTable, manager=IParagraphTitleToolbar,
                weight=20)
class InternalLinksTitleToolbarViewlet(ParagraphTitleToolbarItemMixin):
    """Internal links title toolbar viewlet"""

    icon_class = INTERNAL_LINK_ICON_CLASS
    icon_hint = _("Internal links")

    target_intf = IAssociationContainer
    item_intf = IInternalLink


@viewlet_config(name='external-links',
                context=IAssociationContainerTarget, layer=IAdminLayer,
                view=IParagraphContainerFullTable, manager=IParagraphTitleToolbar,
                weight=20)
class ExternalLinksTitleToolbarViewlet(ParagraphTitleToolbarItemMixin):
    """External links title toolbar viewlet"""

    icon_class = EXTERNAL_LINK_ICON_CLASS
    icon_hint = _("External links")

    target_intf = IAssociationContainer
    item_intf = IExternalLink


@viewlet_config(name='mailto-links',
                context=IAssociationContainerTarget, layer=IAdminLayer,
                view=IParagraphContainerFullTable, manager=IParagraphTitleToolbar,
                weight=30)
class MailtoLinksTitleToolbarViewlet(ParagraphTitleToolbarItemMixin):
    """Mailto links title toolbar viewlet"""

    icon_class = MAILTO_LINK_ICON_CLASS
    icon_hint = _("Mailto links")

    target_intf = IAssociationContainer
    item_intf = IMailtoLink
