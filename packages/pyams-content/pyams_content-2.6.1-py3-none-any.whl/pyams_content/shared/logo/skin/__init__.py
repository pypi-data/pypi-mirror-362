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

from persistent import Persistent
from zope.container.contained import Contained
from zope.schema.fieldproperty import FieldProperty

from pyams_content.feature.renderer import DefaultContentRenderer, IContentRenderer
from pyams_content.shared.logo import IWfLogo
from pyams_content.shared.logo.interfaces import ILogosParagraph
from pyams_content.shared.logo.skin.interfaces import ILogosParagraphDefaultRendererSettings, TARGET_PRIORITY
from pyams_content.shared.view.portlet.skin import IViewItemTargetURL
from pyams_layer.interfaces import IPyAMSLayer, IPyAMSUserLayer
from pyams_portal.interfaces import DEFAULT_RENDERER_NAME
from pyams_template.template import template_config
from pyams_utils.adapter import ContextRequestAdapter, adapter_config
from pyams_utils.factory import factory_config
from pyams_utils.interfaces.url import ICanonicalURL, IRelativeURL
from pyams_utils.url import canonical_url, relative_url

__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(required=(IWfLogo, IPyAMSLayer),
                provides=IViewItemTargetURL)
class LogoViewItemTarget(ContextRequestAdapter):
    """Logo view item target getter"""

    @property
    def target(self):
        """Logo target getter"""
        return self.context.target

    @property
    def url(self):
        """Logo URL getter"""
        return self.context.url


@adapter_config(required=(IWfLogo, IPyAMSUserLayer),
                provides=ICanonicalURL)
class WfLogoCanonicalUrlAdapter(ContextRequestAdapter):
    """Logo canonical URL adapter"""

    def get_url(self, view_name=None, query=None):
        if self.context.url:
            return self.context.url
        if self.context.reference:
            target = self.context.target
            if target is not None:
                return canonical_url(target, self.request, view_name, query)
        return None


@adapter_config(context=(IWfLogo, IPyAMSUserLayer),
                provides=IRelativeURL)
class WfLogoRelativeUrlAdapter(ContextRequestAdapter):
    """Logo relative URL adapter"""

    def get_url(self, display_context=None, view_name=None, query=None):
        if self.context.url:
            return self.context.url
        if self.context.reference:
            target = self.context.target
            if target is not None:
                return relative_url(target, self.request, display_context, view_name, query)
        return None


@factory_config(ILogosParagraphDefaultRendererSettings)
class LogosParagraphDefaultRendererSettings(Persistent, Contained):
    """Logos paragraph default renderer settings"""
    
    target_priority = FieldProperty(ILogosParagraphDefaultRendererSettings['target_priority'])
    force_canonical_url = FieldProperty(ILogosParagraphDefaultRendererSettings['force_canonical_url'])


@adapter_config(name=DEFAULT_RENDERER_NAME,
                required=(ILogosParagraph, IPyAMSLayer),
                provides=IContentRenderer)
@template_config(template='templates/logos-default.pt',
                 layer=IPyAMSLayer)
class LogosParagraphDefaultRenderer(DefaultContentRenderer):
    """Logos paragraph default renderer"""
    
    label = _("Simple logos list (default)")

    settings_interface = ILogosParagraphDefaultRendererSettings
    
    def get_internal_url(self, logo):
        target = logo.target
        if target is not None:
            if self.settings.force_canonical_url:
                url_getter = canonical_url
            else:
                url_getter = relative_url
            return url_getter(target, request=self.request)
        return None

    @staticmethod
    def get_external_url(logo):
        return logo.url

    def get_url(self, logo):
        priority = self.settings.target_priority
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
