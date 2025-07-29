# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from persistent import Persistent
from zope.container.contained import Contained
from zope.schema.fieldproperty import FieldProperty

from pyams_content.reference.pictogram.interfaces import IThesaurusTermPictogramsInfo, IThesaurusTermPictogramsTarget, \
    THESAURUS_TERM_PICTOGRAMS_INFO_KEY
from pyams_thesaurus.interfaces.extension import IThesaurusTermExtension
from pyams_utils.adapter import adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.registry import utility_config

__docformat__ = 'restructuredtext'

from pyams_content import _


@factory_config(provided=IThesaurusTermPictogramsInfo)
class ThesaurusTermPictogramsInfo(Persistent, Contained):
    """Thesaurus term pictograms info"""
    
    pictogram_on = FieldProperty(IThesaurusTermPictogramsInfo['pictogram_on'])
    pictogram_off = FieldProperty(IThesaurusTermPictogramsInfo['pictogram_off'])


@adapter_config(required=IThesaurusTermPictogramsTarget,
                provides=IThesaurusTermPictogramsInfo)
def thesaurus_term_pictograms_factory(context):
    """Thesaurus term pictograms factory"""
    return get_annotation_adapter(context, THESAURUS_TERM_PICTOGRAMS_INFO_KEY,
                                  IThesaurusTermPictogramsInfo)


@utility_config(name='pictograms',
                provides=IThesaurusTermExtension)
class PictogramsThesaurusTermExtension:
    """Pictograms thesaurus term extension"""
    
    label = _("Pictograms")
    weight = 30
    
    icon_css_class = 'fas fa-icons'
    
    target_interface = IThesaurusTermPictogramsTarget
    target_view = 'pictograms-dialog.html'
    