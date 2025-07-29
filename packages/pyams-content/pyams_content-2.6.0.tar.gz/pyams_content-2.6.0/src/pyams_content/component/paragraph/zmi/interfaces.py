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

"""PyAMS_content.component.paragraph.zmi.interfaces module

"""

__docformat__ = 'restructuredtext'

from zope.interface import Interface

from pyams_viewlet.interfaces import IViewletManager


class IParagraphContainerBaseTable(Interface):
    """Paragraph container base table marker interface"""


class IParagraphContainerFullTable(IParagraphContainerBaseTable):
    """Paragraph container table marker interface"""


class IParagraphContainerView(Interface):
    """Paragraph container view marker interface"""


class IParagraphAddForm(Interface):
    """Paragraph add form marker interface"""


class IParagraphEditForm(Interface):
    """Paragraph edit form marker interface"""


class IInnerParagraphEditForm(Interface):
    """Inner paragraph edit form marker interface"""


class IParagraphRendererSettingsEditForm(Interface):
    """Paragraph renderer settings edit form interface"""


class IParagraphTitleToolbar(IViewletManager):
    """Paragraph title toolbar viewlet manager interface"""
