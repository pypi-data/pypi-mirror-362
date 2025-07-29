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

"""PyAMS_content.feature.navigation.portlet.skin module

"""

from persistent import Persistent
from zope.container.contained import Contained
from zope.interface import Interface
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.association.interfaces import IAssociationInfo
from pyams_content.feature.navigation.portlet import IDoubleNavigationPortletSettings, \
    ISimpleNavigationPortletSettings
from pyams_content.feature.navigation.portlet.skin.interfaces import \
    IDoubleNavigationPortletDefaultRendererSettings, \
    ISimpleNavigationPortletDefaultRendererSettings
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import IPortalContext, IPortletRenderer
from pyams_portal.skin import PortletRenderer
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_utils.factory import factory_config


__docformat__ = 'restructuredtext'

from pyams_content import _


#
# Simple navigation portlet renderers
#

class BaseSimpleNavigationPortletRenderer(PortletRenderer):
    """Base simple navigation portlet renderer"""

    @staticmethod
    def get_link_info(link):
        """Link information getter"""
        return IAssociationInfo(link)


@factory_config(ISimpleNavigationPortletDefaultRendererSettings)
class SimpleNavigationPortletDefaultRendererSettings(Persistent, Contained):
    """Simple navigation portlet default renderer settings"""

    thumb_selection = FieldProperty(
        ISimpleNavigationPortletDefaultRendererSettings['thumb_selection'])


@adapter_config(required=(IPortalContext, IPyAMSLayer, Interface,
                          ISimpleNavigationPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/simple-default.pt', layer=IPyAMSLayer)
class SimpleNavigationPortletDefaultRenderer(BaseSimpleNavigationPortletRenderer):
    """Simple navigation portlet default renderer"""

    label = _("Horizontal grid links with illustrations (default)")

    settings_interface = ISimpleNavigationPortletDefaultRendererSettings
    weight = 10


@adapter_config(name='footer-simple',
                required=(IPortalContext, IPyAMSLayer, Interface,
                          ISimpleNavigationPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/simple-footer.pt', layer=IPyAMSLayer)
class SimpleNavigationPortletFooterRenderer(BaseSimpleNavigationPortletRenderer):
    """Simple navigation portlet footer renderer"""

    label = _("Simple footer links")

    weight = 20


#
# Double navigation portlet renderers
#

@factory_config(IDoubleNavigationPortletDefaultRendererSettings)
class DoubleNavigationPortletDefaultRendererSettings(Persistent, Contained):
    """Double navigation portlet default renderer settings"""

    thumb_selection = FieldProperty(
        IDoubleNavigationPortletDefaultRendererSettings['thumb_selection'])


@adapter_config(required=(IPortalContext, IPyAMSLayer, Interface,
                          IDoubleNavigationPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/double-default.pt', layer=IPyAMSLayer)
class DoubleNavigationPortletDefaultRenderer(PortletRenderer):
    """Double navigation portlet default renderer"""

    label = _("Horizontal tabs of grids links with illustrations (default)")

    settings_interface = IDoubleNavigationPortletDefaultRendererSettings
    weight = 10

    @staticmethod
    def get_link_info(link):
        """Link information getter"""
        return IAssociationInfo(link)
