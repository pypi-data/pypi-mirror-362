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

"""PyAMS_*** module

"""

__docformat__ = 'restructuredtext'

from pyams_content import _
from pyams_content.feature.search.interfaces import ISearchManagerInfo
from pyams_content.interfaces import MANAGE_SITE_ROOT_PERMISSION
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IGroup
from pyams_layer.interfaces import IPyAMSLayer
from pyams_site.interfaces import ISiteRoot
from pyams_utils.adapter import adapter_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminEditForm, FormGroupChecker
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IPropertiesMenu
from pyams_zmi.zmi.viewlet.menu import NavigationMenuDivider, NavigationMenuItem


@viewlet_config(name='search.divider',
                context=ISiteRoot, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=799,
                permission=MANAGE_SITE_ROOT_PERMISSION)
class SearchManagerMenuDivider(NavigationMenuDivider):
    """Search manager menu divider"""


@viewlet_config(name='search-manager.menu',
                context=ISiteRoot, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=800,
                permission=MANAGE_SITE_ROOT_PERMISSION)
class SearchManagerMenu(NavigationMenuItem):
    """Search manager menu"""

    label = _("Search settings")
    href = '#search-manager.html'


@ajax_form_config(name='search-manager.html',
                  context=ISiteRoot, layer=IPyAMSLayer,
                  permission=MANAGE_SITE_ROOT_PERMISSION)
class SearchManagerPropertiesEditForm(AdminEditForm):
    """Search manager properties edit form"""

    title = _("Search settings")
    legend = _("General search settings")

    fields = Fields(ISearchManagerInfo).select('reference', 'name', 'description')


@adapter_config(name='search-manager-tags-group',
                required=(ISiteRoot, IAdminLayer, SearchManagerPropertiesEditForm),
                provides=IGroup)
class SearchManagerTagsGroup(FormGroupChecker):
    """Search manager tags group"""

    fields = Fields(ISearchManagerInfo).select('enable_tags_search', 'tags_search_target')

    weight = 10


@adapter_config(name='search-manager-collections-group',
                required=(ISiteRoot, IAdminLayer, SearchManagerPropertiesEditForm),
                provides=IGroup)
class SearchManagerCollectionsGroup(FormGroupChecker):
    """Search manager collections group"""

    fields = Fields(ISearchManagerInfo).select('enable_collections_search', 'collections_search_target')

    weight = 20
