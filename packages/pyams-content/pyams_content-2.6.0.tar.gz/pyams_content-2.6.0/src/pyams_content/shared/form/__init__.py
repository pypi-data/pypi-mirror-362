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

"""PyAMS_content.shared.form module

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
from pyams_content.shared.form.interfaces import FORM_CONTENT_NAME, FORM_CONTENT_TYPE, \
    IForm, IFormManager, IWfForm
from pyams_fields.interfaces import ICaptchaTarget, IFormFieldContainerTarget, \
    IFormHandlersTarget, IRGPDTarget
from pyams_utils.factory import factory_config


__docformat__ = 'restructuredtext'


@factory_config(IWfForm)
@factory_config(IWfSharedContent, name=FORM_CONTENT_TYPE)
@implementer(IIllustrationTarget, ILinkIllustrationTarget, ICaptchaTarget, IRGPDTarget,
             IFormFieldContainerTarget, IFormHandlersTarget, IParagraphContainerTarget,
             ITagsTarget, IThemesTarget, IReviewTarget, IPreviewTarget)
class WfForm(WfSharedContent, WfTypedSharedContentMixin):
    """Base form"""

    content_type = FORM_CONTENT_TYPE
    content_name = FORM_CONTENT_NAME
    content_intf = IWfForm
    content_view = True

    references = FieldProperty(IWfForm['references'])
    data_type = FieldProperty(IWfForm['data_type'])
    alt_title = FieldProperty(IWfForm['alt_title'])
    form_header = FieldProperty(IWfForm['form_header'])
    form_legend = FieldProperty(IWfForm['form_legend'])


@factory_config(IForm)
@factory_config(ISharedContent, name=FORM_CONTENT_TYPE)
class Form(SharedContent):
    """Workflow managed form class"""

    content_type = FORM_CONTENT_TYPE
    content_name = FORM_CONTENT_NAME
