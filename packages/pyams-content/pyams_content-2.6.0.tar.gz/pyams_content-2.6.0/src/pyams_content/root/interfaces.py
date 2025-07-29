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

"""PyAMS_content.root.interfaces module

This module defines interfaces which are used for whole site configuration.
"""

from zope.interface import Interface
from zope.schema import Dict, InterfaceField, TextLine, URI

from pyams_content.interfaces import OPERATOR_ROLE, WEBMASTER_ROLE
from pyams_file.schema import ImageField
from pyams_i18n.schema import I18nTextField, I18nTextLineField
from pyams_portal.interfaces import DESIGNER_ROLE
from pyams_security.interfaces import IContentRoles
from pyams_security.schema import PrincipalField, PrincipalsSetField


__docformat__ = 'restructuredtext'

from pyams_content import _
from pyams_utils.schema import MailAddressField

SITE_ROOT_INFOS_KEY = 'pyams_content.root'


class ISiteRootInfos(Interface):
    """Site root information interfaces"""

    title = I18nTextLineField(title=_("Title"),
                              description=_("Application title displayed in title bar"),
                              required=False)

    short_title = I18nTextLineField(title=_("Short title"),
                                    description=_("Application short title visible as "
                                                  "title prefix"),
                                    required=False)

    description = I18nTextField(title=_("Description"),
                                description=_("Main application description"),
                                required=False)

    author = TextLine(title=_("Author"),
                      description=_("Public author name"),
                      required=False)

    icon = ImageField(title=_("Icon"),
                      description=_("Browser favourite icon"),
                      required=False)

    logo = ImageField(title=_("Logo"),
                      description=_("Image containing application logo"),
                      required=False)

    public_url = URI(title=_("Public site URI"),
                     description=_("Base URL of the public site"),
                     required=False)

    support_email = MailAddressField(title=_("Support email"),
                                     description=_("Public support email address"),
                                     required=False)


SITEROOT_ROLES = 'pyams_content.root.roles'


class ISiteRootRoles(IContentRoles):
    """Main site roles"""

    webmasters = PrincipalsSetField(title=_("Webmasters"),
                                    description=_("These principals can handle all settings and "
                                                  "contents of web site, except for a few ones "
                                                  "which require administrator access"),
                                    role_id=WEBMASTER_ROLE,
                                    required=False)

    designers = PrincipalsSetField(title=_("Templates managers"),
                                   description=_("These principals can only handle presentation "
                                                 "templates"),
                                   role_id=DESIGNER_ROLE,
                                   required=False)

    operators = PrincipalField(title=_("Operators group"),
                               description=_("Name of group containing all roles owners"),
                               role_id=OPERATOR_ROLE,
                               required=False)

    def get_operators_group(self):
        """Get operators groups instance"""


SITE_ROOT_TOOLS_CONFIGURATION_KEY = 'pyams_content.root.configuration'


class ISiteRootToolsConfiguration(Interface):
    """Site root shared tools configuration"""

    tables_manager_name = TextLine(title="Tables manager name")
    tables_names = Dict(title="References tables names",
                        key_type=InterfaceField(),
                        value_type=TextLine())

    def check_table(self, interface, table_name, registry):
        """Check or create given table from factory

        :param interface: provided table interface
        :param table_name: default table name
        :param registry: current registry
        """

    tools_manager_name = TextLine(title="Shared tools manager name")
    tools_names = Dict(title="Shared tools names",
                       key_type=InterfaceField(),
                       value_type=TextLine())

    def check_tool(self, interface, tool_name, registry):
        """Check or create given shared tool from factory

        :param interface: provided shared tool interface
        :param tool_name: default tool name
        :param registry: current registry
        """
