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

"""PyAMS_content.component.paragraph.skin.html module

"""

from persistent import Persistent
from pygments.lexers import get_lexer_by_name
from zope.container.contained import Contained
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.illustration import IIllustration
from pyams_content.component.paragraph.interfaces.html import IHTMLParagraph, IRawParagraph
from pyams_content.component.paragraph.skin.interfaces.html import IHTMLParagraphAlertRendererSettings, \
    IHTMLParagraphRendererSettings
from pyams_content.feature.renderer import DefaultContentRenderer, IContentRenderer
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import DEFAULT_RENDERER_NAME
from pyams_template.template import template_config
from pyams_utils import library
from pyams_utils.adapter import adapter_config
from pyams_utils.factory import factory_config
from pyams_utils.fanstatic import ExternalResource
from pyams_utils.interfaces.pygments import IPygmentsCodeConfiguration
from pyams_utils.pygments import render_source
from pyams_utils.text import text_to_html

__docformat__ = 'restructuredtext'

from pyams_content import _


#
# Raw HTML code renderer
#

@adapter_config(name=DEFAULT_RENDERER_NAME,
                required=(IRawParagraph, IPyAMSLayer),
                provides=IContentRenderer)
@template_config(template='templates/raw.pt', layer=IPyAMSLayer)
@template_config(name='group',
                 template='templates/raw-group.pt', layer=IPyAMSLayer)
@template_config(name='group:tab',
                 template='templates/raw-group-tab.pt', layer=IPyAMSLayer)
class RawParagraphDefaultRenderer(DefaultContentRenderer):
    """Raw paragraph default renderer"""

    label = _("HTML source code (default)")
    
    @property
    def body(self):
        """Raw body getter"""
        return II18n(self.context).query_attribute('body', request=self.request)


@adapter_config(name='source-code',
                required=(IRawParagraph, IPyAMSLayer),
                provides=IContentRenderer)
@template_config(template='templates/raw-code.pt', layer=IPyAMSLayer)
@template_config(name='group',
                 template='templates/raw-code-group.pt', layer=IPyAMSLayer)
@template_config(name='group:tab',
                 template='templates/raw-code-group-tab.pt', layer=IPyAMSLayer)
class RawParagraphSourceCodeRenderer(DefaultContentRenderer):
    """Raw paragraph source code renderer"""

    label = _("Formatted source code")
    weight = 10

    settings_interface = IPygmentsCodeConfiguration

    @property
    def editor_filename(self):
        """ACE editor mode getter"""
        settings = self.settings
        if (settings is not None) and (settings.lexer not in (None, 'auto')):
            lexer = get_lexer_by_name(settings.lexer)
            return f"body.{lexer.filenames[0].rsplit('.', 1)[-1]}"
        return 'body.html'

    @property
    def resources(self):
        """Fanstatic resources getter"""
        settings = self.settings
        path = f'get-pygments-style.css?style={settings.style}'
        resource = library.known_resources.get(path)
        if resource is None:
            resource = ExternalResource(library, path, resource_type='css')
            if library.library_nr is None:
                library.init_library_nr()
        yield resource

    @property
    def body(self):
        """Formatted body getter"""
        body = II18n(self.context).query_attribute('body', request=self.request)
        if not body:
            return ''
        return render_source(body, self.settings)


@adapter_config(name='rest',
                required=(IRawParagraph, IPyAMSLayer),
                provides=IContentRenderer)
@template_config(template='templates/raw-code.pt', layer=IPyAMSLayer)
@template_config(name='group',
                 template='templates/raw-code-group.pt', layer=IPyAMSLayer)
@template_config(name='group:tab',
                 template='templates/raw-code-group-tab.pt', layer=IPyAMSLayer)
class RawParagraphRestRenderer(DefaultContentRenderer):
    """Raw paragraph ReStructured text renderer"""

    label = _("ReStructured text")
    weight = 20

    editor_filename = 'body.rst'

    @property
    def body(self):
        """Formatted body getter"""
        body = II18n(self.context).query_attribute('body', request=self.request)
        if not body:
            return ''
        return text_to_html(body, 'rest;oid_to_href;glossary', request=self.request)


@adapter_config(name='markdown',
                required=(IRawParagraph, IPyAMSLayer),
                provides=IContentRenderer)
