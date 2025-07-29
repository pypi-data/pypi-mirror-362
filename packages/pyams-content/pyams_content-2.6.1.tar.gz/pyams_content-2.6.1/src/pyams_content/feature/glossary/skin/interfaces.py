#
# Copyright (c) 2015-2022 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.feature.glossary.skin.interfaces module

This module defines interfaces related to glossary terms rendering.
"""

__docformat__ = 'restructuredtext'

from zope.contentprovider.interfaces import IContentProvider
from zope.interface import Attribute


class IThesaurusTermRenderer(IContentProvider):
    """Thesaurus term renderer interface"""

    weight = Attribute("Weight used to sort adapters")
