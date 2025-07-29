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

"""PyAMS_content.features.redirect module

This module is used to handle HTTP NotFound errors. It is specially useful
when you are migrating an old site to a new architecture and you want to redirect
users to new pages based on their previous URLs.

It is based on a custom NotFound exception view handler, which relies on a
"redirect manager" which can use regular expressions to analyze initial request and
provide redirection URLs.
"""

import re
from persistent import Persistent
from zope.container.contained import Contained
from zope.schema.fieldproperty import FieldProperty

from pyams_content.feature.redirect.interfaces import IRedirectionRule
from pyams_content.interfaces import MANAGE_SITE_ROOT_PERMISSION
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_sequence.reference import InternalReferenceMixin
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.factory import factory_config
from pyams_utils.url import canonical_url
from pyams_utils.zodb import volatile_property

__docformat__ = 'restructuredtext'



@factory_config(IRedirectionRule)
class RedirectionRule(InternalReferenceMixin, Persistent, Contained):
    """Redirection rule persistent class"""

    active = FieldProperty(IRedirectionRule['active'])
    chained = FieldProperty(IRedirectionRule['chained'])
    label = FieldProperty(IRedirectionRule['label'])
    permanent = FieldProperty(IRedirectionRule['permanent'])
    _url_pattern = FieldProperty(IRedirectionRule['url_pattern'])
    reference = FieldProperty(IRedirectionRule['reference'])
    target_url = FieldProperty(IRedirectionRule['target_url'])
    notepad = FieldProperty(IRedirectionRule['notepad'])

    @property
    def url_pattern(self):
        return self._url_pattern

    @url_pattern.setter
    def url_pattern(self, value):
        if value != self._url_pattern:
            self._url_pattern = value
            del self.pattern

    @volatile_property
    def pattern(self):
        return re.compile(self.url_pattern)

    def match(self, source_url):
        return self.pattern.match(source_url)

    def rewrite(self, source_url, request):
        target_url = None
        if self.reference:
            target = self.target
            if target is not None:
                target_url = canonical_url(target, request)
        else:
            target_url = self.pattern.sub(self.target_url, source_url)
        return target_url


@adapter_config(required=IRedirectionRule,
                provides=IViewContextPermissionChecker)
class RedirectionRulePermissionChecker(ContextAdapter):
    """Redirection rule permission checker"""

    edit_permission = MANAGE_SITE_ROOT_PERMISSION
