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

"""PyAMS_content.shared.view.zmi.thesaurus module

This module defines management interface components used to handle
thesaurus-based views settings.
"""

from pyams_content.component.thesaurus import ICollectionsManager, ITagsManager, IThemesManager
from pyams_content.shared.view import IWfView
from pyams_content.shared.view.interfaces.settings import IViewCollectionsSettings, IViewTagsSettings, \
    IViewThemesSettings
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_thesaurus.zmi.widget import ThesaurusTermsTreeFieldWidget
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminEditForm
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IPropertiesMenu
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_content import _


#
# Tags management
#

@viewlet_config(name='tags.menu',
                context=IWfView, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=350,
                permission=VIEW_SYSTEM_PERMISSION)
class ViewTagsMenu(NavigationMenuItem):
    """View tags menu"""

    def __new__(cls, context, request, view, manager):
        tags_manager = ITagsManager(request.root, None)
        if (tags_manager is None) or not tags_manager.thesaurus_name:
            return None
        return NavigationMenuItem.__new__(cls)

    label = _("Tags")
    href = '#tags.html'


@ajax_form_config(name='tags.html',
                  context=IWfView, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class ViewTagsEditForm(AdminEditForm):
    """View tags settings edit form"""

    title = _("Tags settings")
    legend = _("View tags settings")

    label_css_class = 'control-label col-md-1'
    input_css_class = 'col-md-11'

    fields = Fields(IViewTagsSettings)
    fields['tags'].widget_factory = ThesaurusTermsTreeFieldWidget

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        widget = self.widgets.get('tags')
        if widget is not None:
            manager = ITagsManager(self.request.root, None)
            if manager is not None:
                widget.label_css_class = 'control-label col-md-2'
                widget.input_css_class = 'col-md-12'
                widget.thesaurus_name = manager.thesaurus_name
                widget.extract_name = manager.extract_name


#
# Themes management
#

@viewlet_config(name='themes.menu',
                context=IWfView, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=360,
                permission=VIEW_SYSTEM_PERMISSION)
class ViewThemesMenu(NavigationMenuItem):
    """View themes menu"""

    def __new__(cls, context, request, view, manager):
        themes_manager = IThemesManager(request.root, None)
        if (themes_manager is None) or not themes_manager.thesaurus_name:
            return None
        return NavigationMenuItem.__new__(cls)

    label = _("Themes")
    href = '#themes.html'


@ajax_form_config(name='themes.html',
                  context=IWfView, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class ViewThemesEditForm(AdminEditForm):
    """View themes settings edit form"""

    title = _("Themes settings")
    legend = _("View themes settings")

    label_css_class = 'control-label col-md-1'
    input_css_class = 'col-md-11'

    fields = Fields(IViewThemesSettings)
    fields['themes'].widget_factory = ThesaurusTermsTreeFieldWidget

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        widget = self.widgets.get('themes')
        if widget is not None:
            manager = IThemesManager(self.request.root, None)
            if manager is not None:
                widget.label_css_class = 'control-label col-md-2'
                widget.input_css_class = 'col-md-12'
                widget.thesaurus_name = manager.thesaurus_name
                widget.extract_name = manager.extract_name


#
# Collections management
#

@viewlet_config(name='collections.menu',
                context=IWfView, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=370,
                permission=VIEW_SYSTEM_PERMISSION)
class ViewCollectionsMenu(NavigationMenuItem):
    """View collections menu"""

    def __new__(cls, context, request, view, manager):
        collections_manager = ICollectionsManager(request.root, None)
        if (collections_manager is None) or not collections_manager.thesaurus_name:
            return None
        return NavigationMenuItem.__new__(cls)

    label = _("Collections")
    href = '#collections.html'


@ajax_form_config(name='collections.html',
                  context=IWfView, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class ViewCollectionsEditForm(AdminEditForm):
    """View collections settings edit form"""

    title = _("Collections settings")
    legend = _("View collections settings")

    label_css_class = 'control-label col-md-1'
    input_css_class = 'col-md-11'

    fields = Fields(IViewCollectionsSettings)
    fields['collections'].widget_factory = ThesaurusTermsTreeFieldWidget

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        widget = self.widgets.get('collections')
        if widget is not None:
            manager = ICollectionsManager(self.request.root, None)
            if manager is not None:
                widget.label_css_class = 'control-label col-md-2'
                widget.input_css_class = 'col-md-12'
                widget.thesaurus_name = manager.thesaurus_name
                widget.extract_name = manager.extract_name
