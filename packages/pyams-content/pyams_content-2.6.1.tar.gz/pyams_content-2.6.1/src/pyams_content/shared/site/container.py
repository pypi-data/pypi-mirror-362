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

"""PyAMS_content.shared.site.container module

This module provides base site container mixin class
"""

import json

from pyramid.location import lineage
from zope.interface import implementer
from zope.intid import IIntIds
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_content.shared.site.interfaces import IBaseSiteItem, ISiteContainer, \
    ISiteElementNavigation, ISiteFolder, ISiteManager, SITE_CONTENT_VOCABULARY
from pyams_i18n.interfaces import II18n
from pyams_utils.finder import find_objects_providing
from pyams_utils.registry import get_pyramid_registry, get_utility
from pyams_utils.request import check_request, query_request
from pyams_utils.traversing import get_parent
from pyams_utils.vocabulary import vocabulary_config


__docformat__ = 'restructuredtext'


@implementer(ISiteContainer)
class SiteContainerMixin:
    """Site container mixin class"""

    def get_visible_items(self, request=None):

        def check_item(item):
            navigation = registry.queryMultiAdapter((item, request), ISiteElementNavigation)
            return (navigation is not None) and navigation.visible

        if request is None:
            request = check_request()
        registry = get_pyramid_registry()
        yield from filter(check_item, self.values())

    def get_folders_tree(self, selected=None, permission=None):

        request = query_request()
        intids = get_utility(IIntIds)

        def get_folder_items(parent, input):
            for folder in parent.values():
                if ISiteFolder.providedBy(folder):
                    if permission is not None:
                        can_select = request.has_permission(permission, context=folder)
                    else:
                        can_select = True
                    value = {
                        'id': intids.queryId(folder),
                        'text': II18n(folder).query_attribute('title', request=request),
                        'state': {
                            'expanded': folder in lineage(self),
                            'selected': folder is selected
                        },
                        'selectable': can_select
                    }
                    items = get_folder_items(folder, [])
                    if items:
                        value['nodes'] = items
                    input.append(value)
            return input

        # get child folders
        items = get_folder_items(self, [])

        # get parents folders
        container = self
        while ISiteContainer.providedBy(container):
            can_select = request.has_permission(permission, context=container) \
                if permission is not None else True
            items = [{
                'id': intids.queryId(container),
                'text': II18n(container).query_attribute('title', request=request),
                'state': {
                    'expanded': True,
                    'selected': container is selected
                },
                'selectable': can_select,
                'nodes': items
            }]
            container = container.__parent__

        return json.dumps(items)


@vocabulary_config(name=SITE_CONTENT_VOCABULARY)
class SiteManagerContentsVocabulary(SimpleVocabulary):
    """Site manager folders vocabulary"""

    def __init__(self, context):
        terms = []
        site = get_parent(context, ISiteManager)
        if site is not None:
            request = query_request()
            intids = get_utility(IIntIds)
            for folder, depth in find_objects_providing(site, IBaseSiteItem, with_depth=True):
                terms.append(SimpleTerm(value=intids.queryId(folder),
                                        title='{}{}'.format(
                                            '- ' * depth,
                                            II18n(folder).query_attribute('title',
                                                                          request=request))))
        super(SiteManagerContentsVocabulary, self).__init__(terms)
