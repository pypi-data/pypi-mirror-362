# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from pyams_content.feature.search.portlet.skin import ISearchResultRenderer, WfSharedContentSearchResultRenderer
from pyams_content.feature.search.skin.interfaces import ISearchResultsView
from pyams_content.shared.resource import IWfResource
from pyams_layer.interfaces import IPyAMSUserLayer
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config

__docformat__ = 'restructuredtext'


@adapter_config(required=(IWfResource, IPyAMSUserLayer, ISearchResultsView),
                provides=ISearchResultRenderer)
@template_config(template='templates/search-result.pt', layer=IPyAMSUserLayer)
@template_config(name='panel',
                 template='templates/search-result-panel.pt', layer=IPyAMSUserLayer)
@template_config(name='card',
                 template='templates/search-result-card.pt', layer=IPyAMSUserLayer)
@template_config(name='masonry',
                 template='templates/search-result-masonry.pt', layer=IPyAMSUserLayer)
class WfResourceSearchResultRenderer(WfSharedContentSearchResultRenderer):
    """Resource search result renderer"""
