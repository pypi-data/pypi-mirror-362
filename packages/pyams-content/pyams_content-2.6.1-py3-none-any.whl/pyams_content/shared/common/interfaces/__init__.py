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

"""PyAMS_content.shared.common.interfaces module

This module defines interfaces which are common to all shared contents.
"""
from collections import OrderedDict
from enum import Enum

from zope.annotation.interfaces import IAttributeAnnotatable
from zope.container.constraints import containers, contains
from zope.container.interfaces import IContainer
from zope.interface import Attribute, Interface
from zope.schema import Bool, Choice, Text, TextLine
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_content.component.paragraph.interfaces import IBaseParagraph
from pyams_content.component.paragraph.schema import ParagraphRendererChoice
from pyams_content.interfaces import CONTRIBUTOR_ROLE, GUEST_ROLE, IBaseContent, MANAGER_ROLE, \
    OWNER_ROLE, PILOT_ROLE, READER_ROLE, WEBMASTER_ROLE
from pyams_i18n.schema import I18nTextField, I18nTextLineField
from pyams_portal.interfaces import DESIGNER_ROLE, IPortalContext, IPortalPage
from pyams_security.schema import PrincipalField, PrincipalsSetField
from pyams_site.interfaces import ISiteRoot
from pyams_utils.interfaces import MISSING_INFO
from pyams_utils.schema import TextLineListField
from pyams_workflow.interfaces import IWorkflowManagedContent, WORKFLOWS_VOCABULARY

__docformat__ = 'restructuredtext'

from pyams_content import _


class IDeletableElement(Interface):
    """Deletable element interface"""

    def is_deletable(self):
        """Check to know if a site element can be deleted"""


CONTENT_MANAGER_ROLES = 'pyams_content.manager.roles'
CONTENT_MANAGER_CONTRIBUTORS = 'pyams_content.manager.roles::contributor'


class IBaseContentManagerRoles(Interface):
    """Shared tool roles interface"""

    webmasters = PrincipalsSetField(title=_("Webmasters"),
                                    description=_("Webmasters can handle all contents, including "
                                                  "published ones"),
                                    role_id=WEBMASTER_ROLE,
                                    required=False)

    pilots = PrincipalsSetField(title=_("Pilots"),
                                description=_("Pilots can handle tool configuration, manage "
                                              "access rules, grant users roles and manage "
                                              "managers restrictions"),
                                role_id=PILOT_ROLE,
                                required=False)

    managers = PrincipalsSetField(title=_("Managers"),
                                  description=_("Managers can handle main operations in tool's "
                                                "workflow, like publish or retire contents"),
                                  role_id=MANAGER_ROLE,
                                  required=False)

    contributors = PrincipalsSetField(title=_("Contributors"),
                                      description=_("Contributors are users which are allowed to "
                                                    "create new contents"),
                                      role_id=CONTRIBUTOR_ROLE,
                                      required=False)

    designers = PrincipalsSetField(title=_("Designers"),
                                   description=_("Designers are users which are allowed to "
                                                 "manage presentation templates"),
                                   role_id=DESIGNER_ROLE,
                                   required=False)


class ISharedSite(IBaseContent, IDeletableElement):
    """Shared site interface"""

    containers(ISiteRoot)

    content_name = Attribute("Site content name")


class ISharedToolContainer(IBaseContent, IContainer):
    """Shared tools container"""

    containers(ISiteRoot)
    contains('.ISharedTool')


DEFAULT_CONTENT_WORKFLOW = 'pyams_content.workflow.default'
BASIC_CONTENT_WORKFLOW = 'pyams_content.workflow.basic'


class SHARED_TOOL_FOLDER_MODES(Enum):
    """Shared tool inner folder modes"""
    NONE = MISSING_INFO
    YEAR_FOLDER = 'year'
    MONTH_FOLDER = 'month'


SHARED_TOOL_FOLDER_MODES_LABELS = OrderedDict((
    (SHARED_TOOL_FOLDER_MODES.NONE.value, _("Don't use inner folders")),
    (SHARED_TOOL_FOLDER_MODES.YEAR_FOLDER.value, _("Use inner year folders")),
    (SHARED_TOOL_FOLDER_MODES.MONTH_FOLDER.value, _("Use inner year and month folders"))
))

SHARED_TOOL_FOLDER_MODES_VOCABULARY = SimpleVocabulary([
    SimpleTerm(v, title=t)
    for v, t in SHARED_TOOL_FOLDER_MODES_LABELS.items()
])


class IBaseSharedTool(IBaseContent, IContainer):
    """Base shared tool interface"""

    containers(ISharedToolContainer)

    shared_content_menu = Attribute("Boolean flag indicating if tool is displayed into 'Shared "
                                    "contents' or Shared tools' menu")

    shared_content_workflow = Choice(title=_("Workflow name"),
                                     description=_("Name of workflow utility used to manage tool "
                                                   "contents"),
                                     vocabulary=WORKFLOWS_VOCABULARY,
                                     default=DEFAULT_CONTENT_WORKFLOW)
    
    inner_folders_mode = Choice(title=_("Use inner folders"),
                                description=_("Defines if inner folders are used to store shared contents"),
                                vocabulary=SHARED_TOOL_FOLDER_MODES_VOCABULARY,
                                default=SHARED_TOOL_FOLDER_MODES.NONE.value,
                                required=True)


