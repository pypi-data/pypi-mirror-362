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

from collections import OrderedDict
from enum import Enum

from zope.interface import Interface
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

__docformat__ = 'restructuredtext'

from pyams_content import _


class HEADER_DISPLAY_MODE(Enum):
    """Header display modes"""
    FULL = 'full'
    START = 'start'
    HIDDEN = 'none'


HEADER_DISPLAY_MODES_NAMES = OrderedDict((
    (HEADER_DISPLAY_MODE.FULL, _("Display full header")),
    (HEADER_DISPLAY_MODE.START, _("Display only header start")),
    (HEADER_DISPLAY_MODE.HIDDEN, _("Hide header"))
), )


HEADER_DISPLAY_MODES_VOCABULARY = SimpleVocabulary([
    SimpleTerm(v.value, title=t)
    for v, t in HEADER_DISPLAY_MODES_NAMES.items()
])


class IPageHeaderTitle(Interface):
    """Page header title getter interface"""
