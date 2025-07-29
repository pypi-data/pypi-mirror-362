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

from pyams_content.component.illustration import ILinkIllustration
from pyams_content.shared.site.interfaces import IInternalSiteLink
from pyams_content.skin.interfaces import IContentNavigationIllustration
from pyams_layer.interfaces import IPyAMSUserLayer
from pyams_utils.adapter import adapter_config


@adapter_config(required=(IInternalSiteLink, IPyAMSUserLayer),
                provides=IContentNavigationIllustration)
def internal_site_link_content_navigation_illustration(context, request):
    """Internal site link content navigation illustration"""
    illustration = ILinkIllustration(context, None)
    if illustration and illustration.has_data():
        return illustration
    target = context.get_target(request=request)
    if target is not None:
        return request.registry.queryMultiAdapter((target, request),
                                                  IContentNavigationIllustration)
    return None
