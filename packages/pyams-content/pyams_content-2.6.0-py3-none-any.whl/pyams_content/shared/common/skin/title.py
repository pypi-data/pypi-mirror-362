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

"""PyAMS_content.shared.common.skin.title module

This module defines components which are used for shared contents title rendering.
"""

from zope.interface import Interface

from pyams_content.interfaces import IBaseContent
from pyams_content.skin.interfaces import IContentTitle
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSUserLayer
from pyams_utils.adapter import adapter_config
from pyams_viewlet.viewlet import ViewContentProvider, contentprovider_config

__docformat__ = 'restructuredtext'


@adapter_config(required=(IBaseContent, IPyAMSUserLayer, Interface),
                provides=IContentTitle)
def base_content_title(context, request, view):
    """Base content title adapter"""
    return II18n(context).query_attribute('title', request=request)


@contentprovider_config(name='pyams_content.title',
                        layer=IPyAMSUserLayer, view=Interface)
class SharedContentTitleContentProvider(ViewContentProvider):
    """Shared content title content provider"""

    def render(self, template_name=''):
        return self.request.registry.queryMultiAdapter((self.context, self.request, self.view),
                                                       IContentTitle) or ''
