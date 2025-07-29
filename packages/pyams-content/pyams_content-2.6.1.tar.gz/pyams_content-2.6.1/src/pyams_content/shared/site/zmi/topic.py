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

"""PyAMS_content.shared.site.zmi.topic module

This module defines sites topics management components.
"""

from zope.intid.interfaces import IIntIds
from zope.schema import Int

from pyams_content.interfaces import CREATE_CONTENT_PERMISSION
from pyams_content.shared.common.zmi import SharedContentAddForm
from pyams_content.shared.site.interfaces import ISiteContainer, ISiteManager, ISiteTopic, IWfSiteTopic
from pyams_content.shared.site.zmi.interfaces import ISiteTreeTable
from pyams_content.shared.site.zmi.widget.folder import SiteManagerFoldersSelectorFieldWidget
from pyams_content.zmi.interfaces import IDashboardColumn, IDashboardContentVisibility
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_layer.interfaces import IPyAMSLayer
from pyams_skin.viewlet.menu import MenuItem
from pyams_utils.adapter import NullAdapter, adapter_config
from pyams_utils.registry import get_utility
from pyams_utils.url import absolute_url
from pyams_viewlet.viewlet import viewlet_config
from pyams_workflow.interfaces import IWorkflowVersions
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.table import ITableElementEditor
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager, IToolbarViewletManager
from pyams_zmi.table import TableElementEditor

__docformat__ = 'restructuredtext'

from pyams_content import _


@viewlet_config(name='add-content.action',
                context=ISiteManager, layer=IAdminLayer,
                manager=IToolbarViewletManager, weight=10)
class SiteManagerContentAddAction(NullAdapter):
    """Site manager add action"""


class ISiteTopicAddFormFields(IWfSiteTopic):
    """Site topic add form fields"""

    parent = Int(title=_("Parent"),
                 description=_("Topic's parent"),
                 required=True)


@adapter_config(required=IWfSiteTopic,
                provides=ISiteTopicAddFormFields)
def site_topic_add_form_fields_adapter(context):
    """Site topic add form fields adapter"""
    return context


@viewlet_config(name='add-site-topic.action',
                context=ISiteContainer, layer=IAdminLayer, view=ISiteTreeTable,
                manager=IContextAddingsViewletManager, weight=20,
                permission=CREATE_CONTENT_PERMISSION)
class SiteContainerTopicAddMenuItem(MenuItem):
    """Site container topic add menu item"""

    label = _("Add site topic...")
    icon_class = 'far fa-file'

    href = 'add-site-topic.html'
    modal_target = True


@ajax_form_config(name='add-site-topic.html',
                  context=ISiteContainer, layer=IPyAMSLayer,
                  permission=CREATE_CONTENT_PERMISSION)
class SiteContainerTopicAddForm(SharedContentAddForm):
    """Site container topic add form"""

    fields = Fields(ISiteTopicAddFormFields).select('title', 'data_type', 'parent', 'notepad')
    fields['parent'].widget_factory = SiteManagerFoldersSelectorFieldWidget

    @property
    def container_target(self):
        """new content container getter"""
        return self.__parent if self.__parent is not None else self.context

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        if 'parent' in self.widgets:
            self.widgets['parent'].permission = CREATE_CONTENT_PERMISSION

    def update_content(self, obj, data):
        data = data.get(self, data)
        # initialize new topic
        intids = get_utility(IIntIds)
        self.__parent = intids.queryObject(data.pop('parent'))
        super().update_content(obj, data)

    def next_url(self):
        """Redirect URL getter"""
        return absolute_url(self.__parent, self.request,
                            f'{self.__uuid}/++versions++/1/admin')


@adapter_config(required=(ISiteTopic, IAdminLayer, ISiteTreeTable),
                provides=ITableElementEditor)
class SiteTopicTableElementEditor(TableElementEditor):
    """Site topic table element editor"""

    view_name = 'admin'
    modal_target = False

    @property
    def href(self):
        """Target URL getter"""
        versions = IWorkflowVersions(self.context)
        version = versions.get_last_versions(1)[0]
        return absolute_url(version, self.request, self.view_name)


@adapter_config(required=(ISiteTopic, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentVisibility)
def site_topic_dashboard_visibility(context, request, column):
    """Site topic dashboard visibility"""
    return column.has_permission(context), ''
