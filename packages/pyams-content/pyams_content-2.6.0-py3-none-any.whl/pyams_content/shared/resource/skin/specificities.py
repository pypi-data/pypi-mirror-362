# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from pyramid.decorator import reify
from zope.interface import Interface

from pyams_content.component.thesaurus import ICollectionsInfo
from pyams_content.feature.search.interfaces import ISearchManagerInfo
from pyams_content.shared.common.portlet.interfaces import ISpecificitiesRenderer
from pyams_content.shared.resource import IResourceInfo, IWfResource
from pyams_content.shared.resource.schema import IAgeRange
from pyams_layer.interfaces import IPyAMSUserLayer
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_viewlet.viewlet import ViewContentProvider

__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(required=(IWfResource, IPyAMSUserLayer, Interface),
                provides=ISpecificitiesRenderer)
@template_config(template='templates/specificities.pt', layer=IPyAMSUserLayer)
class ResourceSpecificitiesRenderer(ViewContentProvider):
    """Resource specificities renderer"""
    
    @property
    def resource_info(self):
        return IResourceInfo(self.context, None)
    
    @property
    def collections(self):
        collections_info = ICollectionsInfo(self.context, None)
        if collections_info is not None:
            yield from sorted(collections_info.collections or (),
                              key=lambda x: (x.order or 999, x.alt or x.label))
            
    @reify
    def search_target(self):
        search_info = ISearchManagerInfo(self.request.root, None)
        if search_info is not None:
            return search_info.collections_target
        
    def get_age_range(self, value: IAgeRange):
        translate = self.request.localizer.translate
        if value.min_value and value.max_value:
            result = _("from {0.min_value} to {0.max_value}")
        elif value.min_value:
            result = _("from {0.min_value}")
        else:
            result = _("up to {0.max_value}")
        return translate(result).format(value)
