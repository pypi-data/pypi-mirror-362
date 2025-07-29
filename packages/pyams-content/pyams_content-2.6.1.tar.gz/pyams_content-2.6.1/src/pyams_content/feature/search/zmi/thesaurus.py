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

from pyams_content.component.thesaurus import ICollectionsManager, ITagsManager, IThemesManager
from pyams_content.feature.search import ISearchFolder
from pyams_content.shared.view.interfaces.settings import IViewCollectionsSettings, IViewTagsSettings, \
    IViewThemesSettings
from pyams_content.shared.view.zmi.thesaurus import ViewCollectionsEditForm, ViewTagsEditForm, ViewThemesEditForm
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_thesaurus.zmi.widget import ThesaurusTermsTreeFieldWidget

__docformat__ = 'restructuredtext'

from pyams_content import _


@ajax_form_config(name='tags.html',
                  context=ISearchFolder, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class SearchFolderTagsEditForm(ViewTagsEditForm):
    """Search folder tags settings edit form"""

    title = _("Tags settings")
    legend = _("Search folder tags settings")

    fields = Fields(IViewTagsSettings).select('tags')
    fields['tags'].widget_factory = ThesaurusTermsTreeFieldWidget

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        tags = self.widgets.get('tags')
        if tags is not None:
            tags.label_css_class = 'hidden'
            manager = ITagsManager(self.request.root, None)
            if manager is not None:
                tags.thesaurus_name = manager.thesaurus_name
                tags.extract_name = manager.extract_name


@ajax_form_config(name='themes.html',
                  context=ISearchFolder, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class SearchFolderThemesEditForm(ViewThemesEditForm):
    """Search folder themes settings edit form"""

    title = _("Themes settings")
    legend = _("Search folder themes settings")

    fields = Fields(IViewThemesSettings).select('themes')
    fields['themes'].widget_factory = ThesaurusTermsTreeFieldWidget

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        themes = self.widgets.get('themes')
        if themes is not None:
            themes.label_css_class = 'hidden'
            manager = IThemesManager(self.request.root, None)
            if manager is not None:
                themes.thesaurus_name = manager.thesaurus_name
                themes.extract_name = manager.extract_name


@ajax_form_config(name='collections.html',
                  context=ISearchFolder, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class SearchFolderCollectionsEditForm(ViewCollectionsEditForm):
    """Search folder collections settings edit form"""

    title = _("Collections settings")
    legend = _("Search folder collections settings")

    fields = Fields(IViewCollectionsSettings).select('collections')
    fields['collections'].widget_factory = ThesaurusTermsTreeFieldWidget

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        collections = self.widgets.get('collections')
        if collections is not None:
            collections.label_css_class = 'hidden'
            manager = ICollectionsManager(self.request.root, None)
            if manager is not None:
                collections.thesaurus_name = manager.thesaurus_name
                collections.extract_name = manager.extract_name
