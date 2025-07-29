#
# Copyright (c) 2015-2022 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.component.extfile.zmi.widget module

This module provides a custom widget used for external files title field.
"""

__docformat__ = 'restructuredtext'

from zope.interface import implementer_only

from pyams_content.component.extfile import IExtFileManagerInfo
from pyams_form.browser.text import TextWidget
from pyams_form.interfaces import DISPLAY_MODE, INPUT_MODE
from pyams_form.interfaces.widget import ITextWidget
from pyams_form.template import widget_template_config
from pyams_form.widget import FieldWidget
from pyams_i18n.interfaces import II18n
from pyams_i18n_views.interfaces import II18nWidget
from pyams_i18n_views.widget import I18nWidget
from pyams_layer.interfaces import IPyAMSLayer


class IExtFileTitleWidget(ITextWidget):
    """External file title widget marker interface"""


@widget_template_config(mode=INPUT_MODE,
                        template='templates/extfile-title-input.pt', layer=IPyAMSLayer)
@widget_template_config(mode=DISPLAY_MODE,
                        template='templates/extfile-title-display.pt', layer=IPyAMSLayer)
@implementer_only(IExtFileTitleWidget)
class ExtFileTitleWidget(TextWidget):
    """External file title widget"""

    @property
    def prefix(self):
        """Widget prefix getter"""
        info = IExtFileManagerInfo(self.request.root, None)
        if info is not None:
            lang = getattr(self, 'lang', None)
            if lang is not None:
                return (info.default_title_prefix or {}).get(lang, '') or ''
            return II18n(info).query_attribute('default_title_prefix', request=self.request)
        return ''


def ExtFileTitleFieldWidget(field, request):  # pylint: disable=invalid-name
    """External file title widget factory"""
    return FieldWidget(field, ExtFileTitleWidget(request))


#
# I18n external file title field widget
#

class II18nExtFileTitleWidget(II18nWidget):
    """I18n external file title field widget interface"""


class I18nExtFileTitleWidget(I18nWidget):
    """I18n external file title widget"""


def I18nExtFileTitleFieldWidget(field, request):  # pylint: disable=invalid-name
    """I18n external file title widget factory"""
    widget = I18nExtFileTitleWidget(request)
    widget.widget_factory = ExtFileTitleFieldWidget
    return FieldWidget(field, widget)
