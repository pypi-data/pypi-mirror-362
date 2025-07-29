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

"""PyAMS_content.shared.common.skin.workflow module

This module defines a content provider used for shared content publication date rendering.
"""

from babel import Locale, UnknownLocaleError
from babel.dates import format_date
from zope.interface import Interface

from pyams_i18n.interfaces import INegotiator
from pyams_layer.interfaces import IPyAMSUserLayer
from pyams_template.template import template_config
from pyams_utils.registry import get_utility
from pyams_viewlet.viewlet import ViewContentProvider, contentprovider_config
from pyams_workflow.interfaces import IWorkflowPublicationInfo

__docformat__ = 'restructuredtext'


@contentprovider_config(name='pyams_content.publication_date',
                        layer=IPyAMSUserLayer, view=Interface)
@template_config(template='templates/publication-date.pt')
class SharedContentPublicationContentProvider(ViewContentProvider):
    """Shared content publication date content provider"""

    date_format = 'long'

    @property
    def publication_date(self):
        info = IWorkflowPublicationInfo(self.context, None)
        if info is None:
            return ''
        try:
            locale = Locale(self.request.locale_name)
        except UnknownLocaleError:
            negotiator = get_utility(INegotiator)
            locale = Locale(negotiator.server_language)
        return format_date(info.visible_publication_date,
                           format=self.date_format, locale=locale)
