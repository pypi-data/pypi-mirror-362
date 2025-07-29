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

"""PyAMS_content.component.paragraph.zmi.html module

This module provides management interface components for raw source code and rich text
paragraphs.
"""

from pyquery import PyQuery
from pyramid.events import subscriber
from zope.interface import Invalid, alsoProvides

from pyams_content.component.links.interfaces import IExternalLinksManagerInfo
from pyams_content.component.paragraph import IParagraphContainer, IParagraphContainerTarget
from pyams_content.component.paragraph.interfaces.html import HTML_PARAGRAPH_ICON_CLASS, \
    HTML_PARAGRAPH_NAME, HTML_PARAGRAPH_TYPE, IHTMLParagraph, IRawParagraph, \
    RAW_PARAGRAPH_ICON_CLASS, RAW_PARAGRAPH_NAME, RAW_PARAGRAPH_TYPE
from pyams_content.component.paragraph.zmi import BaseParagraphAddForm, BaseParagraphAddMenu
from pyams_content.component.paragraph.zmi.interfaces import IParagraphContainerBaseTable
from pyams_form.ajax import ajax_form_config
from pyams_form.interfaces.form import IDataExtractedEvent, IFormUpdatedEvent
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import DEFAULT_RENDERER_NAME, HIDDEN_RENDERER_NAME
from pyams_utils.interfaces.data import IObjectData
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.form import IPropertiesEditForm
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager

__docformat__ = 'restructuredtext'

from pyams_content import _


#
# Raw paragraphs forms
#

@viewlet_config(name='add-raw-paragraph.menu',
                context=IParagraphContainerTarget, layer=IAdminLayer,
                view=IParagraphContainerBaseTable,
                manager=IContextAddingsViewletManager, weight=600)
class RawParagraphAddMenu(BaseParagraphAddMenu):
    """Raw paragraph add menu"""

    label = RAW_PARAGRAPH_NAME
    icon_class = RAW_PARAGRAPH_ICON_CLASS

    factory_name = RAW_PARAGRAPH_TYPE
    href = 'add-raw-paragraph.html'


@ajax_form_config(name='add-raw-paragraph.html',
                  context=IParagraphContainer, layer=IPyAMSLayer)
class RawParagraphAddForm(BaseParagraphAddForm):
    """Raw paragraph add form"""

    content_factory = IRawParagraph


@subscriber(IFormUpdatedEvent,
            form_selector=RawParagraphAddForm)
@subscriber(IFormUpdatedEvent,
            form_selector=IPropertiesEditForm,
            context_selector=IRawParagraph)
def handle_raw_paragraph_form_update(event):
    """Handle raw paragraph form update"""
    body = event.form.widgets.get('body')
    if body is not None:
        body.add_widgets_class('height-100')
        body.widget_css_class = 'editor height-300px'
        filename = 'body.html'
        if IPropertiesEditForm.providedBy(event.form):
            context = event.form.context
            if context.renderer not in (HIDDEN_RENDERER_NAME, DEFAULT_RENDERER_NAME):
                renderer = context.get_renderer()
                if renderer is not None:
                    filename = renderer.editor_filename
        for widget in body.widgets.values():
            widget.object_data = {
                'ams-filename': filename
            }
            alsoProvides(widget, IObjectData)


#
# HTML paragraphs forms
#

@viewlet_config(name='add-html-paragraph.menu',
                context=IParagraphContainerTarget, layer=IAdminLayer,
                view=IParagraphContainerBaseTable,
                manager=IContextAddingsViewletManager, weight=50)
class HTMLParagraphAddMenu(BaseParagraphAddMenu):
    """HTML paragraph add menu"""

    label = HTML_PARAGRAPH_NAME
    icon_class = HTML_PARAGRAPH_ICON_CLASS

    factory_name = HTML_PARAGRAPH_TYPE
    href = 'add-html-paragraph.html'


@ajax_form_config(name='add-html-paragraph.html',
                  context=IParagraphContainer, layer=IPyAMSLayer)
class HTMLParagraphAddForm(BaseParagraphAddForm):
    """HTML rich text paragraph add form"""

    content_factory = IHTMLParagraph


@subscriber(IDataExtractedEvent, form_selector=HTMLParagraphAddForm)
@subscriber(IDataExtractedEvent, context_selector=IHTMLParagraph)
def extract_html_paragraph_data(event):
    """Extract paragraph data"""
    form = event.form
    request = form.request
    settings = IExternalLinksManagerInfo(request.root, None)
    if (settings is None) or not settings.check_external_links:
        return
    data = event.data
    for lang, body in data.get('body', {}).items():
        html = PyQuery(f'<html>{body}</html>')
        for link in html('a[href]'):
            href = link.attrib['href']
            for host in settings.forbidden_hosts or ():
                if host and href.startswith(host):
                    form.widgets.errors += (Invalid(_("You can't create an external link to this site! "
                                                      "Use an internal link instead...")),)
                    return
