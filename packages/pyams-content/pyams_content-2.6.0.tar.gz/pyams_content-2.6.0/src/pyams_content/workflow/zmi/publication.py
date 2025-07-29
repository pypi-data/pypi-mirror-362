#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.workflow.zmi.publication module

"""

from datetime import datetime, timezone

from pyams_content.interfaces import MANAGE_SITE_PERMISSION
from pyams_content.shared.common import IWfSharedContent
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer
from pyams_layer.interfaces import IPyAMSLayer
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.interfaces.form import NO_VALUE
from pyams_utils.timezone import tztime
from pyams_viewlet.viewlet import viewlet_config
from pyams_workflow.interfaces import IWorkflowPublicationInfo, IWorkflowPublicationSupport
from pyams_zmi.form import AdminEditForm
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IPropertiesMenu
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_content import _


@viewlet_config(name='workflow-publication.menu',
                context=IWorkflowPublicationSupport, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=510,
                permission=MANAGE_SITE_PERMISSION)
class SiteItemPublicationDatesMenu(NavigationMenuItem):
    """Site item publication dates menu"""

    label = _("Publication dates")
    href = '#workflow-publication.html'

    def __new__(cls, context, request, view, manager):
        if IWfSharedContent.providedBy(context):
            return None
        return NavigationMenuItem.__new__(cls)


@ajax_form_config(name='workflow-publication.html',
                  context=IWorkflowPublicationSupport, layer=IPyAMSLayer,
                  permission=MANAGE_SITE_PERMISSION)
class SiteItemPublicationDatesEditForm(AdminEditForm):
    """Site item publication dates edit form"""

    title = _("Workflow management")
    legend = _("Content publication dates")

    fields = Fields(IWorkflowPublicationInfo).select('publication_effective_date',
                                                     'publication_expiration_date')

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        effective_date = self.widgets.get('publication_effective_date')
        if (effective_date is not None) and not effective_date.value:
            value = effective_date.extract()
            if value is NO_VALUE:
                pub_info = IWorkflowPublicationInfo(self.context)
                if (pub_info is not None) and \
                        (pub_info.first_publication_date is None) and \
                        (pub_info.publication_effective_date is None):
                    effective_date.value = tztime(datetime.now(timezone.utc))


@adapter_config(required=(IWorkflowPublicationSupport, IAdminLayer, SiteItemPublicationDatesEditForm),
                provides=IAJAXFormRenderer)
class SiteItemPublicationDatesEditFormRenderer(ContextRequestViewAdapter):
    """Site item publication dates edit form renderer"""

    def render(self, changes):
        """Changes renderer"""
        if not changes:
            return None
        return {
            'status': 'reload'
        }
