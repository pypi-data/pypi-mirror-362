# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from datetime import datetime

from zope.interface import Interface
from zope.schema import Choice, Float, Int, TextLine, URI

from pyams_content.shared.common import ISharedContent
from pyams_content.shared.common.interfaces import ISharedToolPortalContext, IWfSharedContentPortalContext
from pyams_content.shared.common.interfaces.types import VISIBLE_DATA_TYPES_VOCABULARY
from pyams_content.shared.resource.schema import AgeRangeField
from pyams_i18n.schema import I18nHTMLField, I18nTextField
from pyams_sequence.interfaces import IInternalReferencesList

__docformat__ = 'restructuredtext'

from pyams_content import _


RESOURCE_CONTENT_TYPE = 'resource'
RESOURCE_CONTENT_NAME = _("Resource")


RESOURCE_INFORMATION_KEY = 'pyams_content.resource'


class IResourceInfo(Interface):
    """Resource information interface"""

    original_country = TextLine(title=_("Original country"),
                                required=False)

    original_title = TextLine(title=_("Original title"),
                              required=False)

    author = TextLine(title=_("Author"),
                      required=False)

    translator = TextLine(title=_("Translator"),
                          required=False)

    illustrator = TextLine(title=_("Illustrator"),
                           required=False)

    drawer = TextLine(title=_("Drawer"),
                      required=False)

    colourist = TextLine(title=_("Colourist"),
                         required=False)

    lettering = TextLine(title=_("Lettering"),
                         required=False)

    producer = TextLine(title=_("Producer"),
                        required=False)

    director = TextLine(title=_("Director"),
                        required=False)

    actors = TextLine(title=_("Actors"),
                      required=False)

    editor = TextLine(title=_("Editor"),
                      required=False)

    collection = TextLine(title=_("Collection"),
                          required=False)

    series = TextLine(title=_("Series"),
                      required=False)

    volume = TextLine(title=_("Volume"),
                      required=False)

    format = TextLine(title=_("Format"),
                      required=False)

    nb_pages = Int(title=_("Nb pages"),
                   min=0,
                   required=False)

    duration = TextLine(title=_("Duration"),
                        required=False)

    age_range = AgeRangeField(title=_("Age range"),
                              required=False)

    release_year = Choice(title=_("Release year"),
                          values=range(datetime.today().year, 1970, -1),
                          required=False)

    awards = I18nTextField(title=_("Awards"),
                           required=False)

    editor_reference = TextLine(title=_("Editor reference"),
                                required=False)

    isbn_number = TextLine(title=_("ISBN number"),
                           required=False)

    price = Float(title=_("Price"),
                  min=0.0,
                  required=False)

    source_url = URI(title=_("Source URI"),
                     description=_("External URL used to get more information about resource"),
                     required=False)

    summary = I18nHTMLField(title=_("Summary"),
                            required=False)

    synopsis = I18nHTMLField(title=_("Synopsis"),
                             required=False)

    publisher_words = I18nHTMLField(title=_("Publisher's words"),
                                    required=False)

    
class IWfResource(IWfSharedContentPortalContext, IInternalReferencesList):
    """Resource interface"""
    
    data_type = Choice(title=_("Data type"),
                       description=_("Type of content data"),
                       required=True,
                       vocabulary=VISIBLE_DATA_TYPES_VOCABULARY)


class IResource(ISharedContent):
    """Workflow managed resource interface"""


class IResourceManager(ISharedToolPortalContext):
    """Resources manager interface"""
