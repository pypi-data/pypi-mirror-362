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

"""PyAMS_content.shared.topic module

"""

from zope.interface import implementer
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.illustration.interfaces import IIllustrationTarget, \
    ILinkIllustrationTarget
from pyams_content.component.paragraph.interfaces import IParagraphContainerTarget
from pyams_content.component.thesaurus.interfaces import ITagsTarget, IThemesTarget
from pyams_content.feature.preview.interfaces import IPreviewTarget
from pyams_content.feature.review import IReviewTarget
from pyams_content.shared.common import ISharedContent, IWfSharedContent, SharedContent, \
    WfSharedContent
from pyams_content.shared.common.types import WfTypedSharedContentMixin
from pyams_content.shared.topic.interfaces import ITopic, IWfTopic, TOPIC_CONTENT_NAME, \
    TOPIC_CONTENT_TYPE
from pyams_utils.factory import factory_config


__docformat__ = 'restructuredtext'


@factory_config(IWfTopic)
@factory_config(IWfSharedContent, name=TOPIC_CONTENT_TYPE)
@implementer(IIllustrationTarget, ILinkIllustrationTarget, IParagraphContainerTarget,
             ITagsTarget, IThemesTarget, IReviewTarget, IPreviewTarget)
class WfTopic(WfSharedContent, WfTypedSharedContentMixin):
    """Base topic content"""

    content_type = TOPIC_CONTENT_TYPE
    content_name = TOPIC_CONTENT_NAME
    content_intf = IWfTopic
    content_view = True

    references = FieldProperty(IWfTopic['references'])
    data_type = FieldProperty(IWfTopic['data_type'])


@factory_config(ITopic)
@factory_config(ISharedContent, name=TOPIC_CONTENT_TYPE)
class Topic(SharedContent):
    """Workflow managed topic class"""

    content_type = TOPIC_CONTENT_TYPE
    content_name = TOPIC_CONTENT_NAME
