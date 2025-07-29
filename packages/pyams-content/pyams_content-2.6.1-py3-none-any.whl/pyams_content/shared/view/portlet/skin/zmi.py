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

from zope.interface import Interface

from pyams_content.shared.view.portlet.skin import IViewItemsPortletBaseRendererSettings, \
    IViewItemsPortletPanelsRendererSettings, IViewItemsPortletThumbnailsRendererSettings, \
    IViewItemsPortletVerticalRendererSettings
from pyams_form.field import Fields
from pyams_form.group import Group
from pyams_form.interfaces.form import IFormFields, IGroup
from pyams_portal.zmi.interfaces import IPortletRendererSettingsEditForm
from pyams_utils.adapter import NullAdapter, adapter_config
from pyams_zmi.form import FormGroupChecker, FormGroupSwitcher
from pyams_zmi.interfaces import IAdminLayer

__docformat__ = 'restructuredtext'

from pyams_content import _


#
# View items portlet base renderer settings
#

@adapter_config(required=(IViewItemsPortletBaseRendererSettings, IAdminLayer, IPortletRendererSettingsEditForm),
                provides=IFormFields)
def view_items_panels_renderer_settings_fields(context, request, form):
    return Fields(Interface)


@adapter_config(name='css-classes',
                required=(IViewItemsPortletBaseRendererSettings, IAdminLayer,
                          IPortletRendererSettingsEditForm),
                provides=IGroup)
class CatalogViewItemsPortletCalendarRendererClassesSettingsGroup(FormGroupSwitcher):
    """Catalog view items portlet calendar renderer CSS classes settings group"""

    legend = _("CSS classes")

    fields = Fields(IViewItemsPortletBaseRendererSettings).select('filters_css_class', 'results_css_class')
    weight = 5


@adapter_config(name='pagination',
                required=(IViewItemsPortletBaseRendererSettings, IAdminLayer, IPortletRendererSettingsEditForm),
                provides=IGroup)
class ViewItemsPortletBaseRendererSettingsPaginationGroup(FormGroupChecker):
    """View items portlet base renderer settings pagination group"""
    
    fields = Fields(IViewItemsPortletBaseRendererSettings).select('paginate', 'page_size')
    weight = 90


#
# View items portlet vertical renderer settings
#

@adapter_config(name='illustration',
                required=(IViewItemsPortletVerticalRendererSettings, IAdminLayer, IPortletRendererSettingsEditForm),
                provides=IGroup)
class ViewItemsPortletVerticalRendererIllustrationSettingsGroup(FormGroupChecker):
    """View item portlet vertical renderer illustration settings group"""

    fields = Fields(IViewItemsPortletVerticalRendererSettings).select('display_illustrations', 'thumb_selection')
    weight = 20


@adapter_config(name='settings',
                required=(IViewItemsPortletVerticalRendererSettings, IAdminLayer, IPortletRendererSettingsEditForm),
                provides=IGroup)
class ViewItemsPortletVerticalRendererMiscSettingsGroup(Group):
    """View item portlet vertical renderer misc settings group"""

    fields = Fields(IViewItemsPortletVerticalRendererSettings).select('display_breadcrumbs', 'display_tags',
                                                                      'reference', 'link_label')
    weight = 30


#
# View items portlet thumbnails renderer settings
#

@adapter_config(name='illustration',
                required=(IViewItemsPortletThumbnailsRendererSettings, IAdminLayer, IPortletRendererSettingsEditForm),
                provides=IGroup)
class ViewItemsPortletThumbnailsRendererIllustrationSettingsGroup(FormGroupChecker):
    """View item portlet thumbnails renderer illustration settings group"""

    fields = Fields(IViewItemsPortletThumbnailsRendererSettings).select('display_illustrations', 'thumb_selection')
    weight = 20


@adapter_config(name='pagination',
                required=(IViewItemsPortletThumbnailsRendererSettings, IAdminLayer, IPortletRendererSettingsEditForm),
                provides=IGroup)
class ViewItemsPortletThumbnailsRendererSettingsPaginationGroup(NullAdapter):
    """View items portlet thumbnails renderer settings pagination group"""


#
# View items portlet panels renderer settings
#

@adapter_config(name='columns',
                required=(IViewItemsPortletPanelsRendererSettings, IAdminLayer, IPortletRendererSettingsEditForm),
                provides=IGroup)
class ViewItemsPortletPanelsRendererColumnsSettingsGroup(Group):
    """View item portlet panels renderer columns settings group"""
    
    fields = Fields(IViewItemsPortletPanelsRendererSettings).select('columns_count')
    weight = 10


@adapter_config(name='illustration',
                required=(IViewItemsPortletPanelsRendererSettings, IAdminLayer, IPortletRendererSettingsEditForm),
                provides=IGroup)
class ViewItemsPortletPanelsRendererIllustrationSettingsGroup(FormGroupChecker):
    """View item portlet panels renderer illustration settings group"""
    
    fields = Fields(IViewItemsPortletPanelsRendererSettings).select('display_illustrations', 'thumb_selection')
    weight = 20


@adapter_config(name='header',
                required=(IViewItemsPortletPanelsRendererSettings, IAdminLayer, IPortletRendererSettingsEditForm),
                provides=IGroup)
class ViewItemsPortletPanelsRendererHeaderSettingsGroup(Group):
    """View items portlet panels renderer header settings group"""

    legend = _("Header display")

    fields = Fields(IViewItemsPortletPanelsRendererSettings).select('header_display_mode', 'start_length')
    weight = 40
