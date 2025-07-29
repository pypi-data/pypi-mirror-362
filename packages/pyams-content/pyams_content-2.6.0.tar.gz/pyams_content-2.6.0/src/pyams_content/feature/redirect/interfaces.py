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

"""PyAMS_content.feature.redirect.interfaces module

This module defines interfaces used to define redirection rules.
"""

from zope.container.constraints import contains
from zope.container.interfaces import IOrderedContainer
from zope.interface import Attribute, Interface, Invalid, invariant
from zope.schema import Bool, Text, TextLine

from pyams_sequence.interfaces import IInternalReference
from pyams_sequence.schema import InternalReferenceField

__docformat__ = 'restructuredtext'

from pyams_content import _


REDIRECT_MANAGER_KEY = 'pyams_content.redirect'


class IRedirectionRule(IInternalReference):
    """Redirection rule interface"""

    active = Bool(title=_("Active rule?"),
                  description=_("If 'no', selected rule is inactive"),
                  required=True,
                  default=False)

    chained = Bool(title=_("Chained rule?"),
                   description=_("If 'no', and if this rule is matching received request URL, the rule "
                                 "returns a redirection response; otherwise, the rule just rewrites the "
                                 "input URL which is forwarded to the next rule"),
                   required=True,
                   default=False)

    label = TextLine(title=_("Label"),
                     description=_("The label of the redirection rule"),
                     required=True)

    permanent = Bool(title=_("Permanent redirect?"),
                     description=_("Define if this redirection should be permanent or temporary"),
                     required=True,
                     default=True)

    url_pattern = TextLine(title=_("URL pattern"),
                           description=_("Regexp pattern of matching URLs for this redirection rule"),
                           required=True)

    pattern = Attribute("Compiled URL pattern")

    reference = InternalReferenceField(title=_("Internal redirection target"),
                                       description=_("Internal redirection reference. You can search a reference using "
                                                     "'+' followed by internal number, of by entering text matching "
                                                     "content title."),
                                       required=False)

    target_url = TextLine(title=_("Target URL"),
                          description=_("URL to which source URL should be redirected"),
                          required=False)

    notepad = Text(title=_("Notepad"),
                   required=False)

    @invariant
    def check_reference_and_target(self):
        if bool(self.reference) == bool(self.target_url):
            raise Invalid(_("You must provide an internal reference OR a target URL"))

    def match(self, source_url):
        """Return regexp URL match on given URL"""

    def rewrite(self, source_url, request):
        """Rewrite given source URL"""


class IRedirectionManager(IOrderedContainer):
    """Redirection manager"""

    contains(IRedirectionRule)

    def get_active_items(self):
        """Get iterator over active items"""

    def get_response(self, request):
        """Get new response for given request"""

    def test_rules(self, source_url, request, check_inactive_rules=False):
        """Test rules against given URL"""


class IRedirectionManagerTarget(Interface):
    """Redirection manager target marker interface"""
