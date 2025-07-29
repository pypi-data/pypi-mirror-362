#
# Copyright (c) 2015-2024 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.feature.redirect.handler module

This module defines the main handler of NotFound exceptions, which is used
to redirect request based on defined redirection rules.
"""

from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import Response
from pyramid.view import notfound_view_config

from pyams_content.feature.redirect.interfaces import IRedirectionManager
from pyams_layer.interfaces import IPyAMSLayer

__docformat__ = 'restructuredtext'


@notfound_view_config(request_type=IPyAMSLayer)
def notfound_handler(request):
    """NotFound exception handler"""
    manager = IRedirectionManager(request.root, None)
    if manager is not None:
        response = manager.get_response(request)
        if response is not None:
            return response
    return Response(status=HTTPNotFound.code)
