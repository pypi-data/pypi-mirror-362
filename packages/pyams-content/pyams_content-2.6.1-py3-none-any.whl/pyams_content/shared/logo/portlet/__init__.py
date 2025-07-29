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

from pyams_content.shared.logo.portlet.interfaces import ILogosPortletSettings
from pyams_portal.portlet import Portlet, PortletSettings, portlet_config
from pyams_sequence.reference import get_reference_target
from pyams_utils.factory import factory_config

__docformat__ = 'restructuredtext'

from pyams_content import _


LOGOS_PORTLET_NAME = 'pyams_content.portlet.logos'


@factory_config(ILogosPortletSettings)
class LogosPortletSettings(PortletSettings):
    """Logos portlet settings"""
    
    title = FieldProperty(ILogosPortletSettings['title'])
    references = FieldProperty(ILogosPortletSettings['references'])
    
    def get_logos(self, status=None, with_reference=False):
        """Get logos from internal references"""
        for reference in self.references or ():
            target = get_reference_target(reference, status)
            if target is not None:
                yield (reference, target) if with_reference else target
                
    
@portlet_config(permission=None)
class LogosPortlet(Portlet):
    """Logos portlet"""
    
    name = LOGOS_PORTLET_NAME
    label = _("Logos")
    
    settings_factory = ILogosPortletSettings
    toolbar_css_class = 'fas fa-icons'
    