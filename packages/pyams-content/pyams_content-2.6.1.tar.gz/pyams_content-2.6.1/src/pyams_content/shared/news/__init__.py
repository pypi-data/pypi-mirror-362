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

"""PyAMS_content.shared.news module

"""

from zope.interface import implementer
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.illustration.interfaces import IIllustrationTarget, \
    ILinkIllustrationTarget
from pyams_content.component.paragraph.interfaces import IParagraphContainerTarget
from pyams_content.component.thesaurus.interfaces import ITagsTarget, IThemesTarget
from pyams_content.feature.preview.interfaces import IPreviewTarget
from pyams_content.feature.review.interfaces import IReviewTarget
from pyams_content.shared.common import SharedContent, WfSharedContent
from pyams_content.shared.common.interfaces import ISharedContent, IWfSharedContent
from pyams_content.shared.news.interfaces import INews, IWfNews, NEWS_CONTENT_NAME, NEWS_CONTENT_TYPE
from pyams_utils.factory import factory_config

__docformat__ = 'restructuredtext'


@factory_config(IWfNews)
@factory_config(IWfSharedContent, name=NEWS_CONTENT_TYPE)
@implementer(IIllustrationTarget, ILinkIllustrationTarget, IParagraphContainerTarget,
             ITagsTarget, IThemesTarget, IReviewTarget, IPreviewTarget)
class WfNews(WfSharedContent):
    """Base news content"""

    content_type = NEWS_CONTENT_TYPE
    content_name = NEWS_CONTENT_NAME
    content_intf = IWfNews
    content_view = True

    references = FieldProperty(IWfNews['references'])


@factory_config(INews)
@factory_config(ISharedContent, name=NEWS_CONTENT_TYPE)
class Topic(SharedContent):
    """Workflow managed news class"""

    content_type = NEWS_CONTENT_TYPE
    content_name = NEWS_CONTENT_NAME
