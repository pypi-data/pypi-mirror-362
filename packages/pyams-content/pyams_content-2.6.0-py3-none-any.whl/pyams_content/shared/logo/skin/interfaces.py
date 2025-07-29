# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from collections import OrderedDict
from enum import Enum

from zope.interface import Interface
from zope.schema import Bool, Choice
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

__docformat__ = 'restructuredtext'

from pyams_content import _


class TARGET_PRIORITY(Enum):
    """Logos target priority"""
    DISABLED = 'disabled'
    INTERNAL_FIRST = 'internal'
    EXTERNAL_FIRST = 'external'
    
    
TARGET_PRIORITY_LABELS = OrderedDict((
    (TARGET_PRIORITY.DISABLED, _("Disabled link")),
    (TARGET_PRIORITY.INTERNAL_FIRST, _("Use internal reference first")),
    (TARGET_PRIORITY.EXTERNAL_FIRST, _("Use external URL first"))
))

TARGET_PRIORITY_VOCABULARY = SimpleVocabulary([
    SimpleTerm(v.value, title=t)
    for v, t in TARGET_PRIORITY_LABELS.items()
])


class IBaseLogosRendererSettings(Interface):
    """Base logos renderer settings interface"""
    
    target_priority = Choice(title=_("Links priority"),
                             description=_("Order in which internal or external links are evaluated"),
                             vocabulary=TARGET_PRIORITY_VOCABULARY,
                             default=TARGET_PRIORITY.EXTERNAL_FIRST.value,
                             required=True)

    force_canonical_url = Bool(title=_("Force canonical URL"),
                               description=_("By default, internal links use a \"relative\" URL, "
                                             "which tries to display link target in the current "
                                             "context; by using a canonical URL, you can display "
                                             "target in it's attachment context (if defined)"),
                               required=False,
                               default=False)

    
class ILogosParagraphDefaultRendererSettings(IBaseLogosRendererSettings):
    """Logos paragraph default renderer settings interface"""
