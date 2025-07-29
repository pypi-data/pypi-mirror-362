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

"""PyAMS_*** module

"""

from pyams_content.component.gallery.interfaces import IGalleryContainer
from pyams_content.component.gallery.zmi.interfaces import IGalleryMediasView, IGalleryMediaThumbnailView
from pyams_utils.factory import create_object
from pyams_utils.interfaces import ICacheKeyValue
from pyams_utils.traversing import get_parent

__docformat__ = 'restructuredtext'


def get_json_gallery_refresh_callback(context, request, view):
    """Get gallery refresh event"""
    gallery = get_parent(context, IGalleryContainer)
    provider = create_object(IGalleryMediasView,
                             context=gallery, request=request, view=view)
    if provider is not None:
        provider.update()
        return {
            'callback': 'MyAMS.helpers.refreshElement',
            'options': {
                'object_id': f'gallery_{ICacheKeyValue(gallery)}',
                'content': provider.render()
            }
        }
    return None


def get_json_gallery_media_refresh_callback(context, request, view):
    """Get gallery media refresh event"""
    provider = create_object(IGalleryMediaThumbnailView,
                             context=context, request=request, view=view)
    if provider is not None:
        provider.update()
        return {
            'callback': 'MyAMS.helpers.refreshElement',
            'options': {
                'object_id': f'media_{ICacheKeyValue(context)}',
                'content': provider.render()
            }
        }
    return None
