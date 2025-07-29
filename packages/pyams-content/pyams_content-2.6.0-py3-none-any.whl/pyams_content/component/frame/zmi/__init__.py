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

"""PyAMS_content.component.frame.zmi module

This module defines components for framed text paragraph management interface.
"""

from pyramid.events import subscriber

from pyams_content.component.frame.interfaces import FRAME_PARAGRAPH_ICON_CLASS, FRAME_PARAGRAPH_NAME, \
    FRAME_PARAGRAPH_TYPE, IFrameParagraph
from pyams_content.component.frame.portlet import IFramePortletSettings
from pyams_content.component.paragraph import IParagraphContainer, IParagraphContainerTarget
from pyams_content.component.paragraph.zmi import BaseParagraphAddForm, BaseParagraphAddMenu, \
    IParagraphContainerBaseTable
from pyams_content.component.paragraph.zmi.html import extract_html_paragraph_data
from pyams_form.ajax import ajax_form_config
from pyams_form.interfaces.form import IDataExtractedEvent
from pyams_layer.interfaces import IPyAMSLayer
from pyams_skin.interfaces.widget import IHTMLEditorConfiguration
from pyams_utils.adapter import adapter_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.form import IPropertiesEditForm
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager

__docformat__ = 'restructuredtext'


@viewlet_config(name='add-frame-paragraph.menu',
                context=IParagraphContainerTarget, layer=IAdminLayer,
                view=IParagraphContainerBaseTable,
                manager=IContextAddingsViewletManager, weight=600)
class FrameParagraphAddMenu(BaseParagraphAddMenu):
    """Frame paragraph add menu"""

    label = FRAME_PARAGRAPH_NAME
    icon_class = FRAME_PARAGRAPH_ICON_CLASS

    factory_name = FRAME_PARAGRAPH_TYPE
    href = 'add-frame-paragraph.html'


@ajax_form_config(name='add-frame-paragraph.html',
                  context=IParagraphContainer, layer=IPyAMSLayer)
class FrameParagraphAddForm(BaseParagraphAddForm):
    """HTML rich text paragraph add form"""

    content_factory = IFrameParagraph


@subscriber(IDataExtractedEvent, form_selector=FrameParagraphAddForm)
@subscriber(IDataExtractedEvent, context_selector=IFrameParagraph)
def extract_frame_paragraph_data(event):
    """Extract paragraph data"""
    extract_html_paragraph_data(event)


@adapter_config(name='body',
                required=(IParagraphContainer, IAdminLayer, FrameParagraphAddForm),
                provides=IHTMLEditorConfiguration)
@adapter_config(name='body',
                required=(IFrameParagraph, IAdminLayer, IPropertiesEditForm),
                provides=IHTMLEditorConfiguration)
@adapter_config(name='body',
                required=(IFramePortletSettings, IAdminLayer, IPropertiesEditForm),
                provides=IHTMLEditorConfiguration)
def frame_paragraph_editor_configuration(context, request, view):
    """Frame paragraph editor configuration"""
    return {
        'menubar': False,
        'plugins': 'paste textcolor lists charmap link pyams_link',
        'toolbar': 'undo redo | pastetext | h3 h4 | bold italic superscript | '
                   'forecolor backcolor | bullist numlist | '
                   'charmap pyams_link link',
        'toolbar1': False,
        'toolbar2': False,
        'height': 200
    }
