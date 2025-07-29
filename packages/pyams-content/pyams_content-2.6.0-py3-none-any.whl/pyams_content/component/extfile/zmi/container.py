# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from cgi import FieldStorage

from pyramid.httpexceptions import HTTPForbidden, HTTPServerError
from pyramid.view import view_config
from zope.schema.interfaces import WrongType

from pyams_content.component.association import IAssociationContainer, IAssociationContainerTarget
from pyams_content.component.association.zmi import IAssociationsTable
from pyams_content.component.extfile import IExtFile
from pyams_content.component.paragraph.zmi import get_json_paragraph_toolbar_refresh_event
from pyams_file.file import get_magic_content_type
from pyams_file.interfaces.archive import IArchiveExtractor
from pyams_i18n.interfaces import INegotiator
from pyams_layer.interfaces import IPyAMSLayer
from pyams_layer.skin import apply_skin
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_utils.factory import create_object
from pyams_utils.registry import get_utility, query_utility
from pyams_utils.rest import http_error
from pyams_zmi.helper.event import get_json_table_refresh_callback
from pyams_zmi.skin import AdminSkin

__docformat__ = 'restructuredtext'


@view_config(name='upload-external-files.json',
             context=IAssociationContainerTarget, request_type=IPyAMSLayer,
             request_method='POST', renderer='json', xhr=True, require_csrf=False)
def upload_external_files(request):
    """Upload external files"""
    container = IAssociationContainer(request.context)
    permission_checker = IViewContextPermissionChecker(container, None)
    if permission_checker is None:
        return http_error(request, HTTPServerError, "Missing context permission")
    if not request.has_permission(permission_checker.edit_permission, context=container):
        return http_error(request, HTTPForbidden)
    negotiator = get_utility(INegotiator)
    default_lang = negotiator.server_language
    for name in request.params.keys():
        input_file = request.params.get(name)
        if isinstance(input_file, FieldStorage):
            value = input_file.value
            content_type = get_magic_content_type(value)
            extractor = query_utility(IArchiveExtractor, name=content_type)
            if extractor is not None:
                contents = extractor.get_contents(value)
            else:
                contents = ((value, input_file.filename),)
            for content, filename in contents:
                try:
                    external_file = create_object(IExtFile)
                    container.append(external_file)
                    external_file.data = {
                        default_lang: (filename, content)
                    }
                    external_file.filename = filename
                except WrongType:
                    continue
    apply_skin(request, AdminSkin)
    result = {
        'status': 'success',
        'callbacks': [
            get_json_table_refresh_callback(container, request, IAssociationsTable),
            {
                'module': 'helpers',
                'callback': 'MyAMS.helpers.removeElement',
                'options': {
                    'selector': '.dz-preview'
                }
            }
        ]
    }
    event = get_json_paragraph_toolbar_refresh_event(container, request)
    if event is not None:
        result.setdefault('callbacks', []).append(event)
    return result
