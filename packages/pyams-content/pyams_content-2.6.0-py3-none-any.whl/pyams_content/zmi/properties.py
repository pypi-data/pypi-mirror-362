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

"""PyAMS_content.shared.common.zmi.properties module

This module defines base classes for properties edit forms.
"""

from zope.interface import implementer

from pyams_zmi.interfaces.form import IPropertiesEditForm
from pyams_zmi.form import AdminEditForm


__docformat__ = 'restructuredtext'


@implementer(IPropertiesEditForm)
class PropertiesEditForm(AdminEditForm):
    """Properties edit form"""
