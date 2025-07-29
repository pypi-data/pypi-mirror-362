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

"""PyAMS_content.shared.view.reference module

This module provides persistent classes and adapters used to handle views
internal references support and catalog-based queries.
"""

from hypatia.catalog import CatalogQuery
from hypatia.interfaces import ICatalog
from hypatia.query import Eq, NotAny, NotEq
from persistent import Persistent
from zope.container.contained import Contained
from zope.schema.fieldproperty import FieldProperty

from pyams_catalog.query import CatalogResultSet
from pyams_content.shared.view import IViewSettings, IWfView
from pyams_content.shared.view.interfaces.query import EXCLUDED_VIEW_ITEMS, IViewQueryFilterExtension, \
    IViewQueryParamsExtension, IViewUserQuery
from pyams_content.shared.view.interfaces.settings import ALWAYS_REFERENCE_MODE, IViewInternalReferencesSettings, \
    ONLY_REFERENCE_MODE, VIEW_REFERENCES_SETTINGS_KEY
from pyams_sequence.interfaces import IInternalReferencesList, ISequentialIdInfo
from pyams_utils.adapter import ContextAdapter, adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.registry import get_utility
from pyams_workflow.interfaces import IWorkflow, IWorkflowPublicationInfo, IWorkflowVersions

__docformat__ = 'restructuredtext'


@factory_config(IViewInternalReferencesSettings)
class ViewInternalReferencesSettings(Persistent, Contained):
    """View internal references settings"""

    select_context_references = FieldProperty(IViewInternalReferencesSettings['select_context_references'])
    references = FieldProperty(IViewInternalReferencesSettings['references'])
    references_mode = FieldProperty(IViewInternalReferencesSettings['references_mode'])
    exclude_context = FieldProperty(IViewInternalReferencesSettings['exclude_context'])

    @property
    def is_using_context(self):
        return self.select_context_references

    def get_references(self, context):
        refs = []
        if self.select_context_references:
            references = IInternalReferencesList(context, None)
            if ((references is not None) and
                    getattr(references, 'use_references_for_views', True) and
                    references.references):
                refs.extend(references.references)
        if self.references:
            refs.extend(self.references)
        return refs


@adapter_config(required=IWfView,
                provides=IViewInternalReferencesSettings)
@adapter_config(name='references',
                required=IWfView,
                provides=IViewSettings)
def view_internal_references_settings(view):
    """View internal references settings factory"""
    return get_annotation_adapter(view, VIEW_REFERENCES_SETTINGS_KEY,
                                  IViewInternalReferencesSettings,
                                  name='++view:references++')


@adapter_config(name='references',
                required=IWfView,
                provides=IViewQueryParamsExtension)
class ViewReferencesQueryParamsExtension(ContextAdapter):
    """View internal references query params extension"""

    weight = 10

    def get_params(self, context, request=None):
        """Query params getter"""
        settings = IViewInternalReferencesSettings(self.context)
        # check view references mode
        if settings.references_mode == ONLY_REFERENCE_MODE:
            # references are retrieved by query filter extension, so no params are required!
            yield None
        else:
            # check view settings
            if settings.exclude_context:
                sequence = ISequentialIdInfo(context, None)
                if sequence is not None:
                    oid = sequence.hex_oid
                    catalog = get_utility(ICatalog)
                    yield NotEq(catalog['oid'], oid)


@adapter_config(name='references',
                required=IWfView,
                provides=IViewQueryFilterExtension)
class ViewReferencesQueryFilterExtension(ContextAdapter):
    """View internal references filter extension

    If internal references are selected, these references are forced.
    """

    weight = 999

    def filter(self, context, items, request=None):
        """Filter incoming items based on references settings"""
        settings = IViewInternalReferencesSettings(self.context)
        references = settings.get_references(context)
        if not references:
            return items
        excluded_oid = None
        if settings.exclude_context:
            sequence = ISequentialIdInfo(context, None)
            if sequence is not None:
                excluded_oid = sequence.hex_oid
        if (not items) or (settings.references_mode in (ALWAYS_REFERENCE_MODE, ONLY_REFERENCE_MODE)):
            catalog = get_utility(ICatalog)
            for reference in reversed(references):
                if reference == excluded_oid:
                    continue
                params = Eq(catalog['oid'], reference)
                for item in CatalogResultSet(CatalogQuery(catalog).query(params)):
                    versions = IWorkflowVersions(item, None)
                    if versions is not None:
                        workflow = IWorkflow(item)
                        items.prepend(versions.get_versions(workflow.visible_states))
                    else:
                        publication_info = IWorkflowPublicationInfo(item, None)
                        if (publication_info is not None) and \
                                publication_info.is_visible(request):
                            items.prepend((item,))
        return items


@adapter_config(name='exclusions',
                context=IWfView,
                provides=IViewUserQuery)
class ExclusionsViewQueryParamsExtension(ContextAdapter):
    """Search folder exclusions for Elasticsearch

    This adapter is looking into request's annotations for items which should be excluded
    from search.
    """

    @staticmethod
    def get_user_params(request):
        excluded_items = request.annotations.get(EXCLUDED_VIEW_ITEMS)
        if excluded_items:
            catalog = get_utility(ICatalog)
            yield NotAny(catalog['oid'], excluded_items)
