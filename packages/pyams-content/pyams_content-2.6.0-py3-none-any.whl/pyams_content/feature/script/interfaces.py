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

"""PyAMS_content.feature.script.interfaces module

This module defines interfaces related to optional scripts management.
"""

from zope.annotation.interfaces import IAttributeAnnotatable
from zope.container.constraints import contains
from zope.container.interfaces import IContainer
from zope.interface import Interface
from zope.schema import Bool, Text, TextLine

from pyams_utils.schema import TextLineListField

__docformat__ = 'restructuredtext'

from pyams_content import _


class IScriptInfo(IAttributeAnnotatable):
    """Base script information interface"""

    active = Bool(title=_("Active script?"),
                  description=_("An inactive script is not included into page resources"),
                  required=True,
                  default=True)

    name = TextLine(title=_("Script name"),
                    description=_("This is just a descriptive name given to the script"),
                    required=True)

    body = Text(title=_("Script body"),
                description=_("Script source code, including the HTML wrapping tag; you can use variables "
                              "by embracing them with {} characters"),
                required=False)

    bottom_script = Bool(title=_("Bottom script?"),
                         description=_("If 'yes', script will be included in page bottom instead of "
                                       "page HTML head"),
                         required=True,
                         default=False)


SCRIPT_CONTAINER_KEY = 'pyams_content.scripts'


class IScriptContainer(IContainer):
    """Script container interface"""

    contains(IScriptInfo)

    def append(self, item):
        """Add script to container"""

    def get_active_items(self):
        """Get iterator over active scripts"""

    def get_top_scripts(self):
        """Get iterator over top scripts"""

    def get_bottom_scripts(self):
        """Get iterator over bottom scripts"""


SCRIPT_SETTINGS_KEY = 'pyams_content.scripts.settings'


class IScriptContainerSettings(Interface):
    """Script container settings interface"""

    variables = TextLineListField(title=_("Scripts params"),
                                  description=_("If your scripts have to use parameters, you can set their "
                                                "values here, using \"NAME=value\" syntax for each parameter; "
                                                "you can add comments by prefixing lines with #"),
                                  required=False)

    def items(self):
        """Get all variables as mapping"""


class IScriptContainerTarget(IAttributeAnnotatable):
    """Script container target marker interface"""
