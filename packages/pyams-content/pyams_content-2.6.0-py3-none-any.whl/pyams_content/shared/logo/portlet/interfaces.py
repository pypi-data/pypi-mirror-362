# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from pyams_content.shared.logo import LOGO_CONTENT_TYPE
from pyams_i18n.schema import I18nTextLineField
from pyams_portal.interfaces import IPortletSettings
from pyams_sequence.interfaces import IInternalReferencesList
from pyams_sequence.schema import InternalReferencesListField

__docformat__ = 'restructuredtext'

from pyams_content import _


class ILogosPortletSettings(IPortletSettings, IInternalReferencesList):
    """Logos portlet settings interface"""
    
    title = I18nTextLineField(title=_("Title"),
                              required=False)
    
    references = InternalReferencesListField(title=_("Logos references"),
                                             description=_("List of internal logos references"),
                                             content_type=LOGO_CONTENT_TYPE)
    
    def get_logos(self, status=None, with_reference=False):
        """Get logos from internal references"""
        