SHARED_TOOL_WORKFLOW_STATES_VOCABULARY = 'pyams_content.workflow.states'


class ISharedTool(IBaseSharedTool):
    """Shared tool interface"""

    contains('.ISharedContent')

    shared_content_type = Attribute("Shared data content type name")

    label = I18nTextLineField(title=_("Single content label"),
                              description=_("This label can be used to tag content type of a single content "
                                            "in place of shared tool title"),
                              required=False)

    navigation_label = I18nTextLineField(title=_("Navigation label"),
                                         description=_("Label used for navigation entries"),
                                         required=False)

    facets_label = I18nTextLineField(title=_("Facets label"),
                                     description=_("Label used for the facets of views or search engines, "
                                                   "instead of the standard label"),
                                     required=False)

    facets_type_label = I18nTextLineField(title=_("Facets type label"),
                                          description=_("Label used for the facets of views or search engine, "
                                                        "instead of the standard label, when facets are "
                                                        "configured in \"content-type\" mode"),
                                          required=False)

    dashboard_label = I18nTextLineField(title=_("Dashboards label"),
                                        description=_("Optional label used for dashboards presentation"),
                                        required=False)


class ISharedToolPortalContext(ISharedTool, IPortalContext):
    """Shared tool with portal context"""


class ISharedToolRoles(IBaseContentManagerRoles):
    """Shared tool roles"""
    
    
class ISharedToolInnerFolder(Interface):
    """Shared tool inner folder marker interface"""


class IWfSharedContent(IBaseContent):
    """Shared content interface"""

    content_type = Attribute("Content data type")
    content_name = Attribute("Content name")
    content_intf = Attribute("Content interface")
    content_view = Attribute("Available for views searching")

    content_url = TextLine(title=_("Content URL"),
                           description=_("URL used to access this content; this is important for "
                                         "SEO and should include most important words describing "
                                         "content; spaces and underscores will be automatically "
                                         "replaced by hyphens"),
                           required=True)

    creator = PrincipalField(title=_("Version creator"),
                             description=_("Name of content's version creator. "
                                           "The creator of the first version is also it's "
                                           "owner."),
                             required=True)

    first_owner = PrincipalField(title=_("First owner"),
                                 description=_("Name of content's first version owner"),
                                 required=True,
                                 readonly=True)

    creation_label = TextLine(title=_("Version creation"),
                              readonly=True)

    modifiers = PrincipalsSetField(title=_("Version modifiers"),
                                   description=_("List of principals who modified this content"),
                                   required=False)

    last_modifier = PrincipalField(title=_("Last modifier"),
                                   description=_("Last principal who modified this content"),
                                   required=False)

    last_update_label = TextLine(title=_("Last update"),
                                 readonly=True)

    header = I18nTextField(title=_("Header"),
                           description=_("Content's header is generally displayed in page "
                                         "header"),
                           required=False)

    description = I18nTextField(title=_("Meta-description"),
                                description=_("The content's description is 'hidden' into HTML's "
                                              "page headers; but it can be seen, for example, in "
                                              "some search engines results as content's "
                                              "description; if description is empty, content's "
                                              "header will be used."),
                                required=False)

    keywords = TextLineListField(title=_("Keywords"),
                                 description=_("They will be included into HTML pages metadata"),
                                 required=False)

    notepad = Text(title=_("Notepad"),
                   description=_("Internal information to be known about this content"),
                   required=False)


class IPreventSharedContentUpdateSubscribers(Interface):
    """Shared content update subscribers handler"""


class IBaseContentPortalContext(IPortalContext):
    """Content portal context interface"""


class IWfSharedContentPortalContext(IWfSharedContent, IBaseContentPortalContext):
    """Shared content with portal support"""


class ISharedContentPortalPage(IPortalPage):
    """Shared content portal page interface"""


SHARED_CONTENT_ROLES = 'pyams_content.content.roles'


class IWfSharedContentRoles(Interface):
    """Shared content roles"""

    owner = PrincipalsSetField(title=_("Content owner"),
                               description=_("The owner is the creator of content's first "
                                             "version, except if it was transferred afterwards "
                                             "to another owner"),
                               role_id=OWNER_ROLE,
                               required=True,
                               max_length=1)

    managers = PrincipalsSetField(title=_("Managers"),
                                  description=_("Managers can handle main operations in tool's "
                                                "workflow, like publish or retire contents"),
                                  role_id=MANAGER_ROLE,
                                  required=False)

    contributors = PrincipalsSetField(title=_("Contributors"),
                                      description=_("Contributors are users which are allowed "
                                                    "to update this content in addition to "
                                                    "it's owner"),
                                      role_id=CONTRIBUTOR_ROLE,
                                      required=False)

    designers = PrincipalsSetField(title=_("Designers"),
                                   description=_("Designers are users which are allowed to "
                                                 "manage presentation templates"),
                                   role_id=DESIGNER_ROLE,
                                   required=False)

    readers = PrincipalsSetField(title=_("Readers"),
                                 description=_("Readers are users which are asked to verify and "
                                               "comment contents before they are published"),
                                 role_id=READER_ROLE,
                                 required=False)

    guests = PrincipalsSetField(title=_("Guests"),
                                description=_("Guests are users which are allowed to view "
                                              "contents with restricted access"),
                                role_id=GUEST_ROLE,
                                required=False)


