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

"""PyAMS_*** module

"""

__docformat__ = 'restructuredtext'

from persistent import Persistent
from zope.container.contained import Contained
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_content.reference.pictogram.interfaces import IPictogramManager, \
    IPictogramManagerTarget, IPictogramTable, PICTOGRAM_MANAGER_KEY, SELECTED_PICTOGRAM_VOCABULARY
from pyams_i18n.interfaces import II18n
from pyams_utils.adapter import adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.registry import query_utility
from pyams_utils.request import check_request
from pyams_utils.traversing import get_parent
from pyams_utils.vocabulary import vocabulary_config


@factory_config(IPictogramManager)
class PictogramManager(Persistent, Contained):
    """Pictogram manager settings persistent class"""

    selected_pictograms = FieldProperty(IPictogramManager['selected_pictograms'])


@adapter_config(required=IPictogramManagerTarget,
                provides=IPictogramManager)
def pictogram_manager_factory(target):
    """Pictogram manager factory"""
    return get_annotation_adapter(target, PICTOGRAM_MANAGER_KEY, IPictogramManager)


@vocabulary_config(name=SELECTED_PICTOGRAM_VOCABULARY)
class SelectedPictogramsVocabulary(SimpleVocabulary):
    """Selected pictograms vocabulary"""

    def __init__(self, context=None):
        terms = []
        table = query_utility(IPictogramTable)
        if table is not None:
            request = check_request()
            target = get_parent(context, IPictogramManagerTarget)
            if target is not None:
                manager = IPictogramManager(target)
                pictograms = [table.get(name) for name in manager.selected_pictograms or ()]
                terms = [
                    SimpleTerm(v.__name__,
                               title=II18n(v).query_attribute('title', request=request))
                    for v in pictograms if v is not None
                ]
            else:
                terms = [
                    SimpleTerm(v.__name__,
                               title=II18n(v).query_attribute('title', request=request))
                    for v in table.values()
                ]
            terms = sorted(terms, key=lambda x: x.title)
        super(SelectedPictogramsVocabulary, self).__init__(terms)
