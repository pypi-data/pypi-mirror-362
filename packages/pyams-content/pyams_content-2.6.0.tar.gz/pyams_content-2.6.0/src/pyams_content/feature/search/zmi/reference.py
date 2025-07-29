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

__docformat__ = 'restructuredtext'

from pyams_content.feature.search import ISearchFolder
from pyams_form.ajax import ajax_form_config
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import FORBIDDEN_PERMISSION, VIEW_SYSTEM_PERMISSION
from pyams_utils.adapter import NullAdapter
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IPropertiesMenu


@viewlet_config(name='references.divider',
                context=ISearchFolder, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=299,
                permission=VIEW_SYSTEM_PERMISSION)
class SearchFolderReferencesMenuDivider(NullAdapter):
    """Search folder references menu divider"""


@viewlet_config(name='references.menu',
                context=ISearchFolder, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=300,
                permission=VIEW_SYSTEM_PERMISSION)
class VSearchFolderReferencesMenu(NullAdapter):
    """Search folder references menu"""


@ajax_form_config(name='references.html',
                  context=ISearchFolder, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class SearchFolderReferencesEditForm(NullAdapter):
    """Search folder references settings edit form"""

    _edit_permission = FORBIDDEN_PERMISSION
