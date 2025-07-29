# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

import html
from zope.interface import Interface

from pyams_content.feature.search import ISearchFolder
from pyams_content.feature.search.interfaces import ISearchFormRequestParams
from pyams_layer.interfaces import IPyAMSUserLayer
from pyams_utils.adapter import ContextRequestAdapter, ContextRequestViewAdapter, adapter_config
from pyams_utils.interfaces.tales import ITALESExtension

__docformat__ = 'restructuredtext'


@adapter_config(name='search_form_params',
                required=(Interface, Interface, Interface),
                provides=ITALESExtension)
class RequestSearchParamsTALESExtension(ContextRequestViewAdapter):
    """Request search params TALES extension"""

    def render(self, context=None, ignored=None):
        if context is None:
            context = self.context
        if isinstance(ignored, str):
            ignored = ignored.split(',')
        result = []
        for name, adapter in self.request.registry.getAdapters((context, self.request),
                                                               ISearchFormRequestParams):
            if ignored and (name in ignored):
                continue
            for param in adapter.get_params():
                result.append('<input type="hidden"'
                              ' name="{name}"'
                              ' value="{value}" />'.format(name=param.get('name'),
                                                           value=html.escape(param.get('value'))))
        return '\n'.join(result)


@adapter_config(name='user_search',
                context=(ISearchFolder, IPyAMSUserLayer),
                provides=ISearchFormRequestParams)
class SearchFormUserRequestParams(ContextRequestAdapter):
    """User search form request params"""

    def get_params(self):
        yield {
            'name': 'user_search',
            'value': self.request.params.get('user_search', '')
        }
