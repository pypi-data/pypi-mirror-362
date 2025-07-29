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

"""PyAMS_content.shared.view.merge module

This module defines several views *mergers*, which can utilities which can be
used to merge several views items together.
"""

from heapq import merge
from itertools import chain, zip_longest
from random import shuffle

from zope.componentvocabulary.vocabulary import UtilityTerm, UtilityVocabulary
from zope.dublincore.interfaces import IZopeDublinCore

from pyams_content.shared.view.interfaces import CREATION_DATE_ORDER, FIRST_PUBLICATION_DATE_ORDER, \
    PUBLICATION_DATE_ORDER, UPDATE_DATE_ORDER
from pyams_content.shared.view.interfaces.query import MergeModes, IViewsMerger, VIEWS_MERGERS_VOCABULARY
from pyams_utils.registry import utility_config
from pyams_utils.request import check_request
from pyams_utils.vocabulary import vocabulary_config
from pyams_workflow.interfaces import IWorkflowPublicationInfo

__docformat__ = 'restructuredtext'

from pyams_content import _


@vocabulary_config(name=VIEWS_MERGERS_VOCABULARY)
class ViewsMergersVocabulary(UtilityVocabulary):
    """Views mergers vocabulary"""

    interface = IViewsMerger
    nameOnly = True

    def __init__(self, context, **kw):
        request = check_request()
        registry = request.registry
        translate = request.localizer.translate
        utils = [
            (name, translate(util.label))
            for (name, util) in registry.getUtilitiesFor(self.interface)
        ]
        self._terms = dict((title, UtilityTerm(name, title)) for name, title in utils)


class SingleViewMergeMode:
    """Single view merger"""

    @classmethod
    def get_results(cls, view, context, ignore_cache=False, request=None,
                    aggregates=None, settings=None, get_count=False):
        count, aggregations, results = view.get_results(context, ignore_cache=ignore_cache, request=request,
                                                        aggregates=aggregates, settings=settings, get_count=True)
        if get_count:
            yield count
            yield aggregations
        yield from results


@utility_config(name=MergeModes.CONCAT.value,
                provides=IViewsMerger)
class ViewsConcatenateMergeMode(SingleViewMergeMode):
    """Views concatenate merge mode"""

    label = _("Concatenate views items in order")

    @classmethod
    def get_results(cls, views, context, ignore_cache=False, request=None,
                    aggregates=None, settings=None, get_count=False):
        views = list(views) or ()
        if len(views) == 1:
            yield from super().get_results(views[0], context, ignore_cache=ignore_cache, request=request,
                                           aggregates=aggregates, settings=settings, get_count=get_count)
        else:
            results = (
                view.get_results(context, ignore_cache=ignore_cache, request=request,
                                 aggregates=aggregates, settings=settings, get_count=False)
                for view in views
            )
            yield from chain(*results)


@utility_config(name=MergeModes.RANDOM.value,
                provides=IViewsMerger)
class ViewsRandomMergeMode(SingleViewMergeMode):
    """Views random merge mode"""

    label = _("Extract items randomly")

    @classmethod
    def get_results(cls, views, context, ignore_cache=False, request=None,
                    aggregates=None, settings=None, get_count=False):
        views = list(views) or ()
        if len(views) == 1:
            yield from super().get_results(views[0], context, ignore_cache=ignore_cache, request=request,
                                           aggregates=aggregates, settings=settings, get_count=get_count)
        else:
            results = (
                view.get_results(context, ignore_cache=ignore_cache, request=request,
                                 aggregates=aggregates, settings=settings)
                for view in views
            )
            results = list(chain(*results))
            shuffle(results)
            yield from iter(results)


@utility_config(name=MergeModes.ZIP.value,
                provides=IViewsMerger)
