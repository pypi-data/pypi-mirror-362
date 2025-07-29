# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from persistent import Persistent
from zope.container.contained import Contained
from zope.interface import Interface
from zope.schema.fieldproperty import FieldProperty

from pyams_content.shared.logo.portlet import ILogosPortletSettings
from pyams_content.shared.logo.portlet.skin.interfaces import ILogosPortletDefaultRendererSettings
from pyams_content.shared.logo.skin import TARGET_PRIORITY
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import IPortalContext, IPortletRenderer
from pyams_portal.skin import PortletRenderer
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_utils.factory import factory_config
from pyams_utils.url import canonical_url, relative_url

__docformat__ = 'restructuredtext'

from pyams_content import _


@factory_config(ILogosPortletDefaultRendererSettings)
class LogosPortletDefaultRendererSettings(Persistent, Contained):
    """Logos portlet default renderer settings"""
    
    target_priority = FieldProperty(ILogosPortletDefaultRendererSettings['target_priority'])
    force_canonical_url = FieldProperty(ILogosPortletDefaultRendererSettings['force_canonical_url'])
    
    
@adapter_config(required=(IPortalContext, IPyAMSLayer, Interface, ILogosPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/logos-default.pt', layer=IPyAMSLayer)
class LogosPortletDefaultRenderer(PortletRenderer):
    """Logos portlet default renderer"""
    
    label = _("Simple logos list (default)")

    settings_interface = ILogosPortletDefaultRendererSettings
    
    def get_internal_url(self, logo):
        target = logo.target
        if target is not None:
            if self.renderer_settings.force_canonical_url:
                url_getter = canonical_url
            else:
                url_getter = relative_url
            return url_getter(target, request=self.request)
        return None

    @staticmethod
    def get_external_url(logo):
        return logo.url

    def get_url(self, logo):
        priority = self.renderer_settings.target_priority
        if priority == TARGET_PRIORITY.DISABLED.value:
            return None
        order = [self.get_external_url, self.get_internal_url]
        if priority == TARGET_PRIORITY.INTERNAL_FIRST.value:
            order = reversed(order)
        for getter in order:
            result = getter(logo)
            if result is not None:
                return result
        return None
