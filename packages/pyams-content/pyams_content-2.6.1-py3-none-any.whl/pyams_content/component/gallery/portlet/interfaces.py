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

"""PyAMS_content.component.gallery.portlet module

This module defines interfaces of portlets which can be used to display a medias gallery.
"""

from zope.schema import Bool

from pyams_content.component.gallery.interfaces import IGalleryContainer
from pyams_i18n.schema import I18nTextLineField
from pyams_portal.interfaces import IPortletSettings


__docformat__ = 'restructuredtext'

from pyams_content import _


class IGalleryPortletSettings(IPortletSettings, IGalleryContainer):
    """Gallery portlet settings interface"""

    title = I18nTextLineField(title=_("Title"),
                              description=_("Main component title"),
                              required=False)

    use_context_gallery = Bool(title=_("Use context gallery"),
                               description=_("If 'yes' and if the displayed context supports "
                                             "medias galleries, this gallery will be used to "
                                             "get medias"),
                               required=True,
                               default=False)

    def get_visible_medias(self, context):
        """Get iterator over visible medias"""
