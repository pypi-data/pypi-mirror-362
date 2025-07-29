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

"""PyAMS_content.shared.portal module

"""

from pyams_content.shared.common import IBaseSharedTool
from pyams_content.shared.common.interfaces import IBaseContentPortalContext, \
    ISharedContentPortalPage
from pyams_portal.interfaces import IPortalPage, PORTAL_PAGE_KEY
from pyams_portal.page import PortalPage
from pyams_portal.utils import get_portal_page
from pyams_utils.adapter import adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.traversing import get_parent
from pyams_utils.zodb import volatile_property

__docformat__ = 'restructuredtext'


class SharedContentPortalPageMixin:
    """Shared content portal page mixin class"""

    @volatile_property
    def can_inherit(self):
        page = get_portal_page(self.parent, page_name=self.name)
        return page.template is not None

    @property
    def parent(self):
        return get_parent(self, IBaseSharedTool, allow_context=False)


#
# SHared content portal page
#

@factory_config(ISharedContentPortalPage)
class SharedContentPortalPage(SharedContentPortalPageMixin, PortalPage):
    """Shared content portal page"""


@adapter_config(required=IBaseContentPortalContext,
                provides=IPortalPage)
def shared_content_portal_page(context, page_name=''):
    """Shared content portal page adapter"""

    def set_page_name(page):
        """Set page name after creation"""
        page.name = page_name

    key = f'{PORTAL_PAGE_KEY}::{page_name}' if page_name else PORTAL_PAGE_KEY
    return get_annotation_adapter(context, key, ISharedContentPortalPage,
                                  name=f'++page++{page_name}',
                                  callback=set_page_name)


@adapter_config(name='header',
                required=IBaseContentPortalContext,
                provides=IPortalPage)
def shared_content_portal_page_header(context):
    """Shared content portal page header adapter"""
    return shared_content_portal_page(context, page_name='header')


@adapter_config(name='footer',
                required=IBaseContentPortalContext,
                provides=IPortalPage)
def shared_content_portal_page_footer(context):
    """Shared content portal page footer adapter"""
    return shared_content_portal_page(context, page_name='footer')
