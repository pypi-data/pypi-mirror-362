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

"""PyAMS_content.component.thesaurus.interfaces module

This module is used to assign tags, themes and collections to contents.
These elements are based on thesaurus contents.
"""

from zope.interface import Attribute, Interface, Invalid, invariant
from zope.schema import Bool, Choice

from pyams_thesaurus.interfaces import THESAURUS_NAMES_VOCABULARY
from pyams_thesaurus.interfaces.thesaurus import IThesaurusContextManager, \
    IThesaurusContextManagerTarget
from pyams_thesaurus.schema import ThesaurusTermsListField
from pyams_utils.interfaces.inherit import IInheritInfo

__docformat__ = 'restructuredtext'

from pyams_content import _


#
# Tags management
#

TAGS_MANAGER_KEY = 'pyams_content.tags.manager'
TAGS_INFO_KEY = 'pyams_content.tags.info'


class ITagsManager(IThesaurusContextManager):
    """Tags manager interface"""

    enable_glossary = Bool(title=_("Enable glossary"),
                           required=True,
                           default=False)

    glossary_thesaurus_name = Choice(title=_("Glossary thesaurus name"),
                                     vocabulary=THESAURUS_NAMES_VOCABULARY,
                                     required=False)

    glossary = Attribute("Glossary getter")

    @invariant
    def check_glossary_thesaurus(self):
        if self.enable_glossary and not self.glossary_thesaurus_name:
            raise Invalid(_("You must specify a glossary thesaurus to activate it!"))


class ITagsManagerTarget(IThesaurusContextManagerTarget):
    """Marker interface for tags manager"""


class ITagsInfo(Interface):
    """Tags information interface"""

    tags = ThesaurusTermsListField(title=_("Tags"),
                                   required=False)


class ITagsTarget(Interface):
    """Tags target interface"""


#
# Themes management
#

THEMES_MANAGER_KEY = 'pyams_content.themes.manager'
THEMES_INFO_KEY = 'pyams_content.themes.info'


class IThemesManager(IThesaurusContextManager):
    """Themes manager interface"""


class IThemesManagerTarget(IThesaurusContextManagerTarget):
    """Marker interface for tools managing themes"""


class IThemesInfo(IInheritInfo):
    """Themes information interface"""

    themes = ThesaurusTermsListField(title=_("Themes"),
                                     required=False)


class IThemesTarget(Interface):
    """Themes target interface"""


#
# Collections management
#

COLLECTIONS_MANAGER_KEY = 'pyams_content.collections.manager'
COLLECTIONS_INFO_KEY = 'pyams_content.collections.info'


class ICollectionsManager(IThesaurusContextManager):
    """Collections manager interface"""


class ICollectionsManagerTarget(IThesaurusContextManagerTarget):
    """Marker interface for tools managing collections"""


class ICollectionsInfo(Interface):
    """Collections information interface"""

    collections = ThesaurusTermsListField(title=_("Collections"),
                                          required=False)


class ICollectionsTarget(Interface):
    """Collections target interface"""
