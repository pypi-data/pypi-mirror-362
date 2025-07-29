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

"""PyAMS_content.component.association.skin.interfaces module

This module defines interfaces of associations renderers.
"""

from zope.interface import Interface
from zope.schema import Choice

from pyams_utils.text import PYAMS_HTML_RENDERERS_VOCABULARY

__docformat__ = 'restructuredtext'

from pyams_content import _


class IAssociationParagraphDefaultRendererSettings(Interface):
    """Associations paragraph default renderer settings interface"""

    description_format = Choice(title=_("Description format"),
                                description=_("Formatting style used for description in associations"),
                                vocabulary=PYAMS_HTML_RENDERERS_VOCABULARY,
                                required=True,
                                default='text')
