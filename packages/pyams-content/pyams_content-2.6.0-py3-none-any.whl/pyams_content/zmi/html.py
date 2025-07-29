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

"""PyAMS_content.zmi.html module

This module provides configuration adapter for TinyMCE HTML editor.
"""

__docformat__ = 'restructuredtext'

import json

from zope.dublincore.interfaces import IZopeDublinCore

from pyams_content.zmi import content_js
from pyams_layer.interfaces import ISkinnable
from pyams_skin.interfaces.widget import IHTMLWidget
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.fanstatic import get_resource_path
from pyams_utils.interfaces.data import IObjectDataRenderer
from pyams_utils.traversing import get_parent
from pyams_utils.url import absolute_url


@adapter_config(required=IHTMLWidget,
                provides=IObjectDataRenderer)
class HTMLWidgetDataRenderer(ContextAdapter):
    """HTML widget data getter"""

    def get_object_data(self):
        """Object data getter"""
        context = self.context.context
        request = self.context.request
        data = {
            'ams-modules': {
                'content': get_resource_path(content_js)
            },
            'ams-tinymce-init-callback': 'MyAMS.content.TinyMCE.initEditor',
            'ams-tinymce-link-list': absolute_url(context, request, 'get-links-list.json')
        }
        skinnable = get_parent(request.context, ISkinnable)
        if skinnable is not None:
            editor_stylesheet = skinnable.editor_stylesheet
            if editor_stylesheet:
                modified = IZopeDublinCore(editor_stylesheet).modified
                data['ams-tinymce-content-css'] = absolute_url(editor_stylesheet,
                                                               request,
                                                               query={
                                                                   '_': modified.timestamp()
                                                               })
        return json.dumps(data)
