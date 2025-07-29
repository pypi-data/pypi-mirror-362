# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from pyams_content.reference.pictogram.interfaces import IThesaurusTermPictogramsInfo
from pyams_content.reference.pictogram.zmi.widget import PictogramSelectFieldWidget
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


@ajax_form_config(name='pictograms-dialog.html',
                  context=IThesaurusTerm, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class ThesaurusTermPictogramsPropertiesEditForm(ThesaurusTermExtensionEditForm):
    """Thesaurus term pictograms properties edit form"""
    
    subtitle = _("Associated pictograms")
    legend = _("Pictograms properties")
    modal_class = 'modal-lg'
    
    fields = Fields(IThesaurusTermPictogramsInfo)
    fields['pictogram_on'].widget_factory = PictogramSelectFieldWidget
    fields['pictogram_off'].widget_factory = PictogramSelectFieldWidget


@adapter_config(required=(IThesaurusTerm, IPyAMSLayer, ThesaurusTermPictogramsPropertiesEditForm),
                provides=IFormContent)
def thesaurus_term_pictograms_form_content(context, request, form):
    """Thesaurus term pictograms edit form content getter"""
    return IThesaurusTermPictogramsInfo(context)
