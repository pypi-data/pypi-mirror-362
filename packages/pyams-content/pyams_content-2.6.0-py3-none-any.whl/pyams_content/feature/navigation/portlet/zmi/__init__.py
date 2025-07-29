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

"""PyAMS_content.feature.navigation.portlet.zmi module

"""

from zope.interface import Interface, implementer

from pyams_content.component.association.interfaces import IAssociationInfo
from pyams_content.component.association.zmi.container import AssociationsGroup
from pyams_content.feature.navigation import IMenuLinksContainerTarget
from pyams_content.feature.navigation.portlet import IDoubleNavigationPortletSettings, \
    ISimpleNavigationPortletSettings
from pyams_form.interfaces.form import IInnerSubForm
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import IPortletPreviewer
from pyams_portal.zmi import PortletPreviewer
from pyams_portal.zmi.interfaces import IPortletConfigurationEditor
from pyams_portal.zmi.portlet import PortletConfigurationEditForm
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.form import IPropertiesEditForm

__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(required=(Interface, IPyAMSLayer, Interface, ISimpleNavigationPortletSettings),
                provides=IPortletPreviewer)
@template_config(template='templates/simple-preview.pt', layer=IPyAMSLayer)
class SimpleNavigationPortletPreviewer(PortletPreviewer):
    """Simple navigation portlet previewer"""

    @staticmethod
    def get_link_info(link):
        """Link information getter"""
        return IAssociationInfo(link)


@adapter_config(name='associations-group',
                required=(ISimpleNavigationPortletSettings, IAdminLayer, IPropertiesEditForm),
                provides=IInnerSubForm, force_implements=False)
@adapter_config(name='associations-group',
                required=(IMenuLinksContainerTarget, IAdminLayer, IPropertiesEditForm),
                provides=IInnerSubForm, force_implements=False)
class LinksContainerAssociationsGroup(AssociationsGroup):
    """Links container table group"""

    legend = _("Navigation links")


@adapter_config(required=(Interface, IPyAMSLayer, Interface, IDoubleNavigationPortletSettings),
                provides=IPortletPreviewer)
@template_config(template='templates/double-preview.pt', layer=IPyAMSLayer)
class DoubleNavigationPortletPreviewer(PortletPreviewer):
    """Double navigation portlet previewer"""

    @staticmethod
    def get_link_info(link):
        """Link information getter"""
        return IAssociationInfo(link)


@adapter_config(name='configuration',
                required=(IDoubleNavigationPortletSettings, IAdminLayer,
                          IPortletConfigurationEditor),
                provides=IInnerSubForm)
@implementer(IPropertiesEditForm)
class DoubleNavigationPortletSettingsEditForm(PortletConfigurationEditForm):
    """Double navigation portlet settings edit form"""
