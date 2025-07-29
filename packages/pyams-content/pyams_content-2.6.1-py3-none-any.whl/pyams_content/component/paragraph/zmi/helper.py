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

"""PyAMS_*** module

"""

__docformat__ = 'restructuredtext'


from zope.contentprovider.interfaces import IContentProvider

from pyams_content.component.paragraph.interfaces import IBaseParagraph, IParagraphContainer
from pyams_content.component.paragraph.zmi.interfaces import IParagraphContainerFullTable
from pyams_utils.factory import get_object_factory
from pyams_utils.traversing import get_parent


def get_json_paragraph_toolbar_refresh_event(context, request):
    """Get paragraph toolbar refresh event"""
    paragraph = get_parent(context, IBaseParagraph)
    if paragraph is None:
        return None
    container = get_parent(paragraph, IParagraphContainer)
    if container is None:
        return None
    factory = get_object_factory(IParagraphContainerFullTable)
    if factory is None:
        return None
    table = factory(container, request)
    provider = request.registry.queryMultiAdapter((paragraph, request, table), IContentProvider,
                                                  name='pyams_content.paragraph.title-toolbar')
    if provider is None:
        return None
    provider.update()
    return {
        'callback': 'MyAMS.helpers.refreshElement',
        'options': {
            'object_id': provider.id,
            'content': provider.render()
        }
    }
