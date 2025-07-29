#
# Copyright (c) 2015-2023 Thierry Florac <tflorac AT ulthar.net>
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

from zope.interface import Interface
from zope.schema import Choice

from pyams_content.shared.common import ISharedContent
from pyams_content.shared.common.interfaces import ISharedToolPortalContext, \
    IWfSharedContentPortalContext
from pyams_content.shared.common.interfaces.types import VISIBLE_DATA_TYPES_VOCABULARY
from pyams_i18n.schema import I18nTextField, I18nTextLineField
from pyams_sequence.interfaces import IInternalReferencesList


__docformat__ = 'restructuredtext'

from pyams_content import _


class IFormManager(ISharedToolPortalContext):
    """Form manager interface"""


FORM_CONTENT_TYPE = 'form'
FORM_CONTENT_NAME = _("Form")


class IWfForm(IWfSharedContentPortalContext, IInternalReferencesList):
    """Form interface"""

    data_type = Choice(title=_("Data type"),
                       description=_("Type of content data"),
                       required=False,
                       vocabulary=VISIBLE_DATA_TYPES_VOCABULARY)

    alt_title = I18nTextLineField(title=_("Title"),
                                  description=_("If set, this title will be displayed in front-office "
                                                "above header and input fields"),
                                  required=False)

    form_header = I18nTextField(title=_("Header"),
                                description=_("If set, this header is displayed just above input fields"),
                                required=False)

    form_legend = I18nTextLineField(title=_("Legend"),
                                    description=_("If set, this legend will be displayed above input fields"),
                                    required=False)


class IWfFormFactory(Interface):
    """Form parent interface"""


class IForm(ISharedContent):
    """Workflow managed form interface"""


