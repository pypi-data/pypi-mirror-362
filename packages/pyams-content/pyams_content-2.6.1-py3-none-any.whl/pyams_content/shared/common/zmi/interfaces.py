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

"""PyAMS_content.shared.common.zmi.interfaces module

This module defines custom interfaces related to management interface
of shared contents.
"""

__docformat__ = 'restructuredtext'

from zope.interface import Interface

from pyams_form.interfaces.form import IAddForm


class ISharedContentAddForm(IAddForm):
    """Shared content add form marker interface"""


class ISharedContentPropertiesMenu(Interface):
    """Shared content properties menu marker interface"""


class IContributorRestrictionsEditForm(Interface):
    """Contributor restrictions edit form marker interface"""


class IManagerRestrictionsEditForm(Interface):
    """Manager restrictions edit form marker interface"""


class IManagerRestrictionsGroup(Interface):
    """Manager restrictions workflow group marker interface"""


class IWorkflowDeleteFormTarget(Interface):
    """Interface used to get target of a workflow delete form"""
