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

"""PyAMS_*** module

"""

from persistent import Persistent
from zope.container.contained import Contained
from zope.interface import Interface, implementer
from zope.schema.fieldproperty import FieldProperty

from pyams_content.feature.filter.interfaces import CONTENT_TYPE_FILTER_MODE, ICollectionsFilter, IContentTypesFilter, \
    IFilter, IFilterAggregate, ITagsFilter, IThemesFilter, IThesaurusFilter, ITitleFilter
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import MANAGE_TEMPLATE_PERMISSION
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.factory import factory_config
from pyams_utils.interfaces import ICacheKeyValue
from pyams_zmi.interfaces import IObjectLabel

__docformat__ = 'restructuredtext'


@implementer(IFilter)
class Filter(Persistent, Contained):
    """Base filter persistent class"""

    filter_type = None

    visible = FieldProperty(IFilter['visible'])
    label = FieldProperty(IFilter['label'])
    display_mode = FieldProperty(IFilter['display_mode'])
    open_state = FieldProperty(IFilter['open_state'])
    displayed_entries = FieldProperty(IFilter['displayed_entries'])
    labels_alignment = FieldProperty(IFilter['labels_alignment'])
    truncate_labels = FieldProperty(IFilter['truncate_labels'])
    display_count = FieldProperty(IFilter['display_count'])
    select_placeholder = FieldProperty(IFilter['select_placeholder'])
    sorting_mode = FieldProperty(IFilter['sorting_mode'])

    @property
    def filter_name(self):
        return ICacheKeyValue(self)


@adapter_config(required=(IFilter, IPyAMSLayer, Interface),
                provides=IObjectLabel)
def filter_label(context, request, view):  # pylint: disable=unused-argument
    """Filter label getter"""
    return II18n(context).get_attribute('label', request=request)


@adapter_config(required=IFilter,
                provides=IViewContextPermissionChecker)
class FilterPermissionChecker(ContextAdapter):
    """Filter permission checker"""

    edit_permission = MANAGE_TEMPLATE_PERMISSION


#
# Content-type filter
#

@factory_config(IContentTypesFilter)
class ContentTypesFilter(Filter):
    """Content-types filter """

    content_mode = FieldProperty(IContentTypesFilter['content_mode'])

    filter_type = CONTENT_TYPE_FILTER_MODE.FACET_LABEL.value


#
# Title filter
#

@factory_config(ITitleFilter)
class TitleFilter(Filter):
    """Title filter"""

    filter_type = 'title'


#
# Thesaurus-based filters
#

@implementer(IThesaurusFilter)
class ThesaurusFilter(Filter):
    """Thesaurus base filter"""

    sorting_mode = FieldProperty(IThesaurusFilter['sorting_mode'])

    thesaurus_name = FieldProperty(IThesaurusFilter['thesaurus_name'])
    extract_name = FieldProperty(IThesaurusFilter['extract_name'])
    

@factory_config(ITagsFilter)
class TagsFilter(ThesaurusFilter):
    """Tags filter"""

    filter_type = 'tag'


@factory_config(ICollectionsFilter)
class CollectionsFilter(ThesaurusFilter):
    """Collections filter"""

    filter_type = 'collection'


@factory_config(IThemesFilter)
class ThemesFilter(ThesaurusFilter):
    """Themes filter"""

    filter_type = 'theme'
