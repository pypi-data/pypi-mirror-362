# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.keynumber import KeyNumbersContainer
from pyams_content.component.keynumber.portlet.interfaces import IKeyNumbersPortletSettings
from pyams_portal.portlet import Portlet, PortletSettings, portlet_config
from pyams_utils.factory import factory_config

__docformat__ = 'restructuredtext'

from pyams_content import _


KEYNUMBERS_PORTLET_NAME = 'pyams_content.portlets.key-numbers'


@factory_config(provided=IKeyNumbersPortletSettings)
class KeyNumbersPortletSettings(KeyNumbersContainer, PortletSettings):
    """Key-numbers portlet settings"""
    
    title = FieldProperty(IKeyNumbersPortletSettings['title'])
    header = FieldProperty(IKeyNumbersPortletSettings['header'])
    
    
@portlet_config(permission=None)
class KeyNumbersPortlet(Portlet):
    """Key-numbers portlet"""
    
    name = KEYNUMBERS_PORTLET_NAME
    label = _("Key-numbers")
    
    settings_factory = IKeyNumbersPortletSettings
    toolbar_css_class = 'fas fa-dashboard'
