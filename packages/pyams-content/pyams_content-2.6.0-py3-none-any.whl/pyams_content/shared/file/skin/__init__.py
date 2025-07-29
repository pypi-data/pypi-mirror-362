# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config

from pyams_content.component.file import ProtectedFileView
from pyams_content.shared.file import IWfFile
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_utils.rest import http_error

__docformat__ = 'restructuredtext'


@view_config(context=IWfFile, request_type=IPyAMSLayer)
def render_file(request):
    """Shared file renderer"""
    data = II18n(request.context).query_attribute('data', request=request)
    if data:
        request.context = data
        return ProtectedFileView(request)
    return http_error(request, HTTPNotFound)
