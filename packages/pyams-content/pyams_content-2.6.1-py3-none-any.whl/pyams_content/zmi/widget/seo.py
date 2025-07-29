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

"""PyAMS_content.zmi.widget.seo module

This module define a custom widget which can be used to automatically display
an "SEO quality"
"""

__docformat__ = 'restructuredtext'

from zope.interface import implementer, implementer_only

from pyams_content.zmi.widget.interfaces import II18nSEOTextLineWidget, ISEOTextLineWidget
from pyams_form.browser.text import TextWidget
from pyams_form.interfaces import INPUT_MODE
from pyams_form.template import widget_template_config
from pyams_form.widget import FieldWidget
from pyams_i18n_views.widget import I18nWidget
from pyams_layer.interfaces import IPyAMSLayer


@widget_template_config(mode=INPUT_MODE,
                        template='templates/seo-textline-input.pt',
                        layer=IPyAMSLayer)
@implementer_only(ISEOTextLineWidget)
class SEOTextLineWidget(TextWidget):
    """SEO text line widget"""

    @property
    def length(self):
        """Get current length of text"""
        return len(self.value or '')

    @property
    def status(self):
        """Get widget status based on text length; a "good" length is between 40 and 66
        characters
        """
        status = 'success'
        length = self.length
        if length < 20 or length > 80:
            status = 'danger'
        elif length < 40 or length > 66:
            status = 'warning'
        return status


def SEOTextLineFieldWidget(field, request):  # pylint: disable=invalid-name
    """SEO text line field widget factory"""
    return FieldWidget(field, SEOTextLineWidget(request))


#
# I18n SEO text line widget
#

@implementer(II18nSEOTextLineWidget)
class I18nSEOTextLineWidget(I18nWidget):
    """I18n text line widget with SEO quality marker"""


def I18nSEOTextLineFieldWidget(field, request):
    """I18n text line field widget with SEO quality marker factory"""
    widget = I18nSEOTextLineWidget(request)
    widget.widget_factory = SEOTextLineFieldWidget
    return FieldWidget(field, widget)
