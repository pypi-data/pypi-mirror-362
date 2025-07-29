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

"""PyAMS_content.feature.html module

This module provides several HTML renderers:
 - 'oid_to_href' is used to replace an HTML link URL using oid://xxx syntax to a real
   link to the specified target; the link is removed if the target is not published or can't be
   found; please note also that the link is always targetting the currently published version,
   if any;
 - 'remove_tags' is used to remove all tags from incoming HTML content.
"""

from pyquery import PyQuery
from pyramid.interfaces import IRequest

from pyams_sequence.interfaces import ISequentialIntIds
from pyams_sequence.reference import get_reference_target
from pyams_utils.adapter import ContextRequestAdapter, adapter_config
from pyams_utils.interfaces.text import IHTMLRenderer
from pyams_utils.registry import get_utility
from pyams_utils.request import get_display_context
from pyams_utils.text import text_to_html
from pyams_utils.url import canonical_url
from pyams_workflow.interfaces import IWorkflowPublicationInfo

__docformat__ = 'restructuredtext'


@adapter_config(name='oid_to_href',
                required=(str, IRequest),
                provides=IHTMLRenderer)
class OIDHTMLRenderer(ContextRequestAdapter):
    """An HTML renderer converting all "oid://" URLs to internal relative links"""

    def render(self, **kwargs):
        """Render oid:// links"""
        request = self.request
        html = PyQuery(f'<div>{self.context}</div>')
        sequence = get_utility(ISequentialIntIds)
        for link in html('a[href]'):
            href = link.attrib['href']
            if href.startswith('oid://'):
                oid = sequence.get_full_oid(href.split('//', 1)[1])
                target = get_reference_target(oid, request=request)
                if target is not None:
                    publication_info = IWorkflowPublicationInfo(target, None)
                    if (publication_info is not None) and \
                            publication_info.is_visible(request):
                        link.attrib['href'] = canonical_url(target, request)
                        continue
                # invalid link => remove href!
                link.tag = 'span'
                for name in link.attrib.keys()[:]:
                    del link.attrib[name]
        return html.html()


@adapter_config(name='remove_tags',
                required=(str, IRequest),
                provides=IHTMLRenderer)
class TagsRemoveHTMLRenderer(ContextRequestAdapter):
    """Remove all tags from HTML code"""

    def render(self, **kwargs):
        """Render HTML source without tags"""
        html = PyQuery('<div>{}</div>'.format(self.context))
        return text_to_html(html.text())
