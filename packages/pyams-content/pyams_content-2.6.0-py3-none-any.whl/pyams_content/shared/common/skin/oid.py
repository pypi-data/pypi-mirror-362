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

"""PyAMS_content.shared.common.skin.oid module

This module defines a custom route and a custom traverser used to support
'/+/{oid}::title.html' URL syntax support.
"""

from typing import Optional

from pyramid.httpexceptions import HTTPNotFound
from pyramid.interfaces import IRequest
from pyramid.response import Response
from pyramid.view import render_view_to_response, view_config
from zope.interface import Interface
from zope.traversing.interfaces import ITraversable

from pyams_content.interfaces import OID_ACCESS_ROUTE
from pyams_content.skin.interfaces import IPublicURL
from pyams_layer.interfaces import IPyAMSUserLayer
from pyams_sequence.interfaces import ISequentialIntIds
from pyams_sequence.reference import get_reference_target
from pyams_utils.adapter import ContextRequestAdapter, adapter_config
from pyams_utils.interfaces import DISPLAY_CONTEXT_KEY_NAME
from pyams_utils.registry import get_utility
from pyams_utils.url import absolute_url, canonical_url
from pyams_workflow.interfaces import IWorkflow, IWorkflowPublicationInfo, IWorkflowVersions

__docformat__ = 'restructuredtext'


def get_target(request: IRequest, oid: str) -> Optional[object]:
    """Get target from given reference"""
    sequence = get_utility(ISequentialIntIds)
    reference = sequence.get_full_oid(oid)
    target = get_reference_target(reference)
    if target is not None:
        workflow = IWorkflow(target, None)
        if workflow is not None:
            versions = IWorkflowVersions(target, None)
            if versions is not None:
                versions = versions.get_versions(workflow.visible_states, sort=True)
                if versions:
                    target = versions[-1]
    if (target is not None) and not IWorkflowPublicationInfo(target).is_visible(request):
        target = None
    return target


@view_config(route_name=OID_ACCESS_ROUTE)
def get_oid_access(request):
    """Get direct access to given OID

    This route can be used to get direct access to a given content,
    just by submitting an URL like /+/{oid}, where {oid} is the "short"
    sequence OID.
    """
    oid = request.matchdict.get('oid')
    if oid:
        oid = oid.split('::', 1)[0]
        view_name = ''.join(request.matchdict.get('view'))
        target = get_target(request, oid)
        if target is not None:
            if view_name:  # back-office access => last version
                public_url = request.registry.queryMultiAdapter((target, request), IPublicURL,
                                                                name=view_name)
                if public_url is not None:
                    location = public_url.get_url()
                else:
                    location = absolute_url(target, request, view_name)
            else:
                location = canonical_url(target, request, query=request.params)
            if location == request.url:
                # return view response to avoid infinite redirection!
                request.annotations[DISPLAY_CONTEXT_KEY_NAME] = request.context
                request.context = target
                response = render_view_to_response(target, request, view_name)
            else:
                response = Response()
                response.status_code = 302
                response.location = location
            return response
    raise HTTPNotFound()


@adapter_config(name='+',
                required=(Interface, IPyAMSUserLayer),
                provides=ITraversable)
@adapter_config(name='oid',
                required=(Interface, IPyAMSUserLayer),
                provides=ITraversable)
class OIDTraverser(ContextRequestAdapter):
    """++oid++ traverser

    This traverser can be used to get direct access to any content having an OID.
    The general URL syntax is "*/++oid++{oid}::{title}.html", where {oid} is the internal OID
    of the requested content, and "title" it's "content URL" attribute.

    A shorter syntax, is now available: */+/{oid}::{title}.html
    """

    def traverse(self, name, furtherpath=None):
        """++oid++ namespace traverser"""
        if not name:
            raise HTTPNotFound()
        context = self.context
        request = self.request
        if not hasattr(request, 'context'):
            request.context = context
        if '::' in name:
            oid, _title = name.split('::', 1)
        else:
            oid, _title = name, ''
        target = get_target(request, oid)
        if target is not None:
            request.annotations[DISPLAY_CONTEXT_KEY_NAME] = context
            request.context = target
            return target
        raise HTTPNotFound()
