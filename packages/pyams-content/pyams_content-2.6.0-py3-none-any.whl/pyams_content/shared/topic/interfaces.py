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

"""PyAMS_*** module

"""

from zope.schema import Choice

from pyams_content.shared.common.interfaces import ISharedContent, ISharedToolPortalContext, \
    IWfSharedContentPortalContext
from pyams_content.shared.common.interfaces.types import VISIBLE_DATA_TYPES_VOCABULARY
from pyams_sequence.interfaces import IInternalReferencesList

__docformat__ = 'restructuredtext'

from pyams_content import _


TOPIC_CONTENT_TYPE = 'topic'
TOPIC_CONTENT_NAME = _("Topic")


class IWfTopic(IWfSharedContentPortalContext, IInternalReferencesList):
    """Topic interface"""

    data_type = Choice(title=_("Data type"),
                       description=_("Type of content data"),
                       required=False,
                       vocabulary=VISIBLE_DATA_TYPES_VOCABULARY)


class ITopic(ISharedContent):
    """Workflow managed topic interface"""


class ITopicManager(ISharedToolPortalContext):
    """Topic manager interface"""
