#
# Copyright (c) 2015-2024 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.feature.script.zmi.interfaces module

This module defines custom interfaces for scripts management components.
"""

from zope.interface import Interface

__docformat__ = 'restructuredtext'


class IScriptContainerNavigationMenu(Interface):
    """Script container navigation menu interface"""


class IScriptContainerTable(Interface):
    """Script container table marker interface"""
