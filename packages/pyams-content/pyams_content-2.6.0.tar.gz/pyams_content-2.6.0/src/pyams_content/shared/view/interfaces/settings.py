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

"""PyAMS_content.shared.view.interfaces.settings module

This module defines interfaces used to handle views settings.
"""

from collections import OrderedDict

from zope.interface import Attribute, Interface
from zope.schema import Bool, Choice, Int
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from pyams_sequence.interfaces import IInternalReferencesList
from pyams_sequence.schema import InternalReferencesListField
from pyams_thesaurus.schema import ThesaurusTermsListField

__docformat__ = 'restructuredtext'

from pyams_content import _


class IViewSettings(Interface):
    """Base interface for view settings adapters"""

    is_using_context = Attribute("Check if view settings are using context")


#
# References settings
#

VIEW_REFERENCES_SETTINGS_KEY = 'pyams_content.view.references'

ALWAYS_REFERENCE_MODE = 'always'
IFEMPTY_REFERENCE_MODE = 'if_empty'
ONLY_REFERENCE_MODE = 'only'

REFERENCES_MODES = OrderedDict((
    (ALWAYS_REFERENCE_MODE, _("Always include selected internal references")),
    (IFEMPTY_REFERENCE_MODE, _("Include selected internal references only if view is empty")),
    (ONLY_REFERENCE_MODE, _("Include ONLY selected references (no search will be made)"))
))

REFERENCES_MODES_VOCABULARY = SimpleVocabulary([
    SimpleTerm(v, title=t)
    for v, t in REFERENCES_MODES.items()
])


class IViewInternalReferencesSettings(IViewSettings, IInternalReferencesList):
    """View internal references settings"""

    select_context_references = Bool(title=_("Select context references?"),
                                     description=_("If 'non', references imposed by the context "
                                                   "will not be used"),
                                     required=False,
                                     default=True)

    references = InternalReferencesListField(title=_("Other references"),
                                             description=_("List of internal references"),
                                             required=False)

    references_mode = Choice(title=_("Internal references usage"),
                             description=_("Specify how selected references are included into "
                                           "view results"),
                             vocabulary=REFERENCES_MODES_VOCABULARY,
                             required=True,
                             default=ALWAYS_REFERENCE_MODE)

    exclude_context = Bool(title=_("Exclude context?"),
                           description=_("If 'yes', context will be excluded from results list"),
                           required=True,
                           default=True)

    def get_references(self, context):
        """Get all references for given context"""


#
# Tags settings
#

VIEW_TAGS_SETTINGS_KEY = 'pyams_content.view.tags'


class IViewTagsSettings(IViewSettings):
    """View tags settings"""

    select_context_tags = Bool(title=_("Select context tags?"),
                               description=_("If 'yes', tags will be extracted from context"),
                               required=False,
                               default=False)

    tags = ThesaurusTermsListField(title=_("Other tags"),
                                   required=False)

    def get_tags(self, context):
        """Get all tags for given context"""

    def get_tags_index(self, context):
        """Get all tags index values for given context"""


#
# Themes settings
#

VIEW_THEMES_SETTINGS_KEY = 'pyams_content.view.themes'


class IViewThemesSettings(IViewSettings):
    """View themes settings"""

    select_context_themes = Bool(title=_("Select context themes?"),
                                 description=_("If 'yes', themes will be extracted from context"),
                                 required=False,
                                 default=False)

    themes = ThesaurusTermsListField(title=_("Other themes"),
                                     required=False)

    include_subthemes = Bool(title=_("Include all subthemes?"),
                             description=_("If 'yes', subthemes of selected themes will also "
                                           "be used to search contents"),
                             required=False,
                             default=False)

    def get_themes(self, context):
        """Get all themes for given context"""

    def get_themes_index(self, context):
        """Get all themes index values for given context"""


#
# Collections settings
#

VIEW_COLLECTIONS_SETTINGS_KEY = 'pyams_content.view.collections'


class IViewCollectionsSettings(IViewSettings):
    """View collections settings"""

    select_context_collections = Bool(title=_("Select context collections?"),
                                      description=_("If 'yes', collections will be extracted "
                                                    "from context"),
                                      required=False,
                                      default=False)

    collections = ThesaurusTermsListField(title=_("Other collections"),
                                          required=False)

    def get_collections(self, context):
        """Get all collections for given context"""

    def get_collections_index(self, context):
        """Get all collections index values for given context"""
