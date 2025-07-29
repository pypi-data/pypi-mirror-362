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

"""PyAMS_content.shared.common.types module

"""

from persistent import Persistent
from pyramid.events import subscriber
from zope.container.contained import Contained
from zope.container.ordered import OrderedContainer
from zope.interface import implementer
from zope.lifecycleevent import IObjectAddedEvent
from zope.location.interfaces import ISublocations
from zope.schema import getFieldsInOrder
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.traversing.interfaces import ITraversable

from pyams_content.component.extfile.interfaces import IExtFileContainerTarget
from pyams_content.component.links.interfaces import ILinkContainerTarget
from pyams_content.component.paragraph.interfaces import IParagraphContainerTarget
from pyams_content.component.thesaurus import ITagsInfo, ITagsTarget, IThemesInfo, IThemesTarget
from pyams_content.interfaces import MANAGE_TOOL_PERMISSION
from pyams_content.reference.pictogram import IPictogramTable
from pyams_content.shared.common.interfaces import ISharedTool
from pyams_content.shared.common.interfaces.types import ALL_DATA_TYPES_VOCABULARY, \
    DATA_MANAGER_ANNOTATION_KEY, DATA_TYPES_VOCABULARY, DATA_TYPE_FIELDS_VOCABULARY, IDataType, \
    ITypedDataManager, ITypedSharedTool, IWfTypedSharedContent, VISIBLE_DATA_TYPES_VOCABULARY
from pyams_i18n.interfaces import II18n
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_sequence.reference import get_reference_target
from pyams_utils.adapter import ContextAdapter, adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.registry import get_utilities_for, query_utility
from pyams_utils.request import check_request
from pyams_utils.traversing import get_parent
from pyams_utils.vocabulary import vocabulary_config

__docformat__ = 'restructuredtext'

from pyams_content import _


@factory_config(IDataType)
@implementer(IParagraphContainerTarget, ILinkContainerTarget, IExtFileContainerTarget,
             ITagsTarget, IThemesTarget)
class DataType(Persistent, Contained):
    """Base data type"""

    visible = FieldProperty(IDataType['visible'])
    label = FieldProperty(IDataType['label'])
    source_folder = FieldProperty(IDataType['source_folder'])
    navigation_label = FieldProperty(IDataType['navigation_label'])
    display_as_tag = FieldProperty(IDataType['display_as_tag'])
    facets_label = FieldProperty(IDataType['facets_label'])
    facets_type_label = FieldProperty(IDataType['facets_type_label'])
    dashboard_label = FieldProperty(IDataType['dashboard_label'])
    color = FieldProperty(IDataType['color'])
    pictogram = FieldProperty(IDataType['pictogram'])
    pictogram_on = FieldProperty(IDataType['pictogram_on'])
    pictogram_off = FieldProperty(IDataType['pictogram_off'])
    field_names = FieldProperty(IDataType['field_names'])

    def get_source_folder(self):
        """Source folder getter"""
        if self.source_folder is not None:
            return get_reference_target(self.source_folder)
        return None

    def get_pictogram(self):
        """Pictogram getter"""
        table = query_utility(IPictogramTable)
        if table is not None:
            return table.get(self.pictogram)
        return None


@adapter_config(required=IDataType,
                provides=ITypedSharedTool)
def datatype_shared_tool(context):
    """Datatype shared tool getter"""
    return get_parent(context, ITypedSharedTool)


@factory_config(ITypedDataManager)
class TypedDataManager(OrderedContainer):
    """Data types container persistent class"""

    def get_visible_items(self):
        """Iterator on visible data types"""
        yield from filter(lambda x: x.visible, self.values())


@adapter_config(required=IDataType,
                provides=IViewContextPermissionChecker)
class DatatypePermissionChecker(ContextAdapter):
    """Data type permission checker"""

    edit_permission = MANAGE_TOOL_PERMISSION


@implementer(ITypedSharedTool)
class TypedSharedToolMixin:
    """Typed shared tool"""

    shared_content_info_factory = None


@adapter_config(required=ITypedSharedTool,
                provides=ITypedDataManager)
def typed_shared_tool_data_manager_factory(context):
    """Types shared tool data manager factory"""
    return get_annotation_adapter(context, DATA_MANAGER_ANNOTATION_KEY, ITypedDataManager,
                                  name='++types++')


@adapter_config(name='types',
                required=ITypedSharedTool,
                provides=ITraversable)
class TypedSharedToolTypesNamespace(ContextAdapter):
    """Typed shared tool ++types++ namespace"""

    def traverse(self, name, furtherpath=None):
        """Namespace traverser"""
        return ITypedDataManager(self.context)


@adapter_config(name='types',
                required=ITypedSharedTool,
                provides=ISublocations)
class TypedSharedToolSublocations(ContextAdapter):
    """Typed shared tool sub-locations adapter"""

    def sublocations(self):
        """Sub-locations iterator"""
        yield from ITypedDataManager(self.context).values()


#
# Typed shared content
#

