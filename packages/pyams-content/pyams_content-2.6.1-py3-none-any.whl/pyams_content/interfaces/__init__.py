#
# Copyright (c) 2015-2019 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.interfaces package

This module defines main content permissions, roles and interfaces.
"""

from zope.annotation import IAttributeAnnotatable
from zope.interface import Interface
from zope.location.interfaces import IContained
from zope.schema import Datetime, Set, TextLine

from pyams_i18n.schema import I18nTextLineField


__docformat__ = 'restructuredtext'

from pyams_content import _


#
# Custom permissions
#

MANAGE_SITE_ROOT_PERMISSION = 'pyams.ManageSiteRoot'
'''Permission required to manage main site root properties'''

MANAGE_REFERENCE_TABLE_PERMISSION = 'pyams.ManageReferenceTable'
'''Permission required to manage reference table properties'''

MANAGE_SITE_TREE_PERMISSION = 'pyams.ManageSiteTree'
'''Permission required to create first level site elements'''

MANAGE_SITE_PERMISSION = 'pyams.ManageSite'
'''Permission required to manager inner site or blog properties'''

MANAGE_TOOL_PERMISSION = 'pyams.ManageTool'
'''Permission required to manager shared tool properties'''

CREATE_CONTENT_PERMISSION = 'pyams.CreateContent'
'''Permission required to create a new content'''

CREATE_VERSION_PERMISSION = 'pyams.CreateVersion'
'''Permission required to create a new version of an existing content'''

MANAGE_CONTENT_PERMISSION = 'pyams.ManageContent'
'''Permission required to manager properties of an existing content'''

COMMENT_CONTENT_PERMISSION = 'pyams.CommentContent'
'''Permission required to add comments on an existing content'''

PUBLISH_CONTENT_PERMISSION = 'pyams.PublishContent'
'''Permission required to publish or retire an existing content'''


#
# Custom roles
#

WEBMASTER_ROLE = 'pyams.Webmaster'
'''Webmaster role has all permissions on all contents'''

REFERENCE_MANAGER_ROLE = 'pyams.ReferenceManager'
'''References manager role has permissions to handle references tables'''

PILOT_ROLE = 'pyams.Pilot'
'''Pilot role is allowed to manage tools configuration and permissions'''

MANAGER_ROLE = 'pyams.Manager'
'''Manager role is allowed to manage contents workflow'''

OWNER_ROLE = 'pyams.Owner'
'''Content owner role is allowed to manage content properties until publication'''

CONTRIBUTOR_ROLE = 'pyams.Contributor'
'''Contributor role is allowed to create new contents'''

READER_ROLE = 'pyams.Reader'
'''Reader role is allowed to read and comment contents while still in draft state'''

OPERATOR_ROLE = 'pyams.Operator'
'''Operator role is allowed to access management interface'''

GUEST_ROLE = 'pyams.Guest'
'''Guest role is allowed to view contents'''


#
# Custom routes
#

OID_ACCESS_ROUTE = 'pyams_content.oid_access'
'''"/+/oid" direct access route name'''

OID_ACCESS_PATH = '/+/{oid}*view'
'''"/+/oid" direct access path'''


#
# Base content interfaces
#

class IBaseContent(IContained, IAttributeAnnotatable):
    """Base content interface"""

    __name__ = TextLine(title=_("Unique key"),
                        description=_("WARNING: this key can't be modified after creation!!! "
                                      "Spaces, uppercase letters or accentuated characters will "
                                      "be replaced automatically."),
                        required=True)

    title = I18nTextLineField(title=_("Title"),
                              description=_("Visible label used to display content"),
                              required=True)

    short_name = I18nTextLineField(title=_("Short name"),
                                   description=_("Short name used in breadcrumbs"),
                                   required=True)


class IBaseContentInfo(Interface):
    """Base content info interface"""

    created_date = Datetime(title=_("Creation date"),
                            required=False,
                            readonly=True)

    modified_date = Datetime(title=_("Modification date"),
                             required=False,
                             readonly=False)


class IObjectType(Interface):
    """Object type value interface"""


class IObjectTypes(Interface):
    """Object types """

    object_types = Set(title=_("Object types"),
                       value_type=TextLine(),
                       required=False)
