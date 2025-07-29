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

from pyams_content.shared.site.portlet.interfaces import ISiteContainerSummaryPortletSettings, \
    SITE_CONTAINER_SUMMARY_PORTLET_NAME
from pyams_portal.portlet import Portlet, PortletSettings, portlet_config
from pyams_utils.factory import factory_config

__docformat__ = 'restructuredtext'

from pyams_content import _


@factory_config(provided=ISiteContainerSummaryPortletSettings)
class SiteContainerSummaryPortletSettings(PortletSettings):
    """Site container summary portlet settings"""
    
    title = FieldProperty(ISiteContainerSummaryPortletSettings['title'])
    button_title = FieldProperty(ISiteContainerSummaryPortletSettings['button_title'])
    
    
@portlet_config(permission=None)
class SiteContainerSummaryPortlet(Portlet):
    """Site container summary portlet"""
    
    name = SITE_CONTAINER_SUMMARY_PORTLET_NAME
    label = _("Site container summary")
    
    settings_factory = ISiteContainerSummaryPortletSettings
    toolbar_css_class = 'far fa-list-alt'
    