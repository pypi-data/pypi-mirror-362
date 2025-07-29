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

"""PyAMS_content.component.illustration.thesaurus module

This module provides a custom thesaurus extension which allows to assign an
illustration on any thesaurus term.
"""

from pyams_content.component.illustration.interfaces import IBaseIllustrationTarget
from pyams_thesaurus.interfaces.extension import IThesaurusTermExtension
from pyams_utils.registry import utility_config


__docformat__ = 'restructuredtext'

from pyams_content import _


@utility_config(name='illustration',
                provides=IThesaurusTermExtension)
class IllustrationThesaurusTermExtension:
    """Illustration thesaurus term extension"""

    label = _("Illustration")
    weight = 20

    icon_css_class = 'far fa-image'

    target_interface = IBaseIllustrationTarget
    target_view = 'illustration-dialog.html'
