#
# Copyright (c) 2015-2022 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.component.file module

This module provides a custom file view to check parents publication.
"""

__docformat__ = 'restructuredtext'

from pyramid.httpexceptions import HTTPNotFound
from pyramid.location import lineage
from pyramid.view import view_config

from pyams_file.interfaces import IFile
from pyams_file.skin.view import FileView
from pyams_layer.interfaces import IPyAMSUserLayer
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_workflow.interfaces import IWorkflowPublicationInfo


@view_config(context=IFile,
             request_type=IPyAMSUserLayer)
def ProtectedFileView(request):  # pylint: disable=invalid-name
    """Protected file view"""
    context = request.context
    if not request.has_permission(VIEW_SYSTEM_PERMISSION, context=context):  # authenticated
        for parent in lineage(context):
            publication_info = IWorkflowPublicationInfo(parent, None)
            if (publication_info is not None) and not publication_info.is_visible(request):
                raise HTTPNotFound()
    return FileView(request)
