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

"""PyAMS_content.feature.redirect.container module

This module defines main redirection rules container and manager.
"""

from pyramid.httpexceptions import HTTPMovedPermanently, HTTPFound
from pyramid.response import Response
from zope.location.interfaces import ISublocations
from zope.traversing.interfaces import ITraversable

from pyams_content.feature.redirect.interfaces import IRedirectionManager, IRedirectionManagerTarget, \
    REDIRECT_MANAGER_KEY
from pyams_utils.adapter import ContextAdapter, adapter_config, get_annotation_adapter
from pyams_utils.container import BTreeOrderedContainer
from pyams_utils.factory import factory_config

__docformat__ = 'restructuredtext'

from pyams_content import _


@factory_config(IRedirectionManager)
class RedirectionManager(BTreeOrderedContainer):
    """Redirection manager class"""

    def get_active_items(self):
        yield from filter(lambda x: x.active, self.values())

    def get_response(self, request):
        target_url = request.path_qs
        for rule in self.get_active_items():
            if rule.match(target_url):
                target_url = rule.rewrite(target_url, request)
                if not rule.chained:
                    return Response(status_code=HTTPMovedPermanently.code if rule.permanent else HTTPFound.code,
                                    location=target_url)
        return None

    def test_rules(self, source_url, request, check_inactive_rules=False):
        if check_inactive_rules:
            rules = self.values()
        else:
            rules = self.get_active_items()
        for rule in rules:
            match = rule.match(source_url)
            if match:
                target_url = rule.rewrite(source_url, request)
                yield rule, source_url, target_url
                if not rule.chained:
                    return
                source_url = target_url
            else:
                yield rule, source_url, request.localizer.translate(_("not matching"))


@adapter_config(required=IRedirectionManagerTarget,
                provides=IRedirectionManager)
def redirection_manager_factory(context):
    """Redirection manager factory"""
    return get_annotation_adapter(context, REDIRECT_MANAGER_KEY, IRedirectionManager,
                                  name='++redirect++')


@adapter_config(name='redirect',
                required=IRedirectionManagerTarget,
                provides=ITraversable)
class RedirectionManagerNamespace(ContextAdapter):
    """Redirection manager ++redirect++ namespace"""

    def traverse(self, name, furtherpath=None):
        return IRedirectionManager(self.context, None)


@adapter_config(name='redirect',
                required=IRedirectionManagerTarget,
                provides=ISublocations)
class RedirectManagerSublocations(ContextAdapter):
    """redirection manager sub-locations adapter"""

    def sublocations(self):
        yield from IRedirectionManager(self.context).values()
