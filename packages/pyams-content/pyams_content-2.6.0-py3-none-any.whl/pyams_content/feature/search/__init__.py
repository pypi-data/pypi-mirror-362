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

"""PyAMS_content.feature.search module

This module defines search folder class and adapters.
"""

from zope.interface import implementer
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.illustration.interfaces import IIllustrationTarget, ILinkIllustrationTarget
from pyams_content.feature.preview.interfaces import IPreviewTarget
from pyams_content.feature.search.interfaces import ISearchFolder
from pyams_content.interfaces import MANAGE_SITE_PERMISSION
from pyams_content.shared.view import WfView
from pyams_portal.interfaces import IPortalContext, IPortalFooterContext, IPortalHeaderContext
from pyams_security.interfaces import IDefaultProtectionPolicy, IViewContextPermissionChecker
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.factory import factory_config
from pyams_workflow.interfaces import IWorkflowPublicationSupport

from pyams_content import _


@factory_config(ISearchFolder)
@implementer(IDefaultProtectionPolicy, IWorkflowPublicationSupport,
             IIllustrationTarget, ILinkIllustrationTarget,
             IPortalContext, IPortalHeaderContext, IPortalFooterContext, IPreviewTarget)
class SearchFolder(WfView):
    """Search folder"""

    content_name = _("Search folder")

    handle_short_name = True
    handle_content_url = False
    handle_header = True
    handle_description = True

    sequence_name = ''  # use default sequence generator
    sequence_prefix = ''

    order_by = FieldProperty(ISearchFolder['order_by'])
    visible_in_list = FieldProperty(ISearchFolder['visible_in_list'])
    navigation_title = FieldProperty(ISearchFolder['navigation_title'])

    selected_content_types = FieldProperty(ISearchFolder['selected_content_types'])
    selected_datatypes = FieldProperty(ISearchFolder['selected_datatypes'])

    @staticmethod
    def is_deletable():
        return True


@adapter_config(required=ISearchFolder,
                provides=IViewContextPermissionChecker)
class SearchFolderPermissionChecker(ContextAdapter):
    """Search folder permission checker"""

    edit_permission = MANAGE_SITE_PERMISSION
