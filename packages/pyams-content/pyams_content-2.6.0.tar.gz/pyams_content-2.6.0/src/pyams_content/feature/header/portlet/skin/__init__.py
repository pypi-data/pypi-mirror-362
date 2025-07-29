#
# Copyright (c) 2015-2024 Thierry Florac <tflorac AT ulthar.net>
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

from pyramid.authorization import Authenticated
from pyramid.traversal import lineage
from zope.interface import Interface

from pyams_content.feature.header.interfaces import IPageHeaderTitle
from pyams_content.feature.header.portlet import IPageHeaderPortletSettings
from pyams_content.root import ISiteRootInfos
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import IPortalContext, IPortletRenderer
from pyams_portal.skin import PortletRenderer
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config

__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(required=(IPortalContext, IPyAMSLayer, Interface, IPageHeaderPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/header-default.pt', layer=IPyAMSLayer)
class PageHeaderPortletDefaultRenderer(PortletRenderer):
    """Page header portlet default renderer"""

    label = _("Simple banner (default)")
    weight = 10

    use_authentication = True

    @property
    def logo(self):
        infos = ISiteRootInfos(self.request.root, None)
        if infos is None:
            return None, None
        return self.request.root, infos.logo

    @property
    def title(self):
        request  =self.request
        registry = request.registry
        for context in lineage(self.context):
            header = registry.queryMultiAdapter((context, self.request), IPageHeaderTitle)
            if header is not None:
                return header
        infos = ISiteRootInfos(self.request.root, None)
        return II18n(infos).query_attribute('title', request=self.request)

    @property
    def authenticated(self):
        identity = self.request.identity
        if identity is None:
            return False
        return Authenticated in identity.principals
