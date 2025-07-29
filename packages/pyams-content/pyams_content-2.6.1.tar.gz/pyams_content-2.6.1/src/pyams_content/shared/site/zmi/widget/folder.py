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

"""PyAMS_content.shared.site.zmi.widget.folder module

This module provides a custom widget which can be used to select a folder
inside a site manager.
"""

from zope.interface import implementer_only

from pyams_content.shared.site.zmi.widget.interfaces import ISiteManagerFoldersSelectorWidget
from pyams_form.browser.text import TextWidget
from pyams_form.widget import FieldWidget


__docformat__ = 'restructuredtext'


@implementer_only(ISiteManagerFoldersSelectorWidget)
class SiteManagerFoldersSelectorWidget(TextWidget):
    """Site manager folders selector widget"""

    permission = None


def SiteManagerFoldersSelectorFieldWidget(field, request):  # pylint: disable=invalid-name
    """IFieldWidget factory for TextWidget."""
    return FieldWidget(field, SiteManagerFoldersSelectorWidget(request))