class ViewsZipMergeMode(SingleViewMergeMode):
    """Views zip merge mode"""

    label = _("Take items from views one by one, in views order")

    @classmethod
    def get_results(cls, views, context, ignore_cache=False, request=None,
                    aggregates=None, settings=None, get_count=False):
        views = list(views) or ()
        if len(views) == 1:
            yield from super().get_results(views[0], context, ignore_cache=ignore_cache, request=request,
                                           aggregates=aggregates, settings=settings, get_count=get_count)
        else:
            results = (
                view.get_results(context, ignore_cache=ignore_cache, request=request,
                                 aggregates=aggregates, settings=settings)
                for view in views
            )
            for array in zip_longest(*results):
                yield from filter(lambda x: x is not None, array)


@utility_config(name=MergeModes.RANDOM_ZIP.value,
                provides=IViewsMerger)
class ViewsRandomZipMergeMode(SingleViewMergeMode):
    """Views random zip merge mode"""

    label = _("Take items from views one by one, in random order")

    @classmethod
    def get_results(cls, views, context, ignore_cache=False, request=None,
                    aggregates=None, settings=None, get_count=False):
        views = list(views) or ()
        if len(views) == 1:
            yield from super().get_results(views[0], context, ignore_cache=ignore_cache, request=request,
                                           aggregates=aggregates, settings=settings, get_count=get_count)
        else:
            results = [
                view.get_results(context, ignore_cache=ignore_cache, request=request,
                                 aggregates=aggregates, settings=settings)
                for view in views
            ]
            shuffle(results)
            for array in zip_longest(*results):
                yield from filter(lambda x: x is not None, array)


class SortedMergeMode(SingleViewMergeMode):
    """Sorted merge mode base class"""

    label = None
    sort_index = None
    sort_key = None

    @classmethod
    def get_results(cls, views, context, ignore_cache=False, request=None,
                    aggregates=None, settings=None, get_count=False):
        views = list(views) or ()
        if len(views) == 1:
            yield from super().get_results(views[0], context, ignore_cache=ignore_cache, request=request,
                                           aggregates=aggregates, settings=settings, get_count=get_count)
        else:
            results = (
                sorted(view.get_results(context, ignore_cache=ignore_cache, request=request,
                                        aggregates=aggregates, settings=settings),
                       key=cls.sort_key, reverse=True)
                for view in views
            )
            yield from merge(*results, key=cls.sort_key, reverse=True)


@utility_config(name=f'{CREATION_DATE_ORDER}.sort',
                provides=IViewsMerger)
class CreationDateSortedMergeMode(SortedMergeMode):
    """Merge pre-sorted views by creation date"""

    label = _("Sort all results by creation date")
    sort_index = CREATION_DATE_ORDER

    @staticmethod
    def sort_key(item):
        return IZopeDublinCore(item).created


@utility_config(name=f'{UPDATE_DATE_ORDER}.sort',
                provides=IViewsMerger)
class UpdateDateSortedMergeMode(SortedMergeMode):
    """Merge pre-sorted views by last update date"""

    label = _("Sort all results by last update date")
    sort_index = UPDATE_DATE_ORDER

    @staticmethod
    def sort_key(item):
        return IZopeDublinCore(item).modified


@utility_config(name=f'{PUBLICATION_DATE_ORDER}.sort',
                provides=IViewsMerger)
class PublicationDateSortedMergeMode(SortedMergeMode):
    """Merge pre-sorted views by publication date"""

    label = _("Sort all results by current publication date")
    sort_index = PUBLICATION_DATE_ORDER

    @staticmethod
    def sort_key(item):
        return IWorkflowPublicationInfo(item).publication_date


@utility_config(name=f'{FIRST_PUBLICATION_DATE_ORDER}.sort',
                provides=IViewsMerger)
class FirstPublicationDateSortedMergeMode(SortedMergeMode):
    """Merge pre-sorted views by first publication date"""

    label = _("Sort all results by first publication date")
    sort_index = FIRST_PUBLICATION_DATE_ORDER

    @staticmethod
    def sort_key(item):
        return IWorkflowPublicationInfo(item).first_publication_date
