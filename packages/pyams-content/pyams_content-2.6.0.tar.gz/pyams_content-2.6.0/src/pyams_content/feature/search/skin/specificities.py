# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

__docformat__ = 'restructuredtext'

from zope.interface import Interface

from pyams_content.feature.search import ISearchFolder
from pyams_content.shared.common.portlet.interfaces import ISpecificitiesRenderer
from pyams_layer.interfaces import IPyAMSUserLayer
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_viewlet.viewlet import ViewContentProvider


@adapter_config(name='header',
                required=(ISearchFolder, IPyAMSUserLayer, Interface),
                provides=ISpecificitiesRenderer)
@template_config(template='templates/specificities-header.pt', layer=IPyAMSUserLayer)
class SearchFolderSpecificitiesRenderer(ViewContentProvider):
    """Search folder specificities renderer"""
    