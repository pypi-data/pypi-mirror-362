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

"""PyAMS_content.shared.common.skin.breadcrumbs module

This module defines components used for shared contents breadcrumbs management.
"""

from zope.interface import Interface
from zope.location.interfaces import ILocation

from pyams_content.shared.common.interfaces.types import IWfTypedSharedContent
from pyams_layer.interfaces import IPyAMSUserLayer
from pyams_skin.interfaces.viewlet import IBreadcrumbs
from pyams_skin.viewlet.breadcrumb import LocationBreadcrumbs as BaseLocationBreadcrumbs
from pyams_template.template import override_template
from pyams_utils.adapter import adapter_config
from pyams_utils.interfaces import DISPLAY_CONTEXT_KEY_NAME

__docformat__ = 'restructuredtext'


@adapter_config(required=(ILocation, IPyAMSUserLayer, Interface),
                provides=IBreadcrumbs)
class BreadcrumbsAdapter(BaseLocationBreadcrumbs):
    """Breadcrumbs adapter"""

    @property
    def items(self):
        source = self.request.annotations.get(DISPLAY_CONTEXT_KEY_NAME)
        if source is None:
            source = self.request.context
        if source is not None:
            yield from self.get_items(source)


override_template(BreadcrumbsAdapter,
                  template='templates/breadcrumbs.pt', layer=IPyAMSUserLayer)


@adapter_config(required=(IWfTypedSharedContent, IPyAMSUserLayer, Interface),
                provides=IBreadcrumbs)
class TypedSharedContentBreadcrumbsAdapter(BreadcrumbsAdapter):
    """Typed shared content breadcrumbs adapter"""

    @property
    def items(self):
        data_type = self.context.get_data_type()
        if data_type is not None:
            source = data_type.get_source_folder()
            if source is not None:
                yield from self.get_items(source)
                return
        yield from super(TypedSharedContentBreadcrumbsAdapter, self).items
