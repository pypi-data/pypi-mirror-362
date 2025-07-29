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

__docformat__ = 'restructuredtext'

from pyramid.decorator import reify
from zope.contentprovider.interfaces import IContentProvider
from zope.interface import Interface

from pyams_content.component.thesaurus import ITagsInfo
from pyams_content.feature.search.interfaces import ISearchManagerInfo
from pyams_layer.interfaces import IPyAMSLayer
from pyams_template.template import template_config
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.interfaces.tales import ITALESExtension
from pyams_viewlet.viewlet import ViewContentProvider, contentprovider_config


@contentprovider_config(name='pyams_content.tags',
                        layer=IPyAMSLayer, view=Interface)
@template_config(template='templates/tags.pt', layer=IPyAMSLayer)
class TagsContentProvider(ViewContentProvider):
    """Tags content provider"""

    tags_info = None

    def update(self):
        super().update()
        self.tags_info = ITagsInfo(self.context, None)

    def render(self, template_name=''):
        if self.tags_info is None:
            return ''
        return super().render(template_name)

    @reify
    def search_target(self):
        manager = ISearchManagerInfo(self.request.root, None)
        if manager is not None:
            return manager.tags_target
        return None

    @property
    def tags(self):
        tags = self.tags_info.tags or ()
        yield from sorted(tags, key=lambda x: (x.order or 999, x.alt or x.label))


@adapter_config(name='tags',
                required=(Interface, Interface, Interface),
                provides=ITALESExtension)
class TagsTALESExtension(ContextRequestViewAdapter):
    """tales:tags(context) TALES extension"""

    def render(self, context=None):
        if context is None:
            context = self.context
        provider = self.request.registry.queryMultiAdapter((context, self.request, self.view),
                                                           IContentProvider,
                                                           name='pyams_content.tags')
        if provider is None:
            return ''
        provider.update()
        return provider.render()
