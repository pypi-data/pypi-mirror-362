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

"""PyAMS_content.shared.common.skin.url module

This module defines adapters used to manage shared contents canonical
and relative URLs.
"""

from pyramid.encode import urlencode, url_quote
from pyramid.url import QUERY_SAFE

from pyams_content.shared.common import ISharedContent, IWfSharedContent
from pyams_content.shared.common.interfaces.types import IWfTypedSharedContent
from pyams_layer.interfaces import IPyAMSUserLayer
from pyams_sequence.interfaces import ISequentialIdInfo
from pyams_utils.adapter import ContextRequestAdapter, adapter_config
from pyams_utils.interfaces.url import ICanonicalURL, IRelativeURL
from pyams_utils.url import absolute_url, canonical_url, relative_url

__docformat__ = 'restructuredtext'


def get_quoted_query(query):
    """Query checker"""
    if not query:
        return None
    if isinstance(query, str):
        return url_quote(query, QUERY_SAFE)
    return urlencode(query, doseq=True)


#
# Canonical URL adapters
#

@adapter_config(required=(IWfSharedContent, IPyAMSUserLayer),
                provides=ICanonicalURL)
class WfSharedContentCanonicalURL(ContextRequestAdapter):
    """Workflow managed shared content canonical URL adapter"""

    def get_url(self, view_name=None, query=None):
        """Canonical URL getter"""
        query = get_quoted_query(query)
        return absolute_url(self.request.root, self.request,
                            f"+/{ISequentialIdInfo(self.context).get_base_oid().strip()}"
                            f"::{self.context.content_url}"
                            f"{'/{}'.format(view_name) if view_name else '.html'}"
                            f"{'?{}'.format(query) if query else ''}")


@adapter_config(required=(IWfTypedSharedContent, IPyAMSUserLayer),
                provides=ICanonicalURL)
class WfTypedSharedContentCanonicalURL(WfSharedContentCanonicalURL):
    """Typed shared content canonical URL adapter"""

    def get_url(self, view_name=None, query=None):
        data_type = self.context.get_data_type()
        if data_type is not None:
            source = data_type.get_source_folder()
            if source is not None:
                return absolute_url(source, self.request,
                                    f"+/{ISequentialIdInfo(self.context).get_base_oid().strip()}"
                                    f"::{self.context.content_url}"
                                    f"{'/{}'.format(view_name) if view_name else '.html'}"
                                    f"{'?{}'.format(query) if query else ''}")
        return super().get_url(view_name, query)


@adapter_config(required=(ISharedContent, IPyAMSUserLayer),
                provides=ICanonicalURL)
class SharedContentCanonicalURL(ContextRequestAdapter):
    """Shared content canonical URL"""

    def get_url(self, display_context=None, view_name=None, query=None):
        """Canonical URL getter"""
        version = self.context.visible_version
        if version is not None:
            return canonical_url(version, self.request, view_name, query)
        return None


#
# Relative URL adapters
#

@adapter_config(required=(IWfSharedContent, IPyAMSUserLayer),
                provides=IRelativeURL)
class WfSharedContentRelativeURL(ContextRequestAdapter):
    """Workflow managed shared content relative URL adapter"""

    def get_url(self, display_context=None, view_name=None, query=None):
        """Relative URL getter"""
        query = get_quoted_query(query)
        return absolute_url(display_context, self.request,
                            f"+/{ISequentialIdInfo(self.context).get_base_oid().strip()}"
                            f"::{self.context.content_url}"
                            f"{'/{}'.format(view_name) if view_name else '.html'}"
                            f"{'?{}'.format(query) if query else ''}")


@adapter_config(required=(ISharedContent, IPyAMSUserLayer),
                provides=IRelativeURL)
class SharedContentRelativeURL(ContextRequestAdapter):
    """Shared content relative URL"""

    def get_url(self, display_context=None, view_name=None, query=None):
        """Relative URL getter"""
        version = self.context.visible_version
        if version is not None:
            return relative_url(version, self.request, display_context, view_name, query)
        return None
