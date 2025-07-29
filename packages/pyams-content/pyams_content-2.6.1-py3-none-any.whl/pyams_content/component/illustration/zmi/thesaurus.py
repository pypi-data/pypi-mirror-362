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

"""PyAMS_content.component.illustration.zmi.thesaurus module

This module provides management components for thesaurus term
illustration extension.
"""

from pyams_content.component.illustration import IBaseIllustration, IIllustration
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IFormContent
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_thesaurus.interfaces.term import IThesaurusTerm
from pyams_thesaurus.zmi.extension import ThesaurusTermExtensionEditForm
from pyams_utils.adapter import adapter_config


__docformat__ = 'restructuredtext'

from pyams_content import _


@ajax_form_config(name='illustration-dialog.html',
                  context=IThesaurusTerm, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class ThesaurusTermIllustrationPropertiesEditForm(ThesaurusTermExtensionEditForm):
    """Thesaurus term illustration properties edit form"""

    subtitle = _("Associated illustration")
    legend = _("Illustration properties")
    modal_class = 'modal-xl'

    fields = Fields(IBaseIllustration)


@adapter_config(required=(IThesaurusTerm, IPyAMSLayer, ThesaurusTermIllustrationPropertiesEditForm),
                provides=IFormContent)
def thesaurus_term_illustration_form_content(context, request, form):
    """Thesaurus term illustration edit form content getter"""
    return IIllustration(context)
