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

"""PyAMS_content.feature.search.portlet.skin.zmi module

"""

from pyams_content.feature.search.portlet.skin import ISearchResultsPortletBaseRendererSettings, \
    ISearchResultsPortletCardsRendererSettings, ISearchResultsPortletPanelsRendererSettings
from pyams_form.field import Fields
from pyams_form.group import Group
from pyams_form.interfaces.form import IFormFields, IGroup
from pyams_portal.zmi.interfaces import IPortletRendererSettingsEditForm
from pyams_utils.adapter import adapter_config
from pyams_zmi.form import FormGroupChecker
from pyams_zmi.interfaces import IAdminLayer

__docformat__ = 'restructuredtext'

from pyams_content import _


#
# Base search results renderer settings
#

@adapter_config(required=(ISearchResultsPortletBaseRendererSettings, IAdminLayer, IPortletRendererSettingsEditForm),
                provides=IFormFields)
def search_results_portlet_renderer_settings_fields(context, request, form):
    """Search results portlet renderer settings fields getter"""
    return Fields(ISearchResultsPortletBaseRendererSettings).select(
        'display_if_empty', 'display_results_count', 'allow_sorting', 'allow_pagination',
        'filters_css_class', 'results_css_class')


@adapter_config(name='illustration',
                required=(ISearchResultsPortletBaseRendererSettings, IAdminLayer, IPortletRendererSettingsEditForm),
                provides=IGroup)
class SearchResultsPortletRendererIllustrationSettingsGroup(FormGroupChecker):
    """Search results portlet renderer illustration settings group"""

    fields = Fields(ISearchResultsPortletBaseRendererSettings).select(
        'display_illustrations', 'thumb_selection')
    weight = 10


@adapter_config(name='header',
                required=(ISearchResultsPortletBaseRendererSettings, IAdminLayer, IPortletRendererSettingsEditForm),
                provides=IGroup)
class SearchResultsPortletRendererHeaderSettingsGroup(Group):
    """Search results portlet renderer header settings group"""

    legend = _("Header display")

    fields = Fields(ISearchResultsPortletBaseRendererSettings).select(
        'header_display_mode', 'start_length', 'display_tags', 'display_publication_date')
    weight = 20


#
# Custom panels renderers settings edit form
#

@adapter_config(required=(ISearchResultsPortletPanelsRendererSettings, IAdminLayer, IPortletRendererSettingsEditForm),
                provides=IFormFields)
def search_results_portlet_panels_renderer_settings_fields(context, request, form):
    """Search results portlet renderer settings fields getter"""
    return Fields(ISearchResultsPortletPanelsRendererSettings).select(
        'display_if_empty', 'display_results_count', 'allow_sorting', 'allow_pagination',
        'filters_css_class', 'results_css_class', 'columns_count')


@adapter_config(name='illustration',
                required=(ISearchResultsPortletPanelsRendererSettings, IAdminLayer, IPortletRendererSettingsEditForm),
                provides=IGroup)
class SearchResultsPortletPanelsRendererIllustrationSettingsGroup(FormGroupChecker):
    """Search results portlet panels renderer illustration settings group"""

    fields = Fields(ISearchResultsPortletPanelsRendererSettings).select(
        'display_illustrations', 'thumb_selection')
    weight = 10


#
# Custom cards renderers settings edit form
#

@adapter_config(required=(ISearchResultsPortletCardsRendererSettings, IAdminLayer, IPortletRendererSettingsEditForm),
                provides=IFormFields)
def search_results_portlet_cards_renderer_settings_fields(context, request, form):
    """Search results portlet renderer settings fields getter"""
    return Fields(ISearchResultsPortletCardsRendererSettings).select(
        'display_if_empty', 'display_results_count', 'allow_sorting', 'allow_pagination',
        'filters_css_class', 'results_css_class', 'columns_count')


@adapter_config(name='illustration',
                required=(ISearchResultsPortletCardsRendererSettings, IAdminLayer, IPortletRendererSettingsEditForm),
                provides=IGroup)
class SearchResultsPortletCardsRendererIllustrationSettingsGroup(FormGroupChecker):
    """Search results portlet cards renderer illustration settings group"""

    fields = Fields(ISearchResultsPortletCardsRendererSettings).select(
        'display_illustrations', 'thumb_selection')
    weight = 10


@adapter_config(name='button',
                required=(ISearchResultsPortletCardsRendererSettings, IAdminLayer, IPortletRendererSettingsEditForm),
                provides=IGroup)
class SearchResultsPortletCardsRendererButtonSettingsGroup(Group):
    """Search results portlet cards renderer button settings group"""

    fields = Fields(ISearchResultsPortletCardsRendererSettings).select('button_title')
    weight = 30