@template_config(template='templates/raw-code.pt', layer=IPyAMSLayer)
@template_config(name='group',
                 template='templates/raw-code-group.pt', layer=IPyAMSLayer)
@template_config(name='group:tab',
                 template='templates/raw-code-group-tab.pt', layer=IPyAMSLayer)
class RawParagraphMarkdownRenderer(DefaultContentRenderer):
    """Raw paragraph Markdown text renderer"""

    label = _("Markdown text")
    weight = 30

    editor_filename = 'body.md'

    @property
    def body(self):
        """Formatted body getter"""
        body = II18n(self.context).query_attribute('body', request=self.request)
        if not body:
            return ''
        return text_to_html(body, 'markdown;oid_to_href;glossary', request=self.request)


#
# HTML rich text renderer
#

@factory_config(IHTMLParagraphRendererSettings)
class HTMLParagraphRendererSettings(Persistent, Contained):
    """HTML paragraph renderer settings"""

    xs_horizontal_padding = FieldProperty(IHTMLParagraphRendererSettings['xs_horizontal_padding'])
    sm_horizontal_padding = FieldProperty(IHTMLParagraphRendererSettings['sm_horizontal_padding'])
    md_horizontal_padding = FieldProperty(IHTMLParagraphRendererSettings['md_horizontal_padding'])
    lg_horizontal_padding = FieldProperty(IHTMLParagraphRendererSettings['lg_horizontal_padding'])
    xl_horizontal_padding = FieldProperty(IHTMLParagraphRendererSettings['xl_horizontal_padding'])

    def has_padding(self):
        """Check if any padding is defined"""
        return any((self.xs_horizontal_padding,
                    self.sm_horizontal_padding,
                    self.md_horizontal_padding,
                    self.lg_horizontal_padding,
                    self.xl_horizontal_padding))

    def get_padding(self):
        """Paddings getter"""
        result = []
        for device in ('xs', 'sm', 'md', 'lg', 'xl'):
            padding = getattr(self, f'{device}_horizontal_padding')
            if padding is not None:
                result.append(f'col-{device}-{12 - padding*2} offset-{device}-{padding}')
        return ' '.join(result)


@adapter_config(name=DEFAULT_RENDERER_NAME,
                required=(IHTMLParagraph, IPyAMSLayer),
                provides=IContentRenderer)
@template_config(template='templates/html.pt', layer=IPyAMSLayer)
@template_config(name='group',
                 template='templates/html-group.pt', layer=IPyAMSLayer)
@template_config(name='group:tab',
                 template='templates/html-group-tab.pt', layer=IPyAMSLayer)
class HTMLParagraphRenderer(DefaultContentRenderer):
    """HTML paragraph default renderer"""

    label = _("Rich text (default)")

    settings_interface = IHTMLParagraphRendererSettings

    illustration = None
    illustration_renderer = None

    def update(self):
        super().update()
        illustration = IIllustration(self.context)
        if illustration.has_data():
            self.illustration = illustration
            self.illustration_renderer = illustration.get_renderer(self.request)
            self.illustration_renderer.update()


#
# HTML rich text 'alert' renderer
#

@factory_config(IHTMLParagraphAlertRendererSettings)
class HTMLParagraphAlertRendererSettings(HTMLParagraphRendererSettings):
    """HTML paragraph alert renderer settings"""

    status = FieldProperty(IHTMLParagraphAlertRendererSettings['status'])
    display_dismiss_button = FieldProperty(IHTMLParagraphAlertRendererSettings['display_dismiss_button'])


@adapter_config(name='alert',
                required=(IHTMLParagraph, IPyAMSLayer),
                provides=IContentRenderer)
@template_config(template='templates/html-alert.pt', layer=IPyAMSLayer)
@template_config(name='group',
                 template='templates/html-alert.pt', layer=IPyAMSLayer)
@template_config(name='group:tab',
                 template='templates/html-alert-group-tab.pt', layer=IPyAMSLayer)
class HTMLParagraphAlertRenderer(HTMLParagraphRenderer):
    """HTML paragraph alert renderer"""

    label = _("Bootstrap alert")

    settings_interface = IHTMLParagraphAlertRendererSettings
