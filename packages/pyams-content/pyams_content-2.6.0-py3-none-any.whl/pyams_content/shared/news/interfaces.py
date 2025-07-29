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

"""PyAMS_content.shared.news.interfaces module

"""

from pyams_content.shared.common.interfaces import ISharedContent, ISharedToolPortalContext, \
    IWfSharedContentPortalContext
from pyams_sequence.interfaces import IInternalReferencesList

__docformat__ = 'restructuredtext'

from pyams_content import _


NEWS_CONTENT_TYPE = 'news'
NEWS_CONTENT_NAME = _("News")


class IWfNews(IWfSharedContentPortalContext, IInternalReferencesList):
    """News interface"""


class INews(ISharedContent):
    """Workflow managed news interface"""


class INewsManager(ISharedToolPortalContext):
    """News manager interface"""
