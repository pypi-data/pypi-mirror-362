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

"""PyAMS_content.reference.pictogram.interfaces module

"""

from zope.annotation import IAttributeAnnotatable
from zope.container.constraints import containers, contains
from zope.interface import Interface
from zope.schema import Choice, List

from pyams_content.reference.interfaces import IReferenceInfo, IReferenceTable
from pyams_file.schema import I18nImageField
from pyams_i18n.schema import I18nTextLineField

__docformat__ = 'restructuredtext'

from pyams_content import _


PICTOGRAM_VOCABULARY = 'pyams_content.pictograms'
SELECTED_PICTOGRAM_VOCABULARY = 'pyams_content.pictograms.selected'


class IPictogram(IReferenceInfo):
    """Pictogram interface

    Pictograms are managed in a specific reference table to be easily reused by the application
    into any shared content.
    """

    containers('.IPictogramTable')

    image = I18nImageField(title=_("Image"),
                           description=_("Pictogram content"),
                           required=True)

    alt_title = I18nTextLineField(title=_("Accessibility title"),
                                  description=_("Alternate title used to describe image content"),
                                  required=False)

    header = I18nTextLineField(title=_('pictogram-header', default="Header"),
                               description=_("Default header associated with this pictogram"),
                               required=False)


class IPictogramTable(IReferenceTable):
    """Pictograms table interface"""

    contains(IPictogram)


PICTOGRAM_MANAGER_KEY = 'pyams_content.pictogram.manager'


class IPictogramManager(Interface):
    """Pictogram manager interface

    A pictogram manager (typically, a shared tool) is a component which allows selection of a
    set of pictogram which will be available for selection into shared content.
    """

    selected_pictograms = List(title=_("Selected pictograms"),
                               description=_("List of selected pictograms which will be "
                                             "available to shared contents"),
                               required=False,
                               value_type=Choice(vocabulary=PICTOGRAM_VOCABULARY))


class IPictogramManagerTarget(IAttributeAnnotatable):
    """Pictogram manager target interface"""


THESAURUS_TERM_PICTOGRAMS_INFO_KEY = 'pyams_content.extension.pictograms'


class IThesaurusTermPictogramsInfo(Interface):
    """Thesaurus term pictograms info interface"""
    
    pictogram_on = Choice(title=_("'ON' pictogram"),
                          description=_("'ON' state pictogram associated with this term"),
                          vocabulary=PICTOGRAM_VOCABULARY,
                          required=False)
    
    pictogram_off = Choice(title=_("'OFF' pictogram"),
                           description=_("'OFF' state pictogram associated with this term"),
                           vocabulary=PICTOGRAM_VOCABULARY,
                           required=False)


class IThesaurusTermPictogramsTarget(IAttributeAnnotatable):
    """Thesaurus term pictograms target marker interface"""
