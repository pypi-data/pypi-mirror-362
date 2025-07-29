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
from zope.location.interfaces import ILocation

from pyams_content.interfaces import IBaseContent
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSUserLayer
from pyams_skin.interfaces.viewlet import IBreadcrumbItem, IBreadcrumbs
from pyams_skin.viewlet.breadcrumb import BreadcrumbItem, BreadcrumbsContentProvider, LocationBreadcrumbs
from pyams_template.template import override_template
from pyams_utils.adapter import adapter_config
from pyams_utils.interfaces import DISPLAY_CONTEXT_KEY_NAME


@adapter_config(required=(ILocation, IPyAMSUserLayer, Interface),
                provides=IBreadcrumbs)
class BreadcrumbsAdapter(LocationBreadcrumbs):
    """Breadcrumbs adapter"""

    @property
    def items(self):
        source = self.request.annotations.get(DISPLAY_CONTEXT_KEY_NAME)
        if source is None:
            source = self.request.context
        if source is not None:
            yield from self.get_items(source)


override_template(view=BreadcrumbsContentProvider,
                  layer=IPyAMSUserLayer,
                  template='templates/breadcrumbs.pt')


@adapter_config(required=(IBaseContent, IPyAMSUserLayer, Interface),
                provides=IBreadcrumbItem)
class BaseContentBreadcrumbAdapter(BreadcrumbItem):
    """Base content breadcrumb adapter"""

    @property
    def label(self):
        return II18n(self.context).query_attribute('short_name', request=self.request)
