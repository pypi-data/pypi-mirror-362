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

"""PyAMS_content.component.links.html module

This module defines components which are used to handle associations in HTML
components.
"""

__docformat__ = 'restructuredtext'

import re

from pyquery import PyQuery
from zope.lifecycleevent import ObjectCreatedEvent

from pyams_content.component.association import IAssociationContainer
from pyams_content.component.extfile import IBaseExtFile
from pyams_content.component.links import IExternalLink, IInternalLink, IMailtoLink
from pyams_i18n.interfaces import II18n
from pyams_sequence.interfaces import ISequentialIntIds
from pyams_utils.factory import get_object_factory
from pyams_utils.registry import get_pyramid_registry, get_utility
from pyams_utils.request import check_request
from pyams_utils.url import absolute_url

FULL_EMAIL = re.compile(r'(.*) <(.*)>')


def check_content_links(context, body, lang, notify=True):  # pylint: disable=too-many-branches, too-many-statements, too-many-locals
    """Check for link associations from HTML content"""
    associations = IAssociationContainer(context, None)
    if associations is None:
        return
    registry = get_pyramid_registry()
    html = PyQuery(f'<html>{body}</html>')
    for link in html('a[href]'):
        link_info = None
        has_link = False
        href = link.attrib['href']
        if href.startswith('oid://'):
            sequence = get_utility(ISequentialIntIds)
            oid = sequence.get_full_oid(href.split('//', 1)[1])
            for association in associations.values():
                internal_info = IInternalLink(association, None)
                if (internal_info is not None) and (internal_info.reference == oid):
                    has_link = True
                    break
            if not has_link:
                factory = get_object_factory(IInternalLink)
                if factory is not None:
                    link_info = factory()
                    link_info.visible = False
                    link_info.reference = oid
                    link_info.title = {lang: link.attrib.get('title') or link.text}
        elif href.startswith('mailto:'):
            name = None
            email = href[7:]
            if '<' in email:
                groups = FULL_EMAIL.findall(email)
                if groups:
                    name, email = groups[0]
            for association in associations.values():
                mailto_info = IMailtoLink(association, None)
                if (mailto_info is not None) and (mailto_info.address == email):
                    has_link = True
                    break
            if not has_link:
                factory = get_object_factory(IMailtoLink)
                if factory is not None:
                    link_info = factory()
                    link_info.visible = False
                    link_info.address = email
                    link_info.address_name = name or email
                    link_info.title = {lang: link.attrib.get('title') or link.text}
        elif href.startswith('http://') or href.startswith('https://'):
            for association in associations.values():
                external_info = IExternalLink(association, None)
                if (external_info is not None) and (external_info.url == href):
                    has_link = True
                    break
                else:
                    extfile_info = IBaseExtFile(association, None)
                    if extfile_info is not None:
                        request = check_request()
                        extfile_url = absolute_url(
                            II18n(extfile_info).query_attribute('data', request=request),
                            request=request)
                        if extfile_url.endswith(href):
                            has_link = True
                            break
            if not has_link:
                factory = get_object_factory(IExternalLink)
                if factory is not None:
                    link_info = factory()
                    link_info.visible = False
                    link_info.url = href
                    link_info.title = {lang: link.attrib.get('title') or link.text}
        if link_info is not None:
            registry.notify(ObjectCreatedEvent(link_info))
            associations.append(link_info, notify=notify)