@implementer(IWfTypedSharedContent)
class WfTypedSharedContentMixin:
    """Typed shared content"""

    data_type = FieldProperty(IWfTypedSharedContent['data_type'])

    def get_data_type(self):
        """Datatype getter"""
        if not self.data_type:
            return None
        tool = ITypedSharedTool(self, None)
        if tool is not None:
            manager = ITypedDataManager(tool)
            return manager.get(self.data_type)
        return None

    @property
    def field_names(self):
        """Field names getter"""
        data_type = self.get_data_type()
        if data_type is not None:
            return data_type.field_names
        return None


@adapter_config(required=IWfTypedSharedContent,
                provides=ITypedSharedTool)
def typed_shared_content_shared_tool(context):
    """Typed shared content tool getter"""
    return get_parent(context, ITypedSharedTool)


@subscriber(IObjectAddedEvent, context_selector=IWfTypedSharedContent)
def handle_added_typed_shared_content(event):
    """Automatically assign tags and themes for newly created typed contents"""
    content = event.object
    data_type = content.get_data_type()
    if data_type is not None:
        if ITagsTarget.providedBy(data_type) and ITagsTarget.providedBy(content):
            tags_info = ITagsInfo(content)
            if not tags_info.tags:
                tags_info.tags = ITagsInfo(data_type).tags
        if IThemesTarget.providedBy(data_type) and IThemesTarget.providedBy(content):
            themes_info = IThemesInfo(content)
            if not themes_info.themes:  # don't remove previous themes!
                themes_info.themes = IThemesInfo(data_type).themes


#
# Data types vocabularies
#

@vocabulary_config(name=ALL_DATA_TYPES_VOCABULARY)
class AllTypedSharedToolDataTypesVocabulary(SimpleVocabulary):
    """Vocabulary consolidating data types of all shared tools"""

    def __init__(self, context):
        terms = []
        request = check_request()
        for name, tool in get_utilities_for(ISharedTool):
            if not name:
                continue
            manager = ITypedDataManager(tool, None)
            if manager is None:
                continue
            terms.extend([
                SimpleTerm(datatype.__name__,
                           title=II18n(datatype).query_attribute('label', request=request))
                for datatype in manager.values()
            ])
        terms.sort(key=lambda x: x.title)
        super().__init__(terms)

    def getTermByToken(self, token):
        try:
            return super().getTermByToken(token)
        except LookupError:
            request = check_request()
            translate = request.localizer.translate
            return SimpleTerm(token,
                              title=translate(_("-- missing value ({}) --")).format(token))


def get_all_data_types(request, context=None, fieldname=None):
    """Get list of all registered data types as JSON object"""
    results = []
    translate = request.localizer.translate
    if context is not None:
        values = getattr(context, fieldname, ()) or ()
    else:
        values = ()
    for name, tool in sorted(get_utilities_for(ISharedTool),
                             key=lambda x: II18n(x[1]).query_attribute('title', request=request)):
        if not name:
            continue
        manager = ITypedDataManager(tool, None)
        if manager is None:
            continue
        terms = [
            {
                'id': datatype.__name__,
                'text': II18n(datatype).query_attribute('label', request=request),
                'selected': datatype.__name__ in values
            }
            for datatype in manager.values()
        ]
        content_factory = tool.shared_content_factory.factory
        results.append({
            'text': translate(content_factory.content_name),
            'disabled': True,
            'children': terms
        })
    return results


@vocabulary_config(name=DATA_TYPES_VOCABULARY)
class TypedSharedToolDataTypesVocabulary(SimpleVocabulary):
    """Typed shared tool data types vocabulary"""

    def __init__(self, context):
        terms = []
        parent = ITypedSharedTool(context, None)
        if parent is not None:
            request = check_request()
            manager = ITypedDataManager(parent)
            terms = [
                SimpleTerm(datatype.__name__,
                           title=II18n(datatype).query_attribute('label', request=request))
                for datatype in manager.values()
            ]
        super().__init__(terms)


@vocabulary_config(name=VISIBLE_DATA_TYPES_VOCABULARY)
class TypedSharedToolVisibleDataTypesVocabulary(SimpleVocabulary):
    """Typed shared tool visible data types vocabulary"""

    def __init__(self, context):
        terms = []
        parent = ITypedSharedTool(context, None)
        if parent is not None:
            request = check_request()
            manager = ITypedDataManager(parent)
            terms = [
                SimpleTerm(datatype.__name__,
                           title=II18n(datatype).query_attribute('label', request=request))
                for datatype in manager.get_visible_items()
            ]
        super().__init__(terms)


@vocabulary_config(name=DATA_TYPE_FIELDS_VOCABULARY)
class TypedSharedToolDataTypesFieldsVocabulary(SimpleVocabulary):
    """Typed shared tool data types fields vocabulary"""

    def __init__(self, context):
        terms = []
        parent = ITypedSharedTool(context, None)
        if (parent is not None) and parent.shared_content_info_factory:
            request = check_request()
            translate = request.localizer.translate
            terms = [
                SimpleTerm(name, title=translate(field.title))
                for name, field in getFieldsInOrder(parent.shared_content_info_factory)
            ]
        super().__init__(terms)
