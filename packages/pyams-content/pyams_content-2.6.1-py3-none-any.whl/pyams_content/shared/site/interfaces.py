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

"""PyAMS_content.shared.site.interfaces module

"""

from collections import OrderedDict

from zope.annotation import IAttributeAnnotatable
from zope.container.constraints import containers, contains
from zope.container.interfaces import IContainer
from zope.interface import Attribute, Interface
from zope.location.interfaces import IContained
from zope.schema import Bool, Choice, Text, URI
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_content.interfaces import IBaseContent
from pyams_content.shared.common.interfaces import IBaseSharedTool, IDeletableElement, ISharedSite
from pyams_content.shared.common.interfaces.types import DATA_TYPES_VOCABULARY
from pyams_content.shared.topic import ITopic, IWfTopic
from pyams_i18n.schema import I18nTextField, I18nTextLineField
from pyams_sequence.interfaces import IInternalReference, IInternalReferencesList, \
    ISequentialIdTarget
from pyams_workflow.interfaces import IWorkflowPublicationSupport


__docformat__ = 'restructuredtext'

from pyams_content import _


SITE_CONTAINER_REDIRECT_MODE = 'redirect'
SITE_CONTAINER_TEMPLATE_MODE = 'template'

SITE_CONTAINER_NAVIGATION_MODES = OrderedDict((
    (SITE_CONTAINER_REDIRECT_MODE, _("Redirect to first visible sub-folder or content")),
    (SITE_CONTAINER_TEMPLATE_MODE, _("Use presentation template"))
))

SITE_CONTAINER_NAVIGATION_MODES_VOCABULARY = SimpleVocabulary([
    SimpleTerm(v, title=t)
    for v, t in SITE_CONTAINER_NAVIGATION_MODES.items()
])


SITE_MANAGER_INDEXATION_FULL_MODE = 'full'
SITE_MANAGER_INDEXATION_INTERNAL_MODE = 'internal'
SITE_MANAGER_INDEXATION_NULL_MODE = 'none'

SITE_MANAGER_INDEXATION_MODES = OrderedDict((
    (SITE_MANAGER_INDEXATION_FULL_MODE, _("Full indexation mode")),
    (SITE_MANAGER_INDEXATION_INTERNAL_MODE, _("Internal only indexation mode")),
    (SITE_MANAGER_INDEXATION_NULL_MODE, _("No indexation mode"))
))

SITE_MANAGER_INDEXATION_MODES_VOCABULARY = SimpleVocabulary([
    SimpleTerm(v, title=t)
    for v, t in SITE_MANAGER_INDEXATION_MODES.items()
])


SITE_CONTENT_VOCABULARY = 'pyams_content.site.content'


class ISiteElement(IContained, IDeletableElement):
    """Base site element interface"""

    containers('.ISiteContainer')

    content_name = Attribute("Content name")


class ISiteElementNavigation(Interface):
    """Site element navigation interface"""

    visible = Attribute("Visible element?")


class IBaseSiteItem(IContained, IWorkflowPublicationSupport):
    """Base site item class"""


class ISiteContainer(IContainer, IBaseSiteItem):
    """Base site container interface"""

    contains(ISiteElement)

    navigation_mode = Choice(title=_("Navigation mode"),
                             description=_("Site behaviour when navigating to site URL"),
                             required=True,
                             vocabulary=SITE_CONTAINER_NAVIGATION_MODES_VOCABULARY,
                             default=SITE_CONTAINER_TEMPLATE_MODE)

    shared_content_type = Attribute("Shared content type")

    shared_content_factory = Attribute("Shared content factory")

    def get_visible_items(self, request=None):
        """Iterator over container visible items"""

    def get_folders_tree(self, selected=None):
        """Get site tree in JSON format"""


#
# Site folder interface
#

SITE_FOLDERS_VOCABULARY = 'pyams_content.site.folders'


