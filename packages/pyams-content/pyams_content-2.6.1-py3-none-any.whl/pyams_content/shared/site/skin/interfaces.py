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

from zope.interface import Interface


class ISiteContainerSummaryView(Interface):
    """Site container summary view marker interface"""


class ISiteContainerSummaryPanelsView(ISiteContainerSummaryView):
    """Site container summary panels view marker interface"""


class ISiteContainerSummaryCardsView(ISiteContainerSummaryView):
    """Site container summary cards view marker interface"""
