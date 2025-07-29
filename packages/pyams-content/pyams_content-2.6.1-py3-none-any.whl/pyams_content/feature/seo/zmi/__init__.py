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

"""PyAMS_content.feature.seo.zmi module

MThis module provides management interface components for SEO related information.
"""

from pyams_content.feature.seo import ISEOContentInfo
from pyams_content.shared.common import IWfSharedContent
from pyams_form.field import Fields
from pyams_form.interfaces.form import IGroup
from pyams_utils.adapter import adapter_config
from pyams_zmi.form import FormGroupSwitcher
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.form import IPropertiesEditForm

__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(name='seo-config.group',
                context=(IWfSharedContent, IAdminLayer, IPropertiesEditForm),
                provides=IGroup)
class SEOConfigurationEditGroup(FormGroupSwitcher):
    """SEO configuration edit form"""

    legend = _("SEO configuration")
    fields = Fields(ISEOContentInfo)
