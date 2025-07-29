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

"""PyAMS_*** module

"""

__docformat__ = 'restructuredtext'

from zope.schema import Bool, Choice, Int, List, Set

from pyams_content.component.paragraph import CONTENT_PARAGRAPHS_VOCABULARY, \
    PARAGRAPH_FACTORIES_VOCABULARY
from pyams_i18n.schema import I18nTextLineField
from pyams_portal.interfaces import IPortletSettings
from pyams_sequence.schema import InternalReferenceField

from pyams_content import _


class IParagraphContainerPortletSettings(IPortletSettings):
    """Paragraph container portlet settings"""

    title = I18nTextLineField(title=_("Title"),
                              required=False)

    reference = InternalReferenceField(title=_("Paragraphs source"),
                                       description=_("If a source is specified, it will be used "
                                                     "as paragraphs source instead of current "
                                                     "context"),
                                       required=False)

    button_label = I18nTextLineField(title=_("Button label"),
                                     description=_("If a source is specified, you can create a "
                                                   "link to this content using a button with "
                                                   "this label"),
                                     required=False)

    paragraphs = List(title=_("Selected paragraphs"),
                      description=_("List of selected paragraphs; an empty selection means that "
                                    "all paragraphs will be selectable by following filters; "
                                    "otherwise, this selection will have priority"),
                      value_type=Choice(vocabulary=CONTENT_PARAGRAPHS_VOCABULARY),
                      required=False)

    factories = Set(title=_("Selected paragraph types"),
                    description=_("Select list of paragraph types you want to include; an empty "
                                  "selection means that all paragraphs types will be selected; "
                                  "this setting is not applied when paragraphs are selected "
                                  "explicitly in the previous field"),
                    value_type=Choice(vocabulary=PARAGRAPH_FACTORIES_VOCABULARY),
                    required=False)

    excluded_factories = Set(title=_("Excluded paragraph types"),
                             description=_("Select list of paragraph types you want to exclude; an empty "
                                           "selection means that all paragraphs types will be selected, "
                                           "except if factories are selected in the previous field; "
                                           "this setting is not applied when paragraphs are selected "
                                           "explicitly in the previous field"),
                             value_type=Choice(vocabulary=PARAGRAPH_FACTORIES_VOCABULARY),
                             required=False)

    anchors_only = Bool(title=_("Anchors only"),
                        description=_("If 'yes', only paragraphs set as 'anchors' will be "
                                      "selected"),
                        required=True,
                        default=False)

    exclude_anchors = Bool(title=_("Exclude anchors"),
                           description=_("If 'yes', paragraphs set as 'anchors' will be "
                                         "excluded; take care to not activate this option and "
                                         "the previous one simultaneously, or no paragraph will "
                                         "be displayed!"),
                           required=True,
                           default=False)

    limit = Int(title=_("Paragraphs count limit"),
                description=_("If specified, the number of displayed paragraphs will be limited "
                              "to this number"),
                required=False)

    display_navigation_links = Bool(title=_("Display navigation links"),
                                    description=_("If 'no', navigation links to previous and "
                                                  "next contents will not be displayed"),
                                    required=True,
                                    default=True)


class IParagraphNavigationPortletSettings(IPortletSettings):
    """Paragraphs container navigation settings interface"""

    paragraphs = List(title=_("Selected paragraphs"),
                      description=_("List of paragraphs selected for navigation; an empty "
                                    "selection means that all paragraphs will be selectable by "
                                    "following filters; otherwise, this selection will have "
                                    "priority"),
                      value_type=Choice(vocabulary=CONTENT_PARAGRAPHS_VOCABULARY),
                      required=False)

    factories = Set(title=_("Selected paragraph types"),
                    description=_("Select list of paragraph types you want to use for "
                                  "navigation; an empty selection means that all paragraphs "
                                  "types will be selected"),
                    value_type=Choice(vocabulary=PARAGRAPH_FACTORIES_VOCABULARY),
                    required=False)

    excluded_factories = Set(title=_("Excluded paragraph types"),
                             description=_("Select list of paragraph types you want to exclude from "
                                           "navigation; an empty selection means that all paragraphs "
                                           "types will be selected, except if factories are selected "
                                           "in the previous field"),
                             value_type=Choice(vocabulary=PARAGRAPH_FACTORIES_VOCABULARY),
                             required=False)

    anchors_only = Bool(title=_("Anchors only"),
                        description=_("If 'no', all paragraphs will be used as navigation "
                                      "anchors"),
                        required=True,
                        default=True)
