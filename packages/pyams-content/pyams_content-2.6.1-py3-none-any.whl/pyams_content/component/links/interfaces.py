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

"""PyAMS_content.component.links.interfaces module

"""

from zope.interface import Attribute, Interface
from zope.schema import Bool, Choice, InterfaceField, TextLine, URI

from pyams_content.component.association.interfaces import IAssociationContainerTarget, \
    IAssociationItem
from pyams_content.reference.pictogram.interfaces import SELECTED_PICTOGRAM_VOCABULARY
from pyams_i18n.interfaces import BASE_LANGUAGES_VOCABULARY_NAME
from pyams_i18n.schema import I18nTextField, I18nTextLineField
from pyams_sequence.interfaces import IInternalReference
from pyams_utils.schema import MailAddressField, TextLineListField

__docformat__ = 'restructuredtext'

from pyams_content import _


CONTENT_LINKS_VOCABULARY = 'pyams_content.links'


class IBaseLink(IAssociationItem):
    """Base link interface"""

    title = I18nTextLineField(title=_("Alternate title"),
                              description=_("Link title, as shown in front-office"),
                              required=False)

    description = I18nTextField(title=_("Description"),
                                description=_(
                                    "Link description displayed by front-office template"),
                                required=False)

    pictogram_name = Choice(title=_("Pictogram"),
                            description=_("Name of the pictogram associated with this link"),
                            required=False,
                            vocabulary=SELECTED_PICTOGRAM_VOCABULARY)

    pictogram = Attribute("Selected pictogram object")

    def get_editor_url(self):
        """Get URL for use in HTML editor"""


INTERNAL_LINK_ICON_CLASS = 'fas fa-sign-in-alt fa-rotate-270'
INTERNAL_LINK_ICON_HINT = _("Internal link")


class IInternalLink(IBaseLink, IInternalReference):
    """Internal link interface"""

    force_canonical_url = Bool(title=_("Force canonical URL?"),
                               description=_("By default, internal links use a \"relative\" URL, "
                                             "which tries to display link target in the current "
                                             "context; by using a canonical URL, you can display "
                                             "target in it's attachment context (if defined)"),
                               required=False,
                               default=False)


#
# Custom internal link properties support
# These interfaces are used to be able to add custom properties to an internal link
# when it's target is of a given content type
#

class IInternalLinkCustomInfoTarget(Interface):
    """Internal link target info

    This optional interface can be supported be any content to be able to provide any
    additional information to link properties
    """

    internal_link_marker_interface = InterfaceField(title=_("Marker interface provided by links "
                                                            "directed to contents supporting "
                                                            "this interface"))


class ICustomInternalLinkTarget(Interface):
    """Base interface for custom internal link target"""


class IInternalLinkCustomInfo(Interface):
    """Base interface for custom link properties"""

    properties_interface = InterfaceField(title=_("Info properties interface"))

    def get_url_params(self):
        """Get custom params to generate link URL"""


EXTERNAL_LINK_ICON_CLASS = 'fas fa-link'
EXTERNAL_LINK_ICON_HINT = _("External link")


class IExternalLink(IBaseLink):
    """External link interface"""

    url = URI(title=_("Target URL"),
              description=_("URL used to access external resource"),
              required=True)

    language = Choice(title=_("Language"),
                      description=_("Language used in this remote resource"),
                      vocabulary=BASE_LANGUAGES_VOCABULARY_NAME,
                      required=False)


MAILTO_LINK_ICON_CLASS = 'fas fa-envelope'
MAILTO_LINK_ICON_HINT = _("Mailto link")


class IMailtoLink(IBaseLink):
    """Mailto link interface"""

    address = MailAddressField(title=_("Target address"),
                               description=_("Target email address"),
                               required=True)

    address_name = TextLine(title=_("Address name"),
                            description=_("Address as displayed in address book"),
                            required=True)


class ILinkContainerTarget(IAssociationContainerTarget):
    """Links container marker interface"""


#
# External links management
#

EXTERNAL_LINKS_MANAGER_INFO_KEY = 'pyams_content.links.manager'


class IExternalLinksManagerInfo(Interface):
    """External links manager info interface"""

    check_external_links = Bool(title=_("Check external links"),
                                description=_("If selected, contributors will not be able to create "
                                              "external links to internal site contents"),
                                required=True,
                                default=False)

    forbidden_hosts = TextLineListField(title=_("Forbidden hosts"),
                                        description=_("List of hosts (including protocol) for which "
                                                      "creation of external links is forbidden"),
                                        required=False)


class IExternalLinksManagerTarget(Interface):
    """External links manager target interface"""