class ISiteFolder(IBaseContent, ISiteElement, ISiteContainer, ISequentialIdTarget):
    """Site folder interface

    A site folder is made to contain sub-folders and topics
    """

    header = I18nTextField(title=_("Header"),
                           description=_("Heading displayed according to presentation template"),
                           required=False)

    description = I18nTextField(title=_("Meta-description"),
                                description=_("The folder's description is 'hidden' into HTML's "
                                              "page headers; but it can be seen, for example, "
                                              "in some search engines results as content's "
                                              "description; if description is empty, content's "
                                              "header will be used."),
                                required=False)

    notepad = Text(title=_("Notepad"),
                   description=_("Internal information to be known about this content"),
                   required=False)

    visible_in_list = Bool(title=_("Visible in folders list"),
                           description=_("If 'no', folder will not be displayed into folders "
                                         "list"),
                           required=True,
                           default=True)

    navigation_title = I18nTextLineField(title=_("Navigation title"),
                                         description=_("Folder's title displayed in navigation "
                                                       "pages; original title will be used if "
                                                       "none is specified"),
                                         required=False)

    navigation_mode = Choice(title=_("Navigation mode"),
                             description=_("Folder behaviour when navigating to folder URL"),
                             required=True,
                             vocabulary=SITE_CONTAINER_NAVIGATION_MODES_VOCABULARY,
                             default=SITE_CONTAINER_REDIRECT_MODE)


#
# Site manager interface
#

PYAMS_SITES_VOCABULARY = 'pyams_content.sites'


class ISiteManager(ISharedSite, ISiteContainer, IBaseSharedTool,
                   IDeletableElement, ISequentialIdTarget):
    """Site manager interface"""

    contains(ISiteElement)

    folder_factory = Attribute("Folder factory")

    header = I18nTextField(title=_("Header"),
                           description=_("Site's header is generally displayed in page header"),
                           required=False)

    indexation_mode = Choice(title=_("Indexation mode"),
                             description=_("Indexation mode is used to specify which site parts "
                                           "should be indexed by robots"),
                             required=True,
                             vocabulary=SITE_MANAGER_INDEXATION_MODES_VOCABULARY,
                             default=SITE_MANAGER_INDEXATION_FULL_MODE)

    description = I18nTextField(title=_("Meta-description"),
                                description=_("The site's description is 'hidden' into HTML's "
                                              "page headers; but it can be seen, for example, "
                                              "in some search engines results as content's "
                                              "description; if description is empty, content's "
                                              "header will be used."),
                                required=False)

    notepad = Text(title=_("Notepad"),
                   description=_("Internal information to be known about this content"),
                   required=False)


#
# Site topics interfaces
#

SITE_TOPIC_CONTENT_TYPE = 'site-topic'
SITE_TOPIC_CONTENT_NAME = _("Site topic")


class IWfSiteTopic(IWfTopic, IInternalReferencesList):
    """Site topic interface"""

    data_type = Choice(title=_("Data type"),
                       description=_("Type of content data"),
                       required=False,
                       vocabulary=DATA_TYPES_VOCABULARY)


class ISiteTopic(ITopic, ISiteElement):
    """Workflow managed site topic interface"""


#
# Site links interfaces
#

class ISiteLink(ISiteElement):
    """Content link interface"""
    
    navigation_title = I18nTextLineField(title=_("Navigation title"),
                                         description=_("Alternate content's title displayed in "
                                                       "navigation pages; original title will be "
                                                       "used if none is specified"),
                                         required=False)

    show_header = Bool(title=_("Show header?"),
                       description=_("If 'no', no header will be displayed"),
                       required=False,
                       default=True)

    navigation_header = I18nTextField(title=_("Navigation header"),
                                      description=_("Alternate content's header displayed in "
                                                    "navigation pages; original header will be "
                                                    "used if none is specified"),
                                      required=False)

    visible = Bool(title=_("Visible?"),
                   description=_("If 'no', link is not visible"),
                   required=True,
                   default=True)


class IInternalSiteLink(ISiteLink, IInternalReference):
    """Internal content site link interface"""

    force_canonical_url = Bool(title=_("Force canonical URL?"),
                               description=_("If 'yes', link to internal references will "
                                             "use their canonical instead of relative URL"),
                               required=True,
                               default=False)


class IExternalSiteLink(ISiteLink, IAttributeAnnotatable):
    """External site link interface"""

    url = URI(title=_("Target URL"),
              description=_("URL used to access external resource"),
              required=True)
