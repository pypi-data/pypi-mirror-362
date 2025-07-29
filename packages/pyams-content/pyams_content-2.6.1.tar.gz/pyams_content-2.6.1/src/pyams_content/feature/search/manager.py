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

"""PyAMS_*** module

"""

__docformat__ = 'restructuredtext'

from persistent import Persistent
from zope.container.contained import Contained
from zope.schema.fieldproperty import FieldProperty

from pyams_content.feature.search.interfaces import ISearchManagerInfo
from pyams_sequence.reference import get_reference_target
from pyams_site.interfaces import ISiteRoot
from pyams_utils.adapter import adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.zodb import volatile_property

SEARCH_MANAGER_INFO_KEY = 'pyams_content.search'


@factory_config(ISearchManagerInfo)
class SearchManagerInfo(Persistent, Contained):
    """Search manager persistent info"""

    _reference = FieldProperty(ISearchManagerInfo['reference'])
    name = FieldProperty(ISearchManagerInfo['name'])
    description = FieldProperty(ISearchManagerInfo['description'])

    enable_tags_search = FieldProperty(ISearchManagerInfo['enable_tags_search'])
    _tags_search_target = FieldProperty(ISearchManagerInfo['tags_search_target'])

    enable_collections_search = FieldProperty(ISearchManagerInfo['enable_collections_search'])
    _collections_search_target = FieldProperty(ISearchManagerInfo['collections_search_target'])

    # main search target

    @property
    def reference(self):
        return self._reference

    @reference.setter
    def reference(self, value):
        self._reference = value
        del self.search_target

    @volatile_property
    def search_target(self):
        return get_reference_target(self._reference)

    # tags search target

    @property
    def tags_search_target(self):
        return self._tags_search_target

    @tags_search_target.setter
    def tags_search_target(self, value):
        self._tags_search_target = value
        del self.tags_target

    @volatile_property
    def tags_target(self):
        if self.enable_tags_search:
            return get_reference_target(self._tags_search_target)
        return None

    # collections search target

    @property
    def collections_search_target(self):
        return self._collections_search_target

    @collections_search_target.setter
    def collections_search_target(self, value):
        self._collections_search_target = value
        del self.collections_target

    @volatile_property
    def collections_target(self):
        if self.enable_collections_search:
            return get_reference_target(self._collections_search_target)
        return None

    @property
    def references(self):
        return list(filter(lambda x: x is not None, [self.reference,
                                                     self.tags_search_target,
                                                     self.collections_search_target]))

    use_references_for_views = False

    def get_targets(self, state=None):
        for reference in [self.reference, self.tags_search_target, self.collections_search_target]:
            if reference is not None:
                yield get_reference_target(reference, state)


@adapter_config(required=ISiteRoot,
                provides=ISearchManagerInfo)
def site_root_search_manager_info(context):
    """Site root search manager adapter"""
    return get_annotation_adapter(context, SEARCH_MANAGER_INFO_KEY, ISearchManagerInfo)
