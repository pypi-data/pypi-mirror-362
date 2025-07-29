# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from zope.interface import Interface, implementer
from zope.schema import Int, Object
from zope.schema.fieldproperty import FieldProperty
from zope.schema.interfaces import IObject
from pyams_utils.factory import factory_config

__docformat__ = 'restructuredtext'

from pyams_content import _


class IAgeRange(Interface):
    """Age range attribute interface"""

    min_value = Int(title=_("Minimum age"),
                    required=False)

    max_value = Int(title=_("Maximum age"),
                    required=False)


@factory_config(IAgeRange)
class AgeRange:
    """Age range attribute object"""

    min_value = FieldProperty(IAgeRange['min_value'])
    max_value = FieldProperty(IAgeRange['max_value'])

    def __init__(self, value=None):
        if value:
            min_value = value.get('min_value')
            if min_value:
                self.min_value = int(min_value)
            max_value = value.get('max_value')
            if max_value:
                self.max_value = int(max_value)
            
    def __bool__(self):
        return bool(self.min_value or self.max_value)


class IAgeRangeField(IObject):
    """Age range schema field interface"""


@implementer(IAgeRangeField)
class AgeRangeField(Object):
    """Age range schema field class"""

    def __init__(self, **kwargs):
        if 'schema' in kwargs:
            del kwargs['schema']
        super().__init__(IAgeRange, **kwargs)
