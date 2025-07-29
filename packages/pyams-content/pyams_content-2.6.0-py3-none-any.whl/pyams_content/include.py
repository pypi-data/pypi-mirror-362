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

"""PyAMS_content.include module

This module is used for Pyramid integration.
"""

import re

from zope.interface import classImplements

from pyams_content.component.extfile.interfaces import IExtFileManagerTarget
from pyams_content.component.links.interfaces import IExternalLinksManagerTarget
from pyams_content.component.thesaurus import ICollectionsManagerTarget, ITagsManagerTarget, \
    IThemesManagerTarget
from pyams_content.feature.preview.interfaces import IPreviewTarget
from pyams_content.feature.redirect.interfaces import IRedirectionManagerTarget
from pyams_content.feature.script.interfaces import IScriptContainerTarget
from pyams_content.interfaces import COMMENT_CONTENT_PERMISSION, CONTRIBUTOR_ROLE, \
    CREATE_CONTENT_PERMISSION, CREATE_VERSION_PERMISSION, GUEST_ROLE, MANAGER_ROLE, \
    MANAGE_CONTENT_PERMISSION, MANAGE_REFERENCE_TABLE_PERMISSION, MANAGE_SITE_PERMISSION, MANAGE_SITE_ROOT_PERMISSION, \
    MANAGE_SITE_TREE_PERMISSION, MANAGE_TOOL_PERMISSION, OID_ACCESS_PATH, OID_ACCESS_ROUTE, OPERATOR_ROLE, OWNER_ROLE, \
    PILOT_ROLE, PUBLISH_CONTENT_PERMISSION, READER_ROLE, REFERENCE_MANAGER_ROLE, WEBMASTER_ROLE
from pyams_layer.interfaces import MANAGE_SKIN_PERMISSION
from pyams_security.interfaces.base import MANAGE_PERMISSION, MANAGE_ROLES_PERMISSION, \
    PUBLIC_PERMISSION, ROLE_ID, VIEW_PERMISSION, VIEW_SYSTEM_PERMISSION
from pyams_security.interfaces.names import ADMIN_USER_ID, SYSTEM_ADMIN_ROLE
from pyams_site.site import BaseSiteRoot
from pyams_thesaurus.interfaces import ADMIN_THESAURUS_PERMISSION, CREATE_THESAURUS_PERMISSION, \
    MANAGE_THESAURUS_CONTENT_PERMISSION, MANAGE_THESAURUS_EXTRACT_PERMISSION

try:
    from pyams_gis.interfaces import MANAGE_MAPS_PERMISSION
except ImportError:
    MANAGE_MAPS_PERMISSION = None
    
__docformat__ = 'restructuredtext'

from pyams_content import _


