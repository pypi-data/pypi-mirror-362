# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from zope.schema import TextLine, URI

from pyams_content.component.paragraph import IBaseParagraph
from pyams_content.component.paragraph.schema import ParagraphRendererChoice
from pyams_content.shared.common import ISharedContent, IWfSharedContent
from pyams_content.shared.common.interfaces import ISharedTool
from pyams_file.schema import I18nImageField
from pyams_i18n.schema import I18nTextLineField
from pyams_sequence.interfaces import IInternalReference, IInternalReferencesList
from pyams_sequence.schema import InternalReferenceField, InternalReferencesListField

__docformat__ = 'restructuredtext'

from pyams_content import _


LOGO_CONTENT_TYPE = 'logo'
LOGO_CONTENT_NAME = _("Logo")


class IWfLogo(IWfSharedContent, IInternalReference):
    """Logo interface"""

    title = I18nTextLineField(title=_("Title"),
                              description=_("Full name of logo organization"),
                              required=True)

    alt_title = I18nTextLineField(title=_("Alternate title"),
                                  description=_("If set, this title will be displayed in "
                                                "front-office instead of original title"),
                                  required=False)

    acronym = TextLine(title=_("Acronym"),
                       description=_("Matching logo acronym, without spaces or separators"),
                       required=False)

    image = I18nImageField(title=_("Image (colored)"),
                           description=_("Image data"),
                           required=True)

    monochrome_image = I18nImageField(title=_("Image (monochrome)"),
                                      description=_("An alternate image which can be used by some "
                                                    "presentation templates"),
                                      required=False)

    url = URI(title=_("Target URL"),
              description=_("URL used to access external resource"),
              required=False)

    reference = InternalReferenceField(title=_("Internal reference"),
                                       description=_("Internal link target reference. You can "
                                                     "search a reference using '+' followed by "
                                                     "internal number, of by entering text "
                                                     "matching content title."),
                                       required=False)

    
class ILogo(ISharedContent):
    """Logo interface"""
    
    
class ILogoManager(ISharedTool):
    """Logos manager interface"""
    
    
LOGOS_PARAGRAPH_TYPE = 'logos'
LOGOS_PARAGRAPH_NAME = _("Logos")
LOGOS_PARAGRAPH_RENDERERS = 'PyAMS_content.paragraph.logos.renderers'
LOGOS_PARAGRAPH_ICON_CLASS = 'fas fa-icons'


class ILogosParagraph(IBaseParagraph, IInternalReferencesList):
    """Logos paragraph interface"""

    references = InternalReferencesListField(title=_("Logos references"),
                                             description=_("List of internal logos references"),
                                             content_type=LOGO_CONTENT_TYPE)
    
    def get_logos(self, status=None, with_reference=False):
        """Get logos from internal references"""
        
    renderer = ParagraphRendererChoice(description=_("Presentation template used for this logos paragraph"),
                                       renderers=LOGOS_PARAGRAPH_RENDERERS)