class ISharedContent(IWorkflowManagedContent):
    """Workflow managed shared content interface"""

    content_type = Attribute("Content type interface")
    content_name = Attribute("Content name")
    content_factory = Attribute("Content factory attribute")
    content_view = Attribute("Available for views searching")

    visible_version = Attribute("Link to actually visible version")


CONTENT_TYPES_VOCABULARY = 'pyams_content.content.types'

SHARED_CONTENT_TYPES_VOCABULARY = 'pyams_content.shared_content.types'

VIEWS_SHARED_CONTENT_TYPES_VOCABULARY = 'pyams_content.shared_content.types.views'


#
# Generic restrictions interfaces
#

class ISharedToolRestrictions(Interface):
    """Base shared tool restrictions interface"""

    def new_restrictions(self, principal):
        """Create new restrictions for given principal"""

    def set_restrictions(self, principal, restrictions=None, interface=None):
        """Set restrictions for given principal"""

    def get_restrictions(self, principal, create_if_empty=False):
        """Get restrictions for given principal"""

    def drop_restrictions(self, principal):
        """Drop restrictions for given principal"""

    def can_access(self, context, permission, request=None):
        """Check if given request can get access to context with given permission"""


class IPrincipalRestrictions(IAttributeAnnotatable):
    """Principal restrictions base class"""

    principal_id = PrincipalField(title=_("Principal ID"),
                                  required=True)


class IRestrictionInfo(Interface):
    """Base restriction interface"""

    weight = Attribute("Adapter ordering weight")

    def can_access(self, context, permission, request):
        """Check if given context can be accessed with given permission"""


#
# Contributors restrictions
#

CONTRIBUTORS_RESTRICTIONS_KEY = 'pyams_content.restrictions.contributors'


class IContributorRestrictions(ISharedToolRestrictions):
    """Contributor restrictions marker interface"""


CONTRIBUTOR_WORKFLOW_RESTRICTIONS_KEY = f'{CONTRIBUTORS_RESTRICTIONS_KEY}::workflow'


class IContributorWorkflowRestrictions(IRestrictionInfo):
    """Base contributor workflow restrictions interface"""

    show_workflow_warning = Bool(title=_("Show workflow checks warning"),
                                 description=_("If 'yes', this contributor will have to confirm "
                                               "that contents have been checked before asking "
                                               "for publication"),
                                 required=True,
                                 default=True)

    owners = PrincipalsSetField(title=_("Substitute for"),
                                description=_("Contributor will have access to contents owned "
                                              "by these principals"),
                                required=False)


#
# Managers restrictions
#

MANAGERS_RESTRICTIONS_KEY = 'pyams_content.restrictions.managers'


class IManagerRestrictions(ISharedToolRestrictions):
    """Manager restrictions marker interface"""


MANAGER_WORKFLOW_RESTRICTIONS_KEY = f'{MANAGERS_RESTRICTIONS_KEY}::workflow'


class IManagerWorkflowRestrictions(IRestrictionInfo):
    """Base manager workflow restrictions interface"""

    show_workflow_warning = Bool(title=_("Publication checks"),
                                 description=_("If 'yes', this manager will have to confirm that "
                                               "contents have been previewed and checked before "
                                               "publishing a content"),
                                 required=True,
                                 default=True)

    restricted_contents = Bool(title=_("Restricted contents"),
                               description=_("If 'yes', this manager will get restricted access "
                                             "to manage contents based on selected settings"),
                               required=True,
                               default=True)

    owners = PrincipalsSetField(title=_("Selected owners"),
                                description=_("Manager will have access to contents owned "
                                              "by these principals"),
                                required=False)


#
# Shared content specificities paragraph
#

SPECIFICITIES_PARAGRAPH_TYPE = 'specificities'
SPECIFICITIES_PARAGRAPH_NAME = _("Content specificities")
SPECIFICITIES_PARAGRAPH_RENDERERS = 'PyAMS_content.paragraph.specificities.renderers'
SPECIFICITIES_PARAGRAPH_ICON_CLASS = 'fas fa-tools'


class ISpecificitiesParagraph(IBaseParagraph):
    """Specificities paragraph interface"""

    renderer = ParagraphRendererChoice(description=_("Presentation template used for these specificities"),
                                       renderers=SPECIFICITIES_PARAGRAPH_RENDERERS)