def include_package(config):
    """Pyramid package include"""

    # add translations
    config.add_translation_dirs('pyams_content:locales')

    # register permissions
    config.register_permission({
        'id': MANAGE_SITE_ROOT_PERMISSION,
        'title': _("Manage main site root properties")
    })
    config.register_permission({
        'id': MANAGE_REFERENCE_TABLE_PERMISSION,
        'title': _("Manage references table")
    })
    config.register_permission({
        'id': MANAGE_SITE_TREE_PERMISSION,
        'title': _("Manage first level site tree elements")
    })
    config.register_permission({
        'id': MANAGE_SITE_PERMISSION,
        'title': _("Manage site, blog or hub properties")
    })
    config.register_permission({
        'id': MANAGE_TOOL_PERMISSION,
        'title': _("Manage shared tool properties")
    })
    config.register_permission({
        'id': CREATE_CONTENT_PERMISSION,
        'title': _("Create new content")
    })
    config.register_permission({
        'id': CREATE_VERSION_PERMISSION,
        'title': _("Create new version of existing content")
    })
    config.register_permission({
        'id': MANAGE_CONTENT_PERMISSION,
        'title': _("Manage content properties")
    })
    config.register_permission({
        'id': COMMENT_CONTENT_PERMISSION,
        'title': _("Comment existing content")
    })
    config.register_permission({
        'id': PUBLISH_CONTENT_PERMISSION,
        'title': _("Publish or retire existing content")
    })

    # upgrade system manager roles
    config.upgrade_role(SYSTEM_ADMIN_ROLE,
                        permissions={
                            MANAGE_SITE_ROOT_PERMISSION, MANAGE_REFERENCE_TABLE_PERMISSION,
                            MANAGE_SITE_TREE_PERMISSION, MANAGE_SITE_PERMISSION,
                            MANAGE_TOOL_PERMISSION, CREATE_CONTENT_PERMISSION,
                            CREATE_VERSION_PERMISSION, MANAGE_CONTENT_PERMISSION,
                            COMMENT_CONTENT_PERMISSION, PUBLISH_CONTENT_PERMISSION
                        })
    if MANAGE_MAPS_PERMISSION:
        config.upgrade_role(SYSTEM_ADMIN_ROLE,
                            permissions={MANAGE_MAPS_PERMISSION})

    # register new roles
    config.register_role({
        'id': WEBMASTER_ROLE,
        'title': _("Webmaster (role)"),
        'permissions': {
            PUBLIC_PERMISSION, VIEW_PERMISSION, MANAGE_PERMISSION,
            VIEW_SYSTEM_PERMISSION, MANAGE_ROLES_PERMISSION,
            CREATE_THESAURUS_PERMISSION, ADMIN_THESAURUS_PERMISSION,
            MANAGE_THESAURUS_CONTENT_PERMISSION, MANAGE_THESAURUS_EXTRACT_PERMISSION,
            MANAGE_SITE_ROOT_PERMISSION, MANAGE_REFERENCE_TABLE_PERMISSION,
            MANAGE_SITE_TREE_PERMISSION, MANAGE_SITE_PERMISSION,
            MANAGE_TOOL_PERMISSION, CREATE_CONTENT_PERMISSION,
            CREATE_VERSION_PERMISSION, MANAGE_CONTENT_PERMISSION,
            COMMENT_CONTENT_PERMISSION, PUBLISH_CONTENT_PERMISSION,
            MANAGE_SKIN_PERMISSION
        },
        'managers': {
            ADMIN_USER_ID,
            ROLE_ID.format(SYSTEM_ADMIN_ROLE)
        }
    })
    if MANAGE_MAPS_PERMISSION:
        config.upgrade_role(WEBMASTER_ROLE,
                            permissions={MANAGE_MAPS_PERMISSION})
        
    config.register_role({
        'id': REFERENCE_MANAGER_ROLE,
        'title': _("References manager (role)"),
        'permissions': {
            PUBLIC_PERMISSION, VIEW_PERMISSION, VIEW_SYSTEM_PERMISSION,
            MANAGE_REFERENCE_TABLE_PERMISSION
        },
        'managers': {
            ADMIN_USER_ID,
            ROLE_ID.format(SYSTEM_ADMIN_ROLE),
            ROLE_ID.format(WEBMASTER_ROLE)
        }
    })

    config.register_role({
        'id': PILOT_ROLE,
        'title': _("Pilot (role)"),
        'permissions': {
            PUBLIC_PERMISSION, VIEW_PERMISSION, MANAGE_PERMISSION,
            VIEW_SYSTEM_PERMISSION, MANAGE_ROLES_PERMISSION,
            MANAGE_SITE_PERMISSION, MANAGE_TOOL_PERMISSION,
            MANAGE_CONTENT_PERMISSION, COMMENT_CONTENT_PERMISSION,
            PUBLISH_CONTENT_PERMISSION
        },
        'managers': {
            ADMIN_USER_ID,
            ROLE_ID.format(SYSTEM_ADMIN_ROLE),
            ROLE_ID.format(WEBMASTER_ROLE)
        }
    })
    
    config.register_role({
        'id': MANAGER_ROLE,
        'title': _("Manager (role)"),
        'permissions': {
            PUBLIC_PERMISSION, VIEW_PERMISSION, MANAGE_PERMISSION,
            VIEW_SYSTEM_PERMISSION, MANAGE_CONTENT_PERMISSION,
            CREATE_VERSION_PERMISSION, COMMENT_CONTENT_PERMISSION,
            PUBLISH_CONTENT_PERMISSION
        },
        'managers': {
            ADMIN_USER_ID,
            ROLE_ID.format(SYSTEM_ADMIN_ROLE),
            ROLE_ID.format(WEBMASTER_ROLE),
            ROLE_ID.format(PILOT_ROLE)
        }
    })

    config.register_role({
        'id': OWNER_ROLE,
        'title': _("Owner (role)"),
        'permissions': {
            PUBLIC_PERMISSION, VIEW_PERMISSION, MANAGE_PERMISSION,
            VIEW_SYSTEM_PERMISSION, MANAGE_ROLES_PERMISSION,
            MANAGE_CONTENT_PERMISSION, CREATE_VERSION_PERMISSION,
            COMMENT_CONTENT_PERMISSION
        }
    })

    config.register_role({
        'id': CONTRIBUTOR_ROLE,
        'title': _("Contributor (role)"),
        'permissions': {
            PUBLIC_PERMISSION, VIEW_PERMISSION, MANAGE_PERMISSION,
            VIEW_SYSTEM_PERMISSION, CREATE_CONTENT_PERMISSION,
            MANAGE_CONTENT_PERMISSION, CREATE_VERSION_PERMISSION,
            COMMENT_CONTENT_PERMISSION
        },
        'managers': {
            ADMIN_USER_ID,
            ROLE_ID.format(SYSTEM_ADMIN_ROLE),
            ROLE_ID.format(WEBMASTER_ROLE),
            ROLE_ID.format(PILOT_ROLE),
            ROLE_ID.format(OWNER_ROLE)
        }
    })

    config.register_role({
        'id': READER_ROLE,
        'title': _("Reader (role)"),
        'permissions': {
            PUBLIC_PERMISSION, VIEW_PERMISSION, MANAGE_PERMISSION,
            VIEW_SYSTEM_PERMISSION, COMMENT_CONTENT_PERMISSION
        },
        'managers': {
            ADMIN_USER_ID,
            ROLE_ID.format(SYSTEM_ADMIN_ROLE),
            ROLE_ID.format(WEBMASTER_ROLE),
            ROLE_ID.format(PILOT_ROLE),
            ROLE_ID.format(MANAGER_ROLE),
            ROLE_ID.format(OWNER_ROLE),
            ROLE_ID.format(CONTRIBUTOR_ROLE)
        }
    })
    
    config.register_role({
        'id': OPERATOR_ROLE,
        'title': _("Operator (role)"),
        'permissions': {
            PUBLIC_PERMISSION, VIEW_PERMISSION, VIEW_SYSTEM_PERMISSION
        },
        'managers': {
            ADMIN_USER_ID,
            ROLE_ID.format(SYSTEM_ADMIN_ROLE)
        }
    })
    
    config.register_role({
        'id': GUEST_ROLE,
        'title': _("Guest user (role)"),
        'permissions': {
            PUBLIC_PERMISSION, VIEW_PERMISSION
        },
        'managers': {
            ADMIN_USER_ID,
            ROLE_ID.format(SYSTEM_ADMIN_ROLE),
            ROLE_ID.format(WEBMASTER_ROLE),
            ROLE_ID.format(PILOT_ROLE),
            ROLE_ID.format(MANAGER_ROLE),
            ROLE_ID.format(OWNER_ROLE),
            ROLE_ID.format(CONTRIBUTOR_ROLE)
        }
    })

    # site root extensions
    classImplements(BaseSiteRoot, IExtFileManagerTarget)
    classImplements(BaseSiteRoot, IExternalLinksManagerTarget)
    classImplements(BaseSiteRoot, ITagsManagerTarget)
    classImplements(BaseSiteRoot, IThemesManagerTarget)
    classImplements(BaseSiteRoot, ICollectionsManagerTarget)
    classImplements(BaseSiteRoot, IScriptContainerTarget)
    classImplements(BaseSiteRoot, IRedirectionManagerTarget)
    classImplements(BaseSiteRoot, IPreviewTarget)

    # custom routes
    config.add_route(OID_ACCESS_ROUTE,
                     config.registry.settings.get(f'{OID_ACCESS_ROUTE}_route.path',
                                                  OID_ACCESS_PATH))

    try:
        import pyams_zmi  # pylint: disable=import-outside-toplevel,unused-import
    except ImportError:
        config.scan(ignore=[re.compile(r'pyams_content\..*\.zmi\.?.*').search])
    else:
        config.scan()
