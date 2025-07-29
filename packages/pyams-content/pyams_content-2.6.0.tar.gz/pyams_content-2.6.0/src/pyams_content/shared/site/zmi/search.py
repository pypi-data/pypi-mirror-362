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

"""PyAMS_content.shared.site.zmi.search module

This module defines custom components which are used to handle searching
inside a site manager.
"""

from pyams_content.shared.common.zmi.dashboard import SharedToolDashboardView
from pyams_content.shared.common.zmi.search import SharedToolAdvancedSearchResultsView, \
    SharedToolQuickSearchView
from pyams_content.shared.site.interfaces import ISiteFolder, ISiteManager
from pyams_i18n.interfaces import II18n
from pyams_skin.interfaces.viewlet import IHeaderViewletManager
from pyams_utils.adapter import adapter_config
from pyams_viewlet.viewlet import EmptyViewlet, viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.table import IInnerTable


__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(name='quick-search',
                required=(ISiteManager, IAdminLayer, SharedToolDashboardView),
                provides=IInnerTable)
class SiteManagerQuickSearchView(SharedToolQuickSearchView):
    """Site manager quick search view"""

    @property
    def legend(self):
        """Legend getter"""
        translate = self.request.localizer.translate
        return translate(_("Between all contents of « {} » site manager")) \
            .format(II18n(self.context).query_attribute('title', request=self.request))


@adapter_config(name='quick-search',
                required=(ISiteFolder, IAdminLayer, SharedToolDashboardView),
                provides=IInnerTable)
class SiteFolderQuickSearchView(SharedToolQuickSearchView):
    """Site folder quick search view"""

    @property
    def legend(self):
        """Legend getter"""
        translate = self.request.localizer.translate
        return translate(_("Between all contents of « {} » site folder")) \
            .format(II18n(self.context).query_attribute('title', request=self.request))


@viewlet_config(name='workflow-status',
                context=ISiteManager, layer=IAdminLayer, view=SharedToolAdvancedSearchResultsView,
                manager=IHeaderViewletManager, weight=20)
class SiteManagerSearchResultsStatusViewlet(EmptyViewlet):
    """Site manager advanced search results header viewlet"""
