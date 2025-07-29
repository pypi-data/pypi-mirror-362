# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from zope.schema.fieldproperty import FieldProperty

from pyams_content.shared.common import SharedContent, WfSharedContent
from pyams_content.shared.common.interfaces import ISharedContent, IWfSharedContent
from pyams_content.shared.logo.interfaces import ILogo, IWfLogo, LOGO_CONTENT_NAME, LOGO_CONTENT_TYPE
from pyams_file.property import I18nFileProperty
from pyams_i18n.interfaces import II18n
from pyams_sequence.reference import InternalReferenceMixin
from pyams_utils.factory import factory_config


@factory_config(IWfLogo)
@factory_config(IWfSharedContent, name=LOGO_CONTENT_TYPE)
class WfLogo(WfSharedContent, InternalReferenceMixin):
    """Logo persistent class"""
    
    content_type = LOGO_CONTENT_TYPE
    content_name = LOGO_CONTENT_NAME
    content_intf = IWfLogo
    content_view = False
    
    handle_content_url = False
    handle_header = False
    handle_description = False
    
    alt_title = FieldProperty(IWfLogo['alt_title'])
    acronym = FieldProperty(IWfLogo['acronym'])
    image = I18nFileProperty(IWfLogo['image'])
    monochrome_image = I18nFileProperty(IWfLogo['monochrome_image'])
    url = FieldProperty(IWfLogo['url'])
    reference = FieldProperty(IWfLogo['reference'])

    def get_title(self, request):
        return II18n(self).query_attributes_in_order(('alt_title', 'title'),
                                                     request=request)


@factory_config(ILogo)
@factory_config(ISharedContent, name=LOGO_CONTENT_TYPE)
class Logo(SharedContent):
    """Workflow managed logo persistent class"""

    content_type = LOGO_CONTENT_TYPE
    content_name = LOGO_CONTENT_NAME
    content_view = False
    