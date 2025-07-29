# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from zope.interface import Interface, alsoProvides, implementer_only

from pyams_content.shared.resource.schema import AgeRange, IAgeRange, IAgeRangeField
from pyams_content.shared.resource.zmi.interfaces import IAgeRangeWidget
from pyams_form.interfaces import IObjectFactory
from pyams_form.interfaces.form import IForm
from pyams_form.interfaces.widget import IFieldWidget
from pyams_form.object import ObjectWidget
from pyams_form.widget import FieldWidget
from pyams_layer.interfaces import IFormLayer
from pyams_utils.adapter import adapter_config
from pyams_utils.factory import get_interface_name, get_object_factory
from pyams_utils.interfaces.data import IObjectData

__docformat__ = 'restructuredtext'


@adapter_config(name=get_interface_name(IAgeRange),
                required=(Interface, IFormLayer, IForm, IAgeRangeWidget),
                provides=IObjectFactory)
def age_range_factory(*args):  # pylint: disable=unused-argument
    """Age range object factory"""
    return get_object_factory(IAgeRange)


@implementer_only(IAgeRangeWidget)
class AgeRangeWidget(ObjectWidget):
    """Age range widget"""

    def update_widgets(self, set_errors=True):
        super().update_widgets(set_errors)
        widgets = self.widgets
        for name in ('min_value', 'max_value'):
            widget = widgets.get(name)
            if widget is not None:
                widget.label_css_class = 'col-4 col-md-3'
                widget.input_css_class = 'col-3 col-md-2'
                widget.object_data = {
                    'input-mask': '9{1,3}'
                }
                alsoProvides(widget, IObjectData)


@adapter_config(required=(IAgeRangeField, IFormLayer),
                provides=IFieldWidget)
def AgeRangeFieldWidget(field, request):
    """Age range field widget factory"""
    return FieldWidget(field, AgeRangeWidget(request))
