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

"""PyAMS_content.shared.site.zmi.widget.interfaces module

"""

__docformat__ = 'restructuredtext'

from zope.interface import Attribute

from pyams_form.interfaces import INPUT_MODE
from pyams_form.interfaces.widget import ITextWidget
from pyams_form.template import widget_template_config
from pyams_zmi.interfaces import IAdminLayer


@widget_template_config(mode=INPUT_MODE,
                        template='templates/folder-select-input.pt',
                        layer=IAdminLayer)
class ISiteManagerFoldersSelectorWidget(ITextWidget):
    """Site manager folders selector widget interface"""

    permission = Attribute("Permission required to select a given node")
