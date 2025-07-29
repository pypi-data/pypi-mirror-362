# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from zope.interface import Interface

from pyams_content.component.keynumber.portlet import IKeyNumbersPortletSettings
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import IPortalContext, IPortletRenderer
from pyams_portal.skin import PortletRenderer
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config

__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(required=(IPortalContext, IPyAMSLayer, Interface, IKeyNumbersPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/key-numbers-default.pt', layer=IPyAMSLayer)
class KeyNumbersPortletDefaultRenderer(PortletRenderer):
    """Key-numbers portlet default renderer"""
    
    label = _("Horizontal cards list (default)")
    weight = 1


@adapter_config(name='vertical',
                required=(IPortalContext, IPyAMSLayer, Interface, IKeyNumbersPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/key-numbers-vertical.pt', layer=IPyAMSLayer)
class KeyNumbersPortletVerticalRenderer(PortletRenderer):
    """Key-numbers portlet vertical renderer"""
    
    label = _("Vertical cards list")
    weight = 10
