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

"""PyAMS_content.shared.site.topic module

"""

from zope.interface import implementer
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.illustration import IIllustrationTarget, ILinkIllustrationTarget
from pyams_content.component.paragraph.interfaces import IParagraphContainerTarget
from pyams_content.component.thesaurus import ITagsTarget, IThemesTarget
from pyams_content.feature.preview.interfaces import IPreviewTarget
from pyams_content.feature.review import IReviewTarget
from pyams_content.shared.common import ISharedContent, SharedContent, WfSharedContent
from pyams_content.shared.common.interfaces import IWfSharedContent
from pyams_content.shared.common.types import WfTypedSharedContentMixin
from pyams_content.shared.site.interfaces import ISiteTopic, IWfSiteTopic, \
    SITE_TOPIC_CONTENT_NAME, SITE_TOPIC_CONTENT_TYPE
from pyams_portal.interfaces import IPortalContext, IPortalFooterContext, IPortalHeaderContext
from pyams_utils.factory import factory_config
from pyams_workflow.interfaces import IWorkflow, IWorkflowState, IWorkflowVersions


__docformat__ = 'restructuredtext'


@factory_config(IWfSiteTopic)
@factory_config(IWfSharedContent, name=SITE_TOPIC_CONTENT_TYPE)
@implementer(IIllustrationTarget, ILinkIllustrationTarget,
             IParagraphContainerTarget, ITagsTarget, IThemesTarget,
             IPortalContext, IPortalHeaderContext, IPortalFooterContext,
             IReviewTarget, IPreviewTarget)
class WfSiteTopic(WfSharedContent, WfTypedSharedContentMixin):
    """Base site topic"""

    content_type = SITE_TOPIC_CONTENT_TYPE
    content_name = SITE_TOPIC_CONTENT_NAME
    content_intf = IWfSiteTopic
    content_view = True

    references = FieldProperty(IWfSiteTopic['references'])
    data_type = FieldProperty(IWfSiteTopic['data_type'])


@factory_config(ISiteTopic)
@factory_config(ISharedContent, name=SITE_TOPIC_CONTENT_TYPE)
class SiteTopic(SharedContent):
    """Workflow managed topic class"""

    content_type = SITE_TOPIC_CONTENT_TYPE
    content_name = SITE_TOPIC_CONTENT_NAME

    def is_deletable(self):
        """Topic deletion checker"""
        workflow = IWorkflow(self)
        for version in IWorkflowVersions(self).get_versions():
            if IWorkflowState(version).state != workflow.initial_state:
                return False
        return True
