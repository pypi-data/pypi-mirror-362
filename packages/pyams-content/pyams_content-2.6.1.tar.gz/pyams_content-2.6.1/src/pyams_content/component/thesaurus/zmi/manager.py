#
# Copyright (c) 2015-2022 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.component.thesaurus.zmi.manager module

This module defines management components for thesaurus manager related forms.
"""

from zope.interface import alsoProvides

from pyams_content.component.thesaurus import ICollectionsManager, ICollectionsManagerTarget, \
    ITagsManager, ITagsManagerTarget, IThemesManager, IThemesManagerTarget
from pyams_content.interfaces import MANAGE_SITE_ROOT_PERMISSION
from pyams_content.zmi import content_js
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IFormContent, IGroup
from pyams_layer.interfaces import IPyAMSLayer
from pyams_utils.adapter import adapter_config
from pyams_utils.fanstatic import get_resource_path
from pyams_utils.interfaces.data import IObjectData
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminEditForm, FormGroupChecker
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IPropertiesMenu
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_content import _


class BaseThesaurusManagerEditForm(AdminEditForm):
    """Base thesaurus manager edit form"""

    def update_widgets(self, prefix=None):
        # store thesaurus name in request header to be able to set
        # extract name correctly
        if self.request.method == 'POST':
            name = f'{self.prefix}widgets.thesaurus_name'
            value = self.request.params.get(name)
            if value is not None:
                self.request.headers['X-Thesaurus-Name'] = value
        super().update_widgets(prefix)
        name = self.widgets.get('thesaurus_name')
        if name is not None:
            name.object_data = {
                'ams-modules': {
                    'content': {
                        'src': get_resource_path(content_js)
                    }
                },
                'ams-change-handler': 'MyAMS.content.thesaurus.changeThesaurus'
            }
            alsoProvides(name, IObjectData)


#
# Tags management
#

@viewlet_config(name='tags-manager.menu',
                context=ITagsManagerTarget, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=730,
                permission=MANAGE_SITE_ROOT_PERMISSION)
class TagsManagerMenu(NavigationMenuItem):
    """Tags manager menu"""

    label = _("Tags settings")
    href = '#tags-manager.html'


@ajax_form_config(name='tags-manager.html',
                  context=ITagsManagerTarget, layer=IPyAMSLayer,
                  permission=MANAGE_SITE_ROOT_PERMISSION)
class TagsManagerEditForm(BaseThesaurusManagerEditForm):
    """Tags manager properties edit form"""

    title = _("Tags settings")
    legend = _("Selected tags thesaurus")

    fields = Fields(ITagsManager).select('thesaurus_name', 'extract_name')


@adapter_config(required=(ITagsManagerTarget, IAdminLayer, TagsManagerEditForm),
                provides=IFormContent)
def tags_manager_edit_form_content(context, request, form):
    """Tags manager edit form content getter"""
    return ITagsManager(context)


@adapter_config(name='glossary',
                required=(ITagsManagerTarget, IAdminLayer, TagsManagerEditForm),
                provides=IGroup)
class TagsManagerGlossaryGroup(FormGroupChecker):
    """Tags manager glossary group"""

    fields = Fields(ITagsManager).select('enable_glossary', 'glossary_thesaurus_name')
    checker_fieldname = 'enable_glossary'
    checker_mode = 'hide'


@adapter_config(required=(ITagsManagerTarget, IAdminLayer, TagsManagerGlossaryGroup),
                provides=IFormContent)
def tags_manager_glossary_group_content(context, request, group):
    """Tags manager glossary edit form group content getter"""
    return ITagsManager(context)


#
# Themes management
#

@viewlet_config(name='themes-manager.menu',
                context=IThemesManagerTarget, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=740,
                permission=MANAGE_SITE_ROOT_PERMISSION)
class ThemesManagerMenu(NavigationMenuItem):
    """Themes manager menu"""

    label = _("Themes settings")
    href = '#themes-manager.html'


@ajax_form_config(name='themes-manager.html',
                  context=IThemesManagerTarget, layer=IPyAMSLayer,
                  permission=MANAGE_SITE_ROOT_PERMISSION)
class ThemesManagerEditForm(BaseThesaurusManagerEditForm):
    """Themes manager properties edit form"""

    title = _("Themes settings")
    legend = _("Selected themes thesaurus")

    fields = Fields(IThemesManager)


@adapter_config(required=(IThemesManagerTarget, IAdminLayer, ThemesManagerEditForm),
                provides=IFormContent)
def themes_manager_edit_form_content(context, request, group):
    """Themes manager edit form content getter"""
    return IThemesManager(context)


#
# Collections management
#

@viewlet_config(name='collections-manager.menu',
                context=ICollectionsManagerTarget, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=750,
                permission=MANAGE_SITE_ROOT_PERMISSION)
class CollectionsManagerMenu(NavigationMenuItem):
    """Collections manager menu"""

    label = _("Collections settings")
    href = '#collections-manager.html'


@ajax_form_config(name='collections-manager.html',
                  context=ICollectionsManagerTarget, layer=IPyAMSLayer,
                  permission=MANAGE_SITE_ROOT_PERMISSION)
class CollectionsManagerEditForm(BaseThesaurusManagerEditForm):
    """Collections manager properties edit form"""

    title = _("Collections settings")
    legend = _("Selected collections thesaurus")

    fields = Fields(ICollectionsManager)


@adapter_config(required=(ICollectionsManagerTarget, IAdminLayer, CollectionsManagerEditForm),
                provides=IFormContent)
def collections_manager_edit_form_content(context, request, form):
    """Collections manager edit form content getter"""
    return ICollectionsManager(context)
