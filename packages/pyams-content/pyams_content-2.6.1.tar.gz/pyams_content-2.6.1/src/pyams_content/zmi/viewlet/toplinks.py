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

"""PyAMS_content.zmi.viewlet.toplinks module

This module provides top-menus viewlets.
"""

from zope.interface import Interface

from pyams_viewlet.manager import viewletmanager_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import ITopLinksViewletManager
from pyams_zmi.zmi.viewlet.toplinks import TopMenusGroupViewletManager


__docformat__ = 'restructuredtext'

from pyams_content import _


@viewletmanager_config(name='top-tabs',
                       context=Interface, layer=IAdminLayer,
                       manager=ITopLinksViewletManager, weight=10)
class TopTabsViewletManager(TopMenusGroupViewletManager):
    """Top tabs viewlet manager"""

    label = _("Shortcuts")
