# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

__docformat__ = 'restructuredtext'

from pyams_form.interfaces import INPUT_MODE
from pyams_form.interfaces.widget import IObjectWidget
from pyams_form.template import widget_layout_config
from pyams_layer.interfaces import IFormLayer, IPyAMSLayer
from pyams_template.template import layout_config


@widget_layout_config(mode=INPUT_MODE,
                      template='templates/age-range-input-layout.pt', layer=IPyAMSLayer)
class IAgeRangeWidget(IObjectWidget):
    """Age range widget interface"""